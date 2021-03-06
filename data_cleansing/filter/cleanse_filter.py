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
from data_cleansing.validation.cleanse_validator import *

# logger = get_logger(__name__)


class FilterResetColumnNames(Filter):
    def __init__(self, log_handler=None):
        super().__init__('pre-process-1', 'set student info column name with _1~_N, set rest columns follow predefined rules, e.g. A1-A', log_handler)

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        if incoming['idx'] <= HEADER_ROW_INDEX:
            self._counter += 1
            # logger.info(self.__str__())
            question_id_header_validator = QuestionIdHeaderValidator()
            question_id_header_validator.do_validate(outgoing)
            reset_column_names(outgoing, generate_excel_column_indexes(iter_cnt=3))
            build_question_to_column_mapping_v2(outgoing, q2c_mapping)
        else:
            chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterExcludeUnnecessaryHeaders(Filter):
    def __init__(self, start_row=1, row_count=2, log_handler=None):
        super().__init__('pre-process-2', 'filter pre-process-2: removing unnecessary header rows start at {}, count {}'
                         .format(HEADER_ROW_INDEX + start_row, row_count), log_handler)
        self.__start_row = start_row
        self.__row_count = row_count

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        if (incoming['idx'] >= HEADER_ROW_INDEX + self.__start_row) and \
                (incoming['idx'] <= HEADER_ROW_INDEX + self.__start_row + self.__row_count - 1):
            self._counter += 1
            # logger.info('{}, current row: {}'.format(self.__str__(), incoming['idx']))
            outgoing.clear()
        else:
            chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterOnlyIncludeDegree(Filter):
    def __init__(self, degree=None, filter_column='_12', log_handler=None):
        super().__init__('pre-process-3', 'filter records with degree: {}'.format(degree), log_handler)
        self.__degree = degree
        self.__filter_column = filter_column

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        column_index = q2c_mapping[self.__filter_column][0]
        if self.__degree is not None and incoming['row'][column_index].value != self.__degree:
            self._counter += 1
            # logger.debug(self.__str__())
            outgoing.clear()
        else:
            chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterExcludeTestRecords(Filter):
    def __init__(self, filter_column='_14', log_handler=None):
        super().__init__('1', 'remove test data, e.g. column {} (专业名称) with value {}'.format(filter_column, MAJOR_FILTER_LIST), log_handler)
        self.__filter_column = filter_column

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        column_index = q2c_mapping[self.__filter_column][0]
        if incoming['row'][column_index].value in MAJOR_FILTER_LIST:
            self._counter += 1
            # logger.debug(self.__str__())
            outgoing.clear()
        else:
            chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterExcludeRecordWithoutA2Answer(Filter):
    def __init__(self, filter_column='A2', log_handler=None):
        super().__init__('2.1', 'remove un-qualified row, e.g. no answer for question {}'.format(filter_column), log_handler)
        self.__filter_column = filter_column

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        column_index = q2c_mapping[self.__filter_column][0]
        if incoming['row'][column_index].value is None or incoming['row'][column_index].value == '':
            self._counter += 1
            # logger.debug(self.__str__())
            outgoing.clear()
        else:
            chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterExcludeRecordWithoutSubmitTime(Filter):
    def __init__(self, filter_column='_22', log_handler=None):
        super().__init__('2.2', 'remove un-submitted row, e.g. no submit-time (column {}) exist'.format(filter_column), log_handler)
        self.__filter_column = filter_column

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        column_index = q2c_mapping[self.__filter_column][0]
        if incoming['row'][column_index].value is None or incoming['row'][column_index].value == '':
            self._counter += 1
            # logger.debug(self.__str__())
            outgoing.clear()
        else:
            chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterRinseIrrelevantAnswers(Filter):
    def __init__(self, id, irrelevant_question_rules, log_handler=None):
        super().__init__(id, 'replace non-relevance answers(cell) with NaN against question-relevance rules', log_handler)
        self.__irrelevant_question_rules = irrelevant_question_rules

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        for rule in self.__irrelevant_question_rules:
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

            if flag:
                for action_id in rule[RINSE_RULE_KEY_ACTION]:
                    for action_index in q2c_mapping[action_id]:
                        if outgoing[action_index] is not None:
                            self._counter += 1
                            outgoing[action_index] = None

            chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterRinseNcOptionValues(Filter):
    def __init__(self, filter_columns=('H5-L', 'H6-H'), log_handler=None):
        super().__init__('4', 'replace values like "无法评价", "以上均不需要改进" with NaN', log_handler)
        self.__filter_columns = filter_columns
        self._counter = [0, 0, 0]

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):

        for idx in range(0, outgoing.__len__()):
            if outgoing[idx] in NC_OPTION_FILTER_LIST:
                outgoing[idx] = None
                self._counter[0] += 1

        idx = 1
        for filter_column in self.__filter_columns:
            column_index = q2c_mapping[filter_column][0]
            if outgoing[column_index] is not None:
                # self._debug_info.append(outgoing[column_index])
                outgoing[column_index] = None
                self._counter[idx] += 1
            idx += 1

        chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterRinseInvalidAnswers(Filter):
    def __init__(self, filter_column='G1', log_handler=None):
        super().__init__('5', 'replace invalid answers(cell) with NaN', log_handler)
        self.__filter_column = filter_column

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        for column_index in q2c_mapping[self.__filter_column]:
            if outgoing[column_index] in G1_OPTION_FILTER_LIST:
                outgoing[column_index] = None
                self._counter += 1

        chain.do_filter(incoming, outgoing, q2c_mapping)


class FilterRinseUnusualSalaryValues(Filter):
    def __init__(self, salary_value_collector, filter_column='B6', log_handler=None):
        super().__init__('6', 'rinse salary < 1000, top 0.3%, ABS(diff of MEAN) > 4 * STDEV', log_handler)
        self.__salary_value_collector = salary_value_collector
        self.__filter_column = filter_column
        self._counter = [0, 0, 0]
        self._debug_info = [[], [], []]

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        # logger.info(self.__str__())

        lower_limit = self.__salary_value_collector.get_lower_limit()
        higher_limit = self.__salary_value_collector.get_higher_limit()
        mean = self.__salary_value_collector.get_mean()
        # stdev = self.__salary_value_collector.get_stdev()
        stdev_4 = self.__salary_value_collector.get_stdev_4()

        column_index = q2c_mapping[self.__filter_column][0]
        cell_value = outgoing[column_index]
        if cell_value is not None:
            salary_value = int(cell_value)
            if salary_value < lower_limit:
                self._counter[0] += 1
                self._debug_info[0].append(salary_value)
                # logger.debug('>> salary {} rinsed by lower limit: {}'.format(outgoing[column_index], lower_limit))
                outgoing[column_index] = None
            if salary_value >= higher_limit:
                self._counter[1] += 1
                self._debug_info[1].append(salary_value)
                # logger.debug('>> salary {} rinsed by higher limit: {}, top_n = {}'
                #              .format(outgoing[column_index], higher_limit, self.__salary_value_collector.get_top_n()))
                outgoing[column_index] = None
            elif abs(salary_value - mean) > stdev_4:
                self._counter[2] += 1
                self._debug_info[2].append(salary_value)
                # logger.debug('>> salary {} rinsed by ABS(diff of MEAN) = {} > 4 * STDEV = {}'
                #              .format(outgoing[column_index], abs(salary_value - mean), stdev_4))
                outgoing[column_index] = None

        chain.do_filter(incoming, outgoing, q2c_mapping)

