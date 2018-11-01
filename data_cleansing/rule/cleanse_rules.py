#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cleanse_rules.py"""

__author__ = 'Gary.Z'

import sys
import numpy as np

from data_cleansing.rule.abstract_rule import *
from data_cleansing.utils import *
from data_cleansing.clock import *

logger = get_logger(__name__)


class RuleRemoveTestRecords(CleanseRule):
    def __init__(self):
        super().__init__('1', 'remove test data, e.g. column 14(专业名称) with value {}'.format(MAJOR_FILTER_LIST))

    @clocking
    def apply(self, work_sheet, question_to_column_mapping, trace_mode=False):
        logger.info(self.__str__())
        # find them
        remove_list = query_row_indexes_by_column_filter(work_sheet, question_to_column_mapping['_13'][0],
                                                         lambda val: val in MAJOR_FILTER_LIST)
        # remove them
        remove_rows_by_index_list(work_sheet, remove_list, self.id, sys._getframe().f_code.co_name, trace_mode)
        logger.debug('>> current total rows: {}'.format(work_sheet.max_row))


class RuleRemoveRecordsWithoutA2Answer(CleanseRule):
    def __init__(self):
        super().__init__('2.1', 'remove un-qualified row, e.g. no answer for question A2')

    @clocking
    def apply(self, work_sheet, question_to_column_mapping, trace_mode=False):
        logger.info(self.__str__())
        # find them
        remove_list = query_row_indexes_by_column_filter(work_sheet, question_to_column_mapping['A2'][0],
                                                         lambda val: (val is None or val == ''))
        # remove them
        remove_rows_by_index_list(work_sheet, remove_list, self.id, sys._getframe().f_code.co_name, trace_mode)
        logger.debug('>> current total rows: {}'.format(work_sheet.max_row))


class RuleRemoveRecordsWithoutSubmitTime(CleanseRule):
    def __init__(self):
        super().__init__('2.2', 'remove un-submitted row, e.g. no submit-time exist')

    @clocking
    def apply(self, work_sheet, question_to_column_mapping, trace_mode=False):
        logger.info(self.__str__())
        # find them
        remove_list = query_row_indexes_by_column_filter(work_sheet, question_to_column_mapping['_21'][0],
                                                         lambda val: (val is None or val == ''))
        # remove them
        remove_rows_by_index_list(work_sheet, remove_list, self.id, sys._getframe().f_code.co_name, trace_mode)
        logger.debug('>> current total rows: {}'.format(work_sheet.max_row))


class RuleRinseIrrelevantAnswers(CleanseRule):
    def __init__(self, id, irrelevant_question_rules):
        super().__init__(id, 'replace non-relevance answers(cell) with NaN against question-relevance rules')
        self.__irrelevant_question_rules = irrelevant_question_rules

    @clocking
    def apply(self, work_sheet, question_to_column_mapping, trace_mode=False):
        logger.info(self.__str__())
        for rule in self.__irrelevant_question_rules:
            logger.info('apply rule: {}'.format(rule))
            question_index = question_to_column_mapping[rule[RINSE_RULE_KEY_QUESTION]][0]
            j = 0
            for q_cell in work_sheet[question_index]:
                if q_cell.row <= HEADER_ROW_INDEX:
                    continue

                answer = q_cell.value
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
                    i = 0
                    for question_id in rule[RINSE_RULE_KEY_ACTION]:
                        for col_index in question_to_column_mapping[question_id]:
                            coordinate = '{}{}'.format(col_index, q_cell.row)
                            if work_sheet[coordinate].value is not None:
                                # logger.info('>> rinsing {}({}) as NaN'.format(coordinate[coordinate].value))
                                if trace_mode:
                                    add_tracing_comment(work_sheet[coordinate], self.id, sys._getframe().f_code.co_name, rule)
                                else:
                                    work_sheet[coordinate].value = None
                                i += 1
                            # break
                    j += i
            logger.info('>> {} cells rinsed'.format(j))


class RuleRinseNcOptionValues(CleanseRule):
    def __init__(self):
        super().__init__('4', 'replace values like "无法评价", "以上均不需要改进" with NaN')

    @clocking
    def apply(self, work_sheet, question_to_column_mapping, trace_mode=False):
        logger.info(self.__str__())
        i = 0
        for row in work_sheet.rows:
            for cell in row:
                if cell.value in NC_OPTION_FILTER_LIST:
                    if cell.value is not None:
                        if trace_mode:
                            add_tracing_comment(cell, '5', sys._getframe().f_code.co_name)
                        else:
                            cell.value = None
                        i += 1
        logger.info('>> {} cells rinsed'.format(i))

        rinse_values_by_column_rowindex(work_sheet, question_to_column_mapping['H5-L'][0], range(HEADER_ROW_INDEX + 1, work_sheet.max_row + 1),
                                        self.id, sys._getframe().f_code.co_name, trace_mode)
        rinse_values_by_column_rowindex(work_sheet, question_to_column_mapping['H6-H'][0], range(HEADER_ROW_INDEX + 1, work_sheet.max_row + 1),
                                        self.id, sys._getframe().f_code.co_name, trace_mode)


