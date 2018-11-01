#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""data_cleanser.py"""

__author__ = 'Gary.Z'

import sys
import numpy as np

from data_cleansing.utils import *
from data_cleansing.clock import *

logger = get_logger(__name__)


class DataCleanser:
    def __init__(self, work_sheet):
        self.__work_sheet = work_sheet
        self.__trace_mode = False
        self.__question_to_column_mapping = {}
        self.__excel_column_indexes = generate_excel_column_indexes(iter_cnt=2)

    @property
    def trace_mode(self):
        return self.__trace_mode;

    @trace_mode.setter
    def trace_mode(self, enabled):
        self.__trace_mode = enabled

    @clocking
    def validate_data_dimensions(self):
        """rule 0: data dimension checking: row >=3 and col >= 231 """
        logger.info('rule 0: validating data dimensions, cols: {}, rows: {}'.format(self.__work_sheet.max_column, self.__work_sheet.max_row))
        if self.__work_sheet.max_column < 231:
            raise Exception("column count must >= 231")
        if self.__work_sheet.max_row < 3:
            raise Exception("row count must >= 3")

    @clocking
    def remove_unnecessary_headers(self, start_row=1, row_count=2):
        """rule 0: remove row 1~2: include question description and option description"""
        logger.info('rule 0: removing unnecessary header rows start at {}, count 2'.format(HEADER_ROW_INDEX + 1))
        self.__work_sheet.delete_rows(HEADER_ROW_INDEX + start_row, row_count)
        logger.debug('>> current total rows: {}'.format(self.__work_sheet.max_row))

    @clocking
    def reset_column_names(self):
        """rule 0: set student info column name with _1~_N, set rest columns follow predefined rules, e.g. A1-A"""
        logger.info('rule 0: batch reset column names with standard codes')

        # Set question-answers column headers
        answer_column = False
        flag1 = False
        flag2 = False
        header_cells = self.__work_sheet[HEADER_ROW_INDEX]
        for i in range(0, header_cells.__len__() - 1):
            header_name = header_cells[i].value

            if not answer_column:
                if header_name is None or header_name == '':
                    header_name = '_' + str(i)
                    header_cells[i].value = header_name
                    continue

                if not answer_column and header_name == 'A1':
                    answer_column = True

            next_header_name = header_cells[i + 1].value

            if header_name is not None and next_header_name is None:
                flag2 = True
                prefix = header_name
                option = 0

            if header_name is None and next_header_name is not None:
                flag1 = True

            if flag2:
                new_header_name = '{}-{}'.format(prefix, self.__excel_column_indexes[option])
                option += 1
                header_cells[i].value = new_header_name

            if flag1:
                flag1 = False
                flag2 = False
                prefix = ''
                option = 1

        self.__question_to_column_mapping = build_question_to_column_mapping(self.__work_sheet, self.__excel_column_indexes)

    def set_sheet_name(self, name):
        self.__work_sheet.title = name

    @clocking
    def reset_emplty_values_with_na(self):
        """rule 0: replace empty values with NaN """
        logger.info('rule 0: replace empty values with NaN ')
        i = 0
        for row in self.__work_sheet.rows:
            for cell in row:
                if cell.value == '':
                    cell.value = None
                    i += 1
        logger.info('>> {} cells replaced'.format(i))

    # @clocking
    # def clear_all_cells_bgcolor(self):
    #     """rule 0: clear all cells' BG color """
    #     logger.info('rule 0: clear all cells\' BG color ')
    #     for row in self.__work_sheet['{}:{}'.format('A', self.__question_to_excel_column_map['I2-22-68'][0])]:
    #         for cell in row:
    #             cell.fill = xl.styles.PatternFill(None)

    @clocking
    def remove_fake_records(self):
        """rule 1: remove fake data, e.g. column 14(专业名称) with value "测试专业" """
        logger.info('rule 1: removing rows which major in {}'.format(MAJOR_FILTER_LIST))
        # find them
        remove_list = query_row_indexes_by_column_filter(self.__work_sheet, self.__question_to_column_mapping['_13'][0], lambda val: val in MAJOR_FILTER_LIST)
        # remove them
        remove_rows_by_index_list(self.__work_sheet, remove_list, '1', sys._getframe().f_code.co_name, self.__trace_mode)
        logger.debug('>> current total rows: {}'.format(self.__work_sheet.max_row))

    @clocking
    def remove_unqualified_records(self):
        """rule 2.1: remove un-qualified row, e.g. no answer for question A2"""
        logger.info('rule 2.1: removing rows which have no A2 answers')
        # find them
        remove_list = query_row_indexes_by_column_filter(self.__work_sheet, self.__question_to_column_mapping['A2'][0],
                                                         lambda val: (val is None or val == ''))
        # remove them
        remove_rows_by_index_list(self.__work_sheet, remove_list, '2.1', sys._getframe().f_code.co_name, self.__trace_mode)
        logger.debug('>> current total rows: {}'.format(self.__work_sheet.max_row))

    @clocking
    def remove_unsubmitted_records(self):
        """rule 2.2: remove un-submitted row, e.g. no submit-time exist"""
        logger.info('rule 2.2: removing rows which have no submit time')
        # find them
        remove_list = query_row_indexes_by_column_filter(self.__work_sheet, self.__question_to_column_mapping['_21'][0],
                                                         lambda val: (val is None or val == ''))
        # remove them
        remove_rows_by_index_list(self.__work_sheet, remove_list, '2.2', sys._getframe().f_code.co_name, self.__trace_mode)
        logger.debug('>> current total rows: {}'.format(self.__work_sheet.max_row))

    @clocking
    def rinse_irrelevant_answers(self, irrelevant_question_rules, rule_no):
        """rule 4/8: replace non-relevance answers(cell) with NaN against question-relevance rules"""
        logger.info('rule {}: replace non-relevance answers(cell) with NaN against question-relevance rules'.format(rule_no))
        for rule in irrelevant_question_rules:
            logger.info('apply rule: {}'.format(rule))
            question_index = self.__question_to_column_mapping[rule[RINSE_RULE_KEY_QUESTION]][0]
            j = 0
            for q_cell in self.__work_sheet[question_index]:
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
                        for col_index in self.__question_to_column_mapping[question_id]:
                            coordinate = '{}{}'.format(col_index, q_cell.row)
                            if self.__work_sheet[coordinate].value is not None:
                                # logger.info('>> rinsing {}({}) as NaN'.format(coordinate[coordinate].value))
                                if self.__trace_mode:
                                    add_tracing_comment(self.__work_sheet[coordinate], rule_no, sys._getframe().f_code.co_name, rule)
                                else:
                                    self.__work_sheet[coordinate].value = None
                                i += 1
                            # break
                    j += i
            logger.info('>> {} cells rinsed'.format(j))

    @clocking
    def rinse_nc_option_values(self):
        """rule 5: replace values like "无法评价", "以上均不需要改进" with NaN """
        logger.info('rule 5: rinse answers which in {} into NaN'.format(NC_OPTION_FILTER_LIST))
        i = 0
        for row in self.__work_sheet.rows:
            for cell in row:
                if cell.value in NC_OPTION_FILTER_LIST:
                    if cell.value is not None:
                        if self.__trace_mode:
                            add_tracing_comment(cell, '5', sys._getframe().f_code.co_name)
                        else:
                            cell.value = None
                        i += 1
        logger.info('>> {} cells rinsed'.format(i))

        rinse_values_by_column_rowindex(self.__work_sheet, self.__question_to_column_mapping['H5-L'][0], range(HEADER_ROW_INDEX + 1, self.__work_sheet.max_row + 1),
                                        '5', sys._getframe().f_code.co_name, self.__trace_mode)
        rinse_values_by_column_rowindex(self.__work_sheet, self.__question_to_column_mapping['H6-H'][0], range(HEADER_ROW_INDEX + 1, self.__work_sheet.max_row + 1),
                                        '5', sys._getframe().f_code.co_name, self.__trace_mode)

    @clocking
    def rinse_invalid_answers(self):
        """rule 6: replace invalid answers(cell) with NaN"""
        logger.info('rule 6: rinse G1 answers which in {}'.format(G1_OPTION_FILTER_LIST))
        # find them
        rinse_list = query_row_indexes_by_column_filter(self.__work_sheet, self.__question_to_column_mapping['G1'][0],
                                                        lambda val: val in G1_OPTION_FILTER_LIST)
        # remove them
        rinse_values_by_column_rowindex(self.__work_sheet, self.__question_to_column_mapping['G1'][0], rinse_list,
                                        '6', sys._getframe().f_code.co_name, self.__trace_mode)
        rinse_values_by_column_rowindex(self.__work_sheet, self.__question_to_column_mapping['G1'][1], rinse_list,
                                        '6', sys._getframe().f_code.co_name, self.__trace_mode)

    @clocking
    def rinse_unusual_salary_values(self):
        """rule 7: remove < 1000, top 0.3%, ABS(diff of MEAN) > 4 * STDEV """
        logger.info('rule 7: remove < 1000, top 0.3%, ABS(diff of MEAN) > 4 * STDEV ')

        salary_cell_range = '{}{}:{}{}'.format(self.__question_to_column_mapping['B6'][0], 2,
                                               self.__question_to_column_mapping['B6'][0], self.__work_sheet.max_row);
        sorted_salary_list = []
        for row in self.__work_sheet[salary_cell_range]:
            if row[0].value is not None and row[0].value != '':
                sorted_salary_list.append([row[0].coordinate, int(row[0].value)])
        sorted_salary_list = sorted(sorted_salary_list, key=lambda kv: kv[1], reverse=True)
        logger.debug('>> current total rows: {}'.format(self.__work_sheet.max_row))
        total = sorted_salary_list.__len__()
        logger.debug('>> current valid salary values: {}'.format(total))

        logger.info('>> 7.1 rinsing salary < 1000')
        n = 0
        _debug_info_ = []
        sorted_salary_list_copy = list(sorted_salary_list)
        for i in range(0, sorted_salary_list_copy.__len__())[::-1]:
            coordinate = sorted_salary_list_copy[i][0]
            value = sorted_salary_list_copy[i][1]
            if value < SALARY_FILTER_LOWER_LIMIT:
                _debug_info_.append(value)
                self.__work_sheet[coordinate].value = None
                sorted_salary_list.pop(i)
                n += 1
            else:
                break
        logger.info('>> {} cells rinsed from {}'.format(n, total))
        logger.debug('>> {}'.format(_debug_info_))
        total -= n
        logger.debug('>> current valid salary values: {}'.format(total))

        logger.info('>> 7.2 rinsing top N salary')
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
                    if self.__trace_mode:
                        add_tracing_comment(self.__work_sheet[coordinate], '7.2', sys._getframe().f_code.co_name)
                    else:
                        self.__work_sheet[coordinate] = None
                    sorted_salary_list.pop(0)
                    n += 1
            logger.info('>> {} cells rinsed from {}'.format(n, total))
            logger.debug('>> {}'.format(_debug_info_))
            total -= n
            logger.debug('>> current valid salary values: {}'.format(total))
        else:
            logger.info('>> no cell need to be rinsed')

        logger.info('>> 7.3 rinsing ABS(salary - MEAN) > 4 * STDEV')
        np_salary_list = np.array(list(map(lambda x: x[1], sorted_salary_list)), dtype=int)
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
                if self.__trace_mode:
                    add_tracing_comment(self.__work_sheet[coordinate], '7.3', sys._getframe().f_code.co_name)
                else:
                    self.__work_sheet[coordinate] = None
                sorted_salary_list.pop(0)
                n += 1
            else:
                break
        logger.info('>> {} cells rinsed from {}'.format(n, total))
        logger.debug('>> {}'.format(_debug_info_))
        logger.debug('>> {}'.format(list(map(lambda x: abs(x - salary_mean), _debug_info_))))
        total -= n
        logger.debug('>> current valid salary values: {}'.format(total))

