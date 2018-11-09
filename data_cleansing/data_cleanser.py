#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""data_cleanser.py"""

__author__ = 'Gary.Z'

import sys

from data_cleansing.utils import *
from data_cleansing.clock import *

logger = get_logger(__name__)


class DataCleanser:
    def __init__(self, work_sheet):
        self._work_sheet = work_sheet
        self._trace_mode = False
        self._question_to_column_mapping = {}
        self._excel_column_indexes = generate_excel_column_indexes(iter_cnt=2)

    @property
    def trace_mode(self):
        return self._trace_mode

    @trace_mode.setter
    def trace_mode(self, enabled):
        self._trace_mode = enabled

    def set_sheet_name(self, name):
        self._work_sheet.title = name

    @clocking
    def validate_data_dimensions(self):
        """rule 0: data dimension checking: row >=3 and col >= 231 """
        logger.info('rule 0: validating data dimensions, cols: {}, rows: {}'.format(self._work_sheet.max_column, self._work_sheet.max_row))
        if self._work_sheet.max_column < 231:
            raise Exception("column count must >= 231")
        if self._work_sheet.max_row < 3:
            raise Exception("row count must >= 3")

    @clocking
    def remove_unnecessary_headers(self, start_row=1, row_count=2):
        """rule 0: remove row 1~2: include question description and option description"""
        logger.info('rule 0: removing unnecessary header rows start at {}, count 2'.format(HEADER_ROW_INDEX + 1))
        self._work_sheet.delete_rows(HEADER_ROW_INDEX + start_row, row_count)
        logger.debug('>> current total rows: {}'.format(self._work_sheet.max_row))

    @clocking
    def reset_column_names(self):
        """rule 0: set student info column name with _1~_N, set rest columns follow predefined rules, e.g. A1-A"""
        logger.info('rule 0: batch reset column names with standard codes')

        # Set question-answers column headers
        answer_column = False
        flag1 = False
        flag2 = False
        header_cells = self._work_sheet[HEADER_ROW_INDEX]
        for i in range(0, header_cells.__len__() - 1):
            header_name = header_cells[i].value

            if not answer_column:
                if header_name is None or header_name == '':
                    header_name = '_' + str(i+1)
                    header_cells[i].value = header_name
                    continue

                if not answer_column and header_name == 'A1':
                    answer_column = True
                    if i < BASE_INFO_COLS_MIN:
                        raise Exception("base info columns must >= 23, current: {}".format(i))

            next_header_name = header_cells[i + 1].value

            if header_name is not None and next_header_name is None:
                flag2 = True
                prefix = header_name
                option = 0

            if header_name is None and next_header_name is not None:
                flag1 = True

            if flag2:
                new_header_name = '{}-{}'.format(prefix, self._excel_column_indexes[option])
                option += 1
                header_cells[i].value = new_header_name

            if flag1:
                flag1 = False
                flag2 = False
                prefix = ''
                option = 1

        self._question_to_column_mapping = build_question_to_column_mapping(self._work_sheet, self._excel_column_indexes)

    @clocking
    def reset_emplty_values_with_na(self):
        """rule 0: replace empty values with NaN """
        logger.info('rule 0: replace empty values with NaN ')
        i = 0
        for row in self._work_sheet.rows:
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
    def filter_records_with_degree(self, degree):
        """rule 0: filter records with degree"""
        logger.info('rule 0: filter records with degree: {}'.format(degree))
        # find them
        remove_list = query_row_indexes_by_column_filter(self._work_sheet, self._question_to_column_mapping['_12'][0],
                                                         lambda val: (val != degree))
        # remove them
        remove_rows_by_index_list(self._work_sheet, remove_list, "0", sys._getframe().f_code.co_name, self._trace_mode)
        logger.debug('>> current total rows: {}'.format(self._work_sheet.max_row))

    @clocking
    def apply_rule_set(self, rules):
        for rule in rules:
            rule.apply(self._work_sheet, self._question_to_column_mapping)
        pass