class RuleRinseInvalidAnswers(CleanseRule):
    def __init__(self):
        super().__init__('5', 'replace invalid answers(cell) with NaN')

    @clocking
    def apply(self, work_sheet, question_to_column_mapping, trace_mode=False):
        logger.info(self.__str__())
        # find them
        rinse_list = query_row_indexes_by_column_filter(work_sheet, question_to_column_mapping['G1'][0],
                                                        lambda val: val in G1_OPTION_FILTER_LIST)
        # remove them
        rinse_values_by_column_rowindex(work_sheet, question_to_column_mapping['G1'][0], rinse_list,
                                        self.id, sys._getframe().f_code.co_name, trace_mode)
        rinse_values_by_column_rowindex(work_sheet, question_to_column_mapping['G1'][1], rinse_list,
                                        self.id, sys._getframe().f_code.co_name, trace_mode)


class RuleRinseUnusualSalaryValues(CleanseRule):
    def __init__(self):
        super().__init__('6', 'rinse < 1000, top 0.3%, ABS(diff of MEAN) > 4 * STDEV')

    @clocking
    def apply(self, work_sheet, question_to_column_mapping, trace_mode=False):
        logger.info(self.__str__())
        salary_cell_range = '{}{}:{}{}'.format(question_to_column_mapping['B6'][0], HEADER_ROW_INDEX + 1,
                                               question_to_column_mapping['B6'][0], work_sheet.max_row);
        sorted_salary_list = []
        for row in work_sheet[salary_cell_range]:
            if row[0].value is not None and row[0].value != '':
                sorted_salary_list.append([row[0].coordinate, int(row[0].value)])
        sorted_salary_list = sorted(sorted_salary_list, key=lambda kv: kv[1], reverse=True)
        logger.debug('>> current total rows: {}'.format(work_sheet.max_row))
        total = sorted_salary_list.__len__()
        logger.debug('>> current valid salary values: {}'.format(total))

        logger.info('>> {}.1 rinsing salary < 1000'.format(self.id))
        n = 0
        _debug_info_ = []
        sorted_salary_list_copy = list(sorted_salary_list)
        for i in range(0, sorted_salary_list_copy.__len__())[::-1]:
            coordinate = sorted_salary_list_copy[i][0]
            value = sorted_salary_list_copy[i][1]
            if value < SALARY_FILTER_LOWER_LIMIT:
                _debug_info_.append(value)
                work_sheet[coordinate].value = None
                sorted_salary_list.pop(i)
                n += 1
            else:
                break
        logger.info('>> {} cells rinsed from {}'.format(n, total))
        logger.debug('>> {}'.format(_debug_info_))
        total -= n
        logger.debug('>> current valid salary values: {}'.format(total))

        logger.info('>> {}.2 rinsing top N salary'.format(self.id))
        top_n = round(sorted_salary_list.__len__() * SALARY_FILTER_TOP_RATIO)
        logger.info('>> top N = {}'.format(top_n))
        if top_n >= 1:
            top_n_list = []
            for n in range(0, top_n):
                top_n_list.append(sorted_salary_list[n][1])

            n = 0
            _debug_info_ = []
            sorted_salary_list_copy = list(sorted_salary_list)
            for i in range(0, sorted_salary_list_copy.__len__()):
                coordinate = sorted_salary_list_copy[i][0]
                value = sorted_salary_list_copy[i][1]
                if value < top_n_list[top_n_list.__len__() - 1]:
                    break
                if value in top_n_list:
                    _debug_info_.append(value)
                    if trace_mode:
                        add_tracing_comment(work_sheet[coordinate], '{}.2'.format(self.id), sys._getframe().f_code.co_name)
                    else:
                        work_sheet[coordinate] = None
                    sorted_salary_list.pop(0)
                    n += 1
            logger.info('>> {} cells rinsed from {}'.format(n, total))
            logger.debug('>> {}'.format(_debug_info_))
            total -= n
            logger.debug('>> current valid salary values: {}'.format(total))
        else:
            logger.info('>> no cell need to be rinsed')

        logger.info('>> {}.3 rinsing ABS(salary - MEAN) > 4 * STDEV'.format(self.id))
        np_salary_list = np.array(list(map(lambda x: x[1], sorted_salary_list)), dtype=np.int64)
        salary_mean = np_salary_list.mean()
        logger.info('>> MEAN = {}'.format(salary_mean))
        salary_stdev = np_salary_list.std()
        logger.info('>> STDEV = {}'.format(salary_stdev))
        salary_stdev_4 = salary_stdev * 4
        logger.info('>> STDEV * 4 = {}'.format(salary_stdev_4))
        n = 0
        _debug_info_ = []
        sorted_salary_list_copy = list(sorted_salary_list)
        for i in range(0, sorted_salary_list_copy.__len__()):
            coordinate = sorted_salary_list_copy[i][0]
            value = sorted_salary_list_copy[i][1]
            if abs(value - salary_mean) > salary_stdev_4:
                _debug_info_.append(value)
                if trace_mode:
                    add_tracing_comment(work_sheet[coordinate], '{}.3'.format(self.id), sys._getframe().f_code.co_name)
                else:
                    work_sheet[coordinate] = None
                sorted_salary_list.pop(0)
                n += 1
            else:
                break
        logger.info('>> {} cells rinsed from {}'.format(n, total))
        logger.debug('>> {}'.format(_debug_info_))
        logger.debug('>> {}'.format(list(map(lambda x: abs(x - salary_mean), _debug_info_))))
        total -= n
        logger.debug('>> current valid salary values: {}'.format(total))
