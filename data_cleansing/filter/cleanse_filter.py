#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cleanse_filter.py"""

__author__ = 'Gary.Z'

import sys
import numpy as np

from data_cleansing.rule.abstract_rule import *
from data_cleansing.utils import *
from data_cleansing.clock import *
from data_cleansing.filter.abstract_filter import *

logger = get_logger(__name__)


class FilterResetColumnNames(Filter):
    def __init__(self):
        super().__init__('pre-process-1', 'set student info column name with _1~_N, set rest columns follow predefined rules, e.g. A1-A')
        pass

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        if incoming['idx'] <= HEADER_ROW_INDEX:
            logger.info(self.__str__())
            reset_column_names(outgoing, generate_excel_column_indexes(iter_cnt=2))
            build_question_to_column_mapping_v2(outgoing, q2c_mapping)
        else:
            chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterExcludeUnnecessaryHeaders(Filter):
    def __init__(self, start_row=1, row_count=2):
        super().__init__('pre-process-2', 'filter pre-process-2: removing unnecessary header rows start at {}, count {}'
                         .format(HEADER_ROW_INDEX + start_row, row_count))
        self.__start_row = start_row
        self.__row_count = row_count

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        if (incoming['idx'] >= HEADER_ROW_INDEX + self.__start_row) and \
                (incoming['idx'] <= HEADER_ROW_INDEX + self.__start_row + self.__row_count - 1):
            logger.info('{}, current row: {}'.format(self.__str__(), incoming['idx']))
            outgoing.clear()
        else:
            chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterOnlyIncludeDegree(Filter):
    def __init__(self, degree=None, filter_column='_12'):
        super().__init__('pre-process-3', 'filter records with degree: {}'.format(degree))
        self.__degree = degree
        self.__filter_column = filter_column

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        column_index = q2c_mapping[self.__filter_column][0]
        if self.__degree is not None and incoming['row'][column_index].value != self.__degree:
            logger.debug(self.__str__())
            outgoing.clear()
        else:
            chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterExcludeTestRecords(Filter):
    def __init__(self, filter_column='_14'):
        super().__init__('1', 'remove test data, e.g. column {} (专业名称) with value {}'.format(filter_column, MAJOR_FILTER_LIST))
        self.__filter_column = filter_column

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        column_index = q2c_mapping[self.__filter_column][0]
        if incoming['row'][column_index].value in MAJOR_FILTER_LIST:
            logger.debug(self.__str__())
            outgoing.clear()
        else:
            chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterExcludeRecordWithoutA2Answer(Filter):
    def __init__(self, filter_column='A2'):
        super().__init__('2.1', 'remove un-qualified row, e.g. no answer for question {}'.format(filter_column))
        self.__filter_column = filter_column

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        column_index = q2c_mapping[self.__filter_column][0]
        if incoming['row'][column_index].value is None or incoming['row'][column_index].value == '':
            logger.debug(self.__str__())
            outgoing.clear()
        else:
            chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterExcludeRecordWithoutSubmitTime(Filter):
    def __init__(self, filter_column='_22'):
        super().__init__('2.2', 'remove un-submitted row, e.g. no submit-time (column {}) exist'.format(filter_column))
        self.__filter_column = filter_column

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        column_index = q2c_mapping[self.__filter_column][0]
        if incoming['row'][column_index].value is None or incoming['row'][column_index].value == '':
            logger.debug(self.__str__())
            outgoing.clear()
        else:
            chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterRinseIrrelevantAnswers(Filter):
    def __init__(self, id, irrelevant_question_rules):
        super().__init__(id, 'replace non-relevance answers(cell) with NaN against question-relevance rules')
        self.__irrelevant_question_rules = irrelevant_question_rules

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        # logger.debug(self.__str__())

        for rule in self.__irrelevant_question_rules:
            # logger.debug('apply rule: {}'.format(rule))

            question_index = q2c_mapping[rule[RINSE_RULE_KEY_QUESTION]][0]

            answer = incoming['row'][question_index].value
            if answer is None:
                answer = ''

            flag = False
            if rule[RINSE_RULE_KEY_OPERATOR] == RINSE_RULE_OPERATOR_IN:
                flag = answer in rule[RINSE_RULE_KEY_ANSWER]
            elif rule[RINSE_RULE_KEY_OPERATOR] == RINSE_RULE_OPERATOR_NOTIN:
                flag = answer not in rule[RINSE_RULE_KEY_ANSWER]
            else:
                # logger.info(">> no applicable operator: {}".format(rule[KEY_OPERATOR]))
                pass

            i = 0
            if flag:
                for action_id in rule[RINSE_RULE_KEY_ACTION]:
                    for action_index in q2c_mapping[action_id]:
                        if outgoing[action_index] is None or outgoing[action_index] == '':
                            outgoing[action_index] = None
                            i += 1
            # if i > 0:
                # logger.debug('>> {} cells rinsed'.format(i))

            chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterRinseNcOptionValues(Filter):
    def __init__(self, filter_columns=('H5-L', 'H6-H')):
        super().__init__('4', 'replace values like "无法评价", "以上均不需要改进" with NaN')
        self.__filter_columns = filter_columns

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        # logger.debug(self.__str__())

        i = 0
        for idx in range(0, outgoing.__len__()):
            if outgoing[idx] in NC_OPTION_FILTER_LIST:
                outgoing[idx] = None
                i += 1

        for filter_column in self.__filter_columns:
            column_index = q2c_mapping[filter_column][0]
            if outgoing[column_index] is not None or outgoing[column_index] == '':
                outgoing[column_index] = None
                i += 1

        # logger.debug('>> {} cells rinsed'.format(i))

        chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterRinseInvalidAnswers(Filter):
    def __init__(self, filter_column='G1'):
        super().__init__('5', 'replace invalid answers(cell) with NaN')
        self.__filter_column = filter_column

    # @clocking
    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        # logger.debug(self.__str__())

        i = 0
        for column_index in q2c_mapping[self.__filter_column]:
            if outgoing[column_index] in G1_OPTION_FILTER_LIST:
                outgoing[column_index] = None
                i += 1

        # logger.debug('>> {} cells rinsed'.format(i))

        chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterRinseUnusualSalaryValues(Filter):
    def __init__(self, salary_value_collector, filter_column='B6'):
        super().__init__('6', 'rinse salary < 1000, top 0.3%, ABS(diff of MEAN) > 4 * STDEV')
        self.__salary_value_collector = salary_value_collector
        self.__filter_column = filter_column

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        # logger.info(self.__str__())

        lower_limit = self.__salary_value_collector.get_lower_limit()
        higher_limit = self.__salary_value_collector.get_higher_limit()
        mean = self.__salary_value_collector.get_mean()
        # stdev = self.__salary_value_collector.get_stdev()
        stdev_4 = self.__salary_value_collector.get_stdev_4()

        column_index = q2c_mapping[self.__filter_column][0]
        cell_value = outgoing[column_index]
        if cell_value is not None and cell_value != '':
            salary_value = int(cell_value)
            if salary_value < lower_limit:
                logger.debug('>> salary {} rinsed by lower limit: {}'.format(outgoing[column_index], lower_limit))
                outgoing[column_index] = None
            if salary_value >= higher_limit:
                logger.debug('>> salary {} rinsed by higher limit: {}, top_n = {}'
                             .format(outgoing[column_index], higher_limit, self.__salary_value_collector.get_top_n()))
                outgoing[column_index] = None
            if abs(salary_value - mean) > stdev_4:
                logger.debug('>> salary {} rinsed by ABS(diff of MEAN) = {} > 4 * STDEV = {}'
                             .format(outgoing[column_index], abs(salary_value - mean), stdev_4))
                outgoing[column_index] = None

        chain.do_filter(incoming, outgoing, q2c_mapping)

