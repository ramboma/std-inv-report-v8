#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""utils.py"""

__author__ = 'Gary.Z'

# import xlrd
# import xlwt
# import pandas as pd
import openpyxl as xl
import numpy as np
import os
import time, timeit


EXCEL_INDEX_BASE = 1
HEADER_ROW_INDEX = 0 + EXCEL_INDEX_BASE
A1_COLUMN_INDEX = 23 + EXCEL_INDEX_BASE

MAJOR_COLUMN_EXCEL_INDEX = 'N'
SUBMIT_TIME_COLUMN_EXCEL_INDEX = 'V'
H5_COLUMN_EXCEL_INDEX_NC = 'DV'
H6_COLUMN_EXCEL_INDEX_NC = 'ED'

MAJOR_FILTER_LIST = ('测试专业')
NC_OPTION_FILTER_LIST = ('无法评价', '以上均不需要改进')
G1_OPTION_FILTER_LIST = ('国际组织', '军队')

# definition of question code mapping to excel column index
QUESTION_TO_EXCEL_COLUMN_MAP = {
    'A1': ['X', 'Y'],
    'A2': ['Z'],
    'B1': ['AB'],
    'B2': ['AC'],
    'B3': ['AD', 'AE', 'AF'],
    'B4': ['AG', 'AH', 'AI'],
    'B5': ['AJ', 'AK', 'AI'],
    'B6': ['AL'],
    'B7-1': ['AM'],
    'B7-2': ['AN'],
    'B7-3': ['AO'],
    'B7-4': ['AP'],
    'B8': ['AQ'],
    'B9-1': ['AR'],
    'B9-2': ['AS'],
    'B10-1': ['AT'],
    'B10-2': ['AU'],
    'C1': ['AV'],
    'C2': ['AW'],
    'D1': ['AX'],
    'D2': ['AY'],
    'E1': ['AZ'],
    'E2': ['BA'],
    'E3': ['BB'],
    'E4': ['BC'],
    'F1': ['BD'],
    'F2': ['BE'],
    'F3': ['BF'],
    'F4': ['BG'],
    'G1': ['BH', 'BI'],
    'G2': ['BJ'],
    'G3': ['BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ'],
    'G4': ['BR', 'BS', 'BT', 'BU', 'BV', 'BW'],
    'G5': ['BX', 'BY', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CE'],
    'I2-1-A': ['EL'],
    'I2-1-B': ['EM'],
    'I2-1-C': ['EN'],
    'I2-1-D': ['EO'],
    'I2-1-E': ['EP'],
    'I2-1-F': ['EQ'],
    'I2-1-G': ['ER'],
    'I2-1-H': ['ES'],
    'I2-1-I': ['ET'],
    'I2-1-J': ['EU'],
    'I2-1-K': ['EV'],
    'I2-1-L': ['EW'],
    'I2-1-M': ['EX'],
    'I2-1-N': ['EY'],
    'I2-1-O': ['EZ'],
    'I2-1-P': ['FA'],
    'I2-1-Q': ['FB'],
    'I2-1-R': ['FC'],
    'I2-1-S': ['FD'],
    'I2-1-T': ['FE'],
    'I2-1-U': ['FF'],
    'I2-1-V': ['FG'],
    'I2-1-1': ['FH'],
    'I2-1-2': ['FI'],
    'I2-2-3': ['FJ'],
    'I2-2-4': ['FK'],
    'I2-3-5': ['FL'],
    'I2-3-6': ['FM'],
    'I2-4-7': ['FL'],
    'I2-4-8': ['FN'],
    'I2-5-9': ['FO'],
    'I2-5-10': ['FP'],
    'I2-5-11': ['FQ'],
    'I2-5-12': ['FR'],
    'I2-5-13': ['FS'],
    'I2-6-14': ['FT'],
    'I2-6-15': ['FU'],
    'I2-6-16': ['FV'],
    'I2-6-17': ['FW'],
    'I2-6-18': ['FX'],
    'I2-7-19': ['FY'],
    'I2-7-20': ['FZ'],
    'I2-8-21': ['GB'],
    'I2-8-22': ['GC'],
    'I2-9-23': ['GD'],
    'I2-9-24': ['GE'],
    'I2-9-25': ['GF'],
    'I2-10-26': ['GG'],
    'I2-10-27': ['GH'],
    'I2-11-28': ['GI'],
    'I2-11-29': ['GJ'],
    'I2-12-30': ['GK'],
    'I2-12-31': ['GL'],
    'I2-12-32': ['GM'],
    'I2-13-33': ['GN'],
    'I2-13-34': ['GO'],
    'I2-14-35': ['GP'],
    'I2-14-36': ['GQ'],
    'I2-15-37': ['GR'],
    'I2-15-38': ['GS'],
    'I2-15-39': ['GT'],
    'I2-16-40': ['GU'],
    'I2-16-41': ['GV'],
    'I2-16-42': ['GW'],
    'I2-16-43': ['GX'],
    'I2-17-44': ['GY'],
    'I2-17-45': ['GZ'],
    'I2-17-46': ['HA'],
    'I2-17-47': ['HB'],
    'I2-18-48': ['HC'],
    'I2-18-49': ['HD'],
    'I2-18-50': ['HE'],
    'I2-18-51': ['HF'],
    'I2-19-52': ['HG'],
    'I2-19-53': ['HH'],
    'I2-19-54': ['HI'],
    'I2-19-55': ['HJ'],
    'I2-19-56': ['HK'],
    'I2-19-57': ['HL'],
    'I2-20-58': ['HM'],
    'I2-20-59': ['HN'],
    'I2-20-60': ['HO'],
    'I2-20-61': ['HP'],
    'I2-20-62': ['HQ'],
    'I2-20-63': ['HR'],
    'I2-21-64': ['HS'],
    'I2-21-65': ['HT'],
    'I2-22-66': ['HU'],
    'I2-22-67': ['HV'],
    'I2-22-68': ['HW'],
}

RINSE_RULE_KEY_QUESTION = 'question_id'
RINSE_RULE_KEY_ANSWER = 'answer'
RINSE_RULE_KEY_OPERATOR = 'operator'
RINSE_RULE_KEY_ACTION = 'tobe_rinsed_id'
RINSE_RULE_OPERATOR_IN = 'IN'
RINSE_RULE_OPERATOR_NOTIN = 'NOT_IN'
# definition of irrelevant question rinse rule
RINSE_RULE_IRRELEVANT_QUESTIONS = [
    # IF A2 not in (在国内工作, 自由职业) then rinse
    #   B1, B2, B3, B4, B5, B6, B7-1, B7-2, B7-3, B7-4, B8, B9-1, B9-2, B10-1, B10-2, D1, D2
    {RINSE_RULE_KEY_QUESTION: 'A2',
     RINSE_RULE_KEY_ANSWER: ('在国内工作', '自由职业'),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7-1', 'B7-2', 'B7-3', 'B7-4', 'B8',
                  'B9-1', 'B9-2', 'B10-1', 'B10-2', 'D1', 'D2']},
    # IF A2 = 自由职业 then rinse B1,B2,B3,B4, B10-1
    {RINSE_RULE_KEY_QUESTION: 'A2',
     RINSE_RULE_KEY_ANSWER: ('自由职业',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_IN,
     RINSE_RULE_KEY_ACTION: ['B1', 'B2', 'B3', 'B4', 'B10-1']},
    # IF B9-1 not in (比较不相关, 很不相关) then rinse B9-2
    {RINSE_RULE_KEY_QUESTION: 'B9-1',
     RINSE_RULE_KEY_ANSWER: ('比较不相关', '很不相关'),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['B9-2']},
    # IF B10-1 = 0次 then rinse B10-2
    {RINSE_RULE_KEY_QUESTION: 'B10-1',
     RINSE_RULE_KEY_ANSWER: ('0次',),
     RINSE_RULE_KEY_OPERATOR: 'IN',
     RINSE_RULE_KEY_ACTION: ['B10-2']},
    # IF A2 != 未就业 then rinse C1, C2
    {RINSE_RULE_KEY_QUESTION: 'A2',
     RINSE_RULE_KEY_ANSWER: ('未就业',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['C1', 'C2']},
    # IF A2 != 在国内升学 then rinse E1,E2,E3,E4
    {RINSE_RULE_KEY_QUESTION: 'A2',
     RINSE_RULE_KEY_ANSWER: ('在国内升学',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['E1', 'E2', 'E3', 'E4']},
    # IF E3 not in (比较不相关, 很不相关) then rinse E4
    {RINSE_RULE_KEY_QUESTION: 'E3',
     RINSE_RULE_KEY_ANSWER: ('比较不相关', '很不相关'),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['E4']},
    # IF A2 != 出国/出境 then rinse F1, F2, F3, F4
    {RINSE_RULE_KEY_QUESTION: 'A2',
     RINSE_RULE_KEY_ANSWER: ('出国/出境',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['F1', 'F2', 'F3', 'F4']},
    # IF F1 != 求学 then rinse F2, F3
    {RINSE_RULE_KEY_QUESTION: 'F1',
     RINSE_RULE_KEY_ANSWER: ('求学',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['F2', 'F3']},
    # IF F3 not in (比较不相关, 很不相关) then rinse F4
    {RINSE_RULE_KEY_QUESTION: 'F3',
     RINSE_RULE_KEY_ANSWER: ('比较不相关', '很不相关'),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['F4']},
    # IF A2 != 自主创业 then rinse G1, G2, G3, G4, G5
    {RINSE_RULE_KEY_QUESTION: 'A2',
     RINSE_RULE_KEY_ANSWER: ('自主创业',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['G1', 'G2', 'G3', 'G4', 'G5']},
    # I2-1 rules, 22 rules in total
    {RINSE_RULE_KEY_QUESTION: 'I2-1-A',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-1-1', 'I2-1-2']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-B',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-3', 'I2-2-4']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-C',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-3-5', 'I2-3-6']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-D',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-4-7', 'I2-4-8']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-E',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-5-9', 'I2-5-10', 'I2-5-11', 'I2-5-12', 'I2-5-13']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-F',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-6-14', 'I2-6-15', 'I2-6-16', 'I2-6-17', 'I2-6-18']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-G',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-7-19', 'I2-7-20']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-H',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-8-21', 'I2-8-22']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-I',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-9-23', 'I2-9-24', 'I2-9-25']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-J',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-10-26', 'I2-10-27']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-K',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-11-28', 'I2-11-29']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-L',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-12-30', 'I2-12-31', 'I2-12-32']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-M',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-13-33', 'I2-13-34']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-N',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-14-35', 'I2-14-36']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-O',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-15-37', 'I2-15-38', 'I2-15-39']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-P',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-16-40', 'I2-16-41', 'I2-16-43', 'I2-16-43']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-Q',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-17-44', 'I2-17-45', 'I2-17-46', 'I2-17-47']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-R',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-18-48', 'I2-18-49', 'I2-18-50', 'I2-18-51']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-S',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-19-52', 'I2-19-53', 'I2-19-54', 'I2-19-55', 'I2-19-56', 'I2-19-57']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-T',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-20-58', 'I2-20-59', 'I2-20-60', 'I2-20-61', 'I2-20-62', 'I2-20-63']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-U',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-21-64', 'I2-21-65']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-V',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-22-66', 'I2-22-67', 'I2-22-68']},
]


def clock(func):
    def clocked(*args):
        t0 = timeit.default_timer()
        result = func(*args)
        elapsed = timeit.default_timer() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        # print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        print('=> [%0.2fs]' % elapsed)
        return result
    return clocked


@clock
def validate_data_dimensions(st):
    """rule 0: data dimension checking: row >=3 and col >= 231 """
    print('rule 0: validating data dimensions, cols: {}, rows: {}'.format(st.max_column, st.max_row))
    if st.max_column < 231:
        raise Exception("column count must >= 231")
    if st.max_row < 3:
        raise Exception("row count must >= 3")


@clock
def remove_unnecessary_headers(st):
    """rule 0: remove row 1~2: include question description and option description"""
    print('rule 0: removing unnecessary header rows start at {}, count 2'.format(HEADER_ROW_INDEX + 1))
    st.delete_rows(HEADER_ROW_INDEX + 1, 2)


@clock
def batch_reset_column_names(st):
    """rule 0: set first 23 column name set with _1~_23, rest set follow predefined rules, e.g. A1-A"""
    print('rule 0: batch reset column names with standard codes')
    BOUNDARY_0 = 0 + EXCEL_INDEX_BASE
    BOUNDARY_1 = A1_COLUMN_INDEX
    BOUNDARY_2 = (st.max_column - 1) + EXCEL_INDEX_BASE

    # Set base info column headers
    for i in range(BOUNDARY_0, BOUNDARY_1):
        value = '_' + str(i)
        st.cell(HEADER_ROW_INDEX, i, value)
        # print('write: "' + value + '"')

    # Set question-answers column headers
    value = ''
    next_value = ''
    flag1 = False
    flag2 = False
    for i in range(BOUNDARY_1, BOUNDARY_2):  # loop from index 23 to last - 1
        value = st.cell(HEADER_ROW_INDEX, i).value
        next_value = st.cell(HEADER_ROW_INDEX, i + 1).value

        if value is not None and next_value is None:
            flag2 = True
            prefix = value
            option = 'A'

        if value is None and next_value is not None:
            flag1 = True

        if flag2:
            value_to_write = prefix + '-' + option
            option = chr(ord(option) + 1)
            st.cell(HEADER_ROW_INDEX, i, value_to_write)
            # print('write: "' + value_to_write + '"')
        # else:
        #     value_to_write = value

        if flag1:
            flag1 = False
            flag2 = False
            prefix = ''
            option = 'A'

    st.title = "cleaned"


@clock
def reset_emplty_values_with_na(st):
    """rule 0: replace empty values with NaN """
    print('rule 0: replace empty values with NaN ')
    i = 0
    # for row in range(HEADER_ROW_INDEX + 1, st.max_row + 1):
    #     for col in range(A1_COLUMN_INDEX, st.max_column + 1):
    #         if st.cell(row, col).value == '':
    #             cell = st.cell(row, col, None)
    #             # print('rinse cell: {} - {}'.format(cell.coordinate, cell.value))
    #             i += 1
    for row in st['{}:{}'.format(QUESTION_TO_EXCEL_COLUMN_MAP['A1'][0], QUESTION_TO_EXCEL_COLUMN_MAP['I2-22-68'][0])]:
        for cell in row:
            if cell.value == '':
                cell.value = None
                i += 1
    print('>> {} cells replaced'.format(i))


def query_row_indexes_by_column_filter(st, xl_col, cb_filter):
    idx_list = []
    for cell in st[xl_col]:
        if cell.row <= HEADER_ROW_INDEX:
            continue
        # print("cell: {}".format(cell.value))
        if cb_filter(cell.value):
            idx_list.append(cell.row)
    # print(idx_list)
    return idx_list


def remove_rows_by_index_list(st, index_list):
    for i in range(0, index_list.__len__())[::-1]:
        st.delete_rows(index_list[i])
        # print('remove row: {}'.format(index_list[i]))
    print('>> {} rows removed'.format(index_list.__len__()))


@clock
def remove_fake_records(st):
    """rule 1: remove fake data, e.g. column 14(专业名称) with value "测试专业" """
    print('rule 1: removing rows which major in {}'.format(MAJOR_FILTER_LIST))
    # find them
    remove_list = query_row_indexes_by_column_filter(st, MAJOR_COLUMN_EXCEL_INDEX, lambda val: val in MAJOR_FILTER_LIST)
    # remove them
    remove_rows_by_index_list(st, remove_list)


@clock
def remove_unsubmitted_records(st):
    """rule 2, 3: remove un-submitted row, e.g. no submit-time exist"""
    print('rule 2, 3: removing rows which have no submit time')
    # find them
    remove_list = query_row_indexes_by_column_filter(st, SUBMIT_TIME_COLUMN_EXCEL_INDEX,
                                                     lambda val: (val is None or val == ''))
    # remove them
    remove_rows_by_index_list(st, remove_list)


@clock
def remove_unqualified_records(st):
    """rule 2, 3: remove un-qualified row, e.g. no answer for question A2"""
    print('rule 2, 3: removing rows which have no A2 answers')
    # find them
    remove_list = query_row_indexes_by_column_filter(st, QUESTION_TO_EXCEL_COLUMN_MAP['A2'][0],
                                                     lambda val: (val is None or val == ''))
    # remove them
    remove_rows_by_index_list(st, remove_list)


@clock
def rinse_irrelevant_answers(st):
    """rule 4: replace non-relevance answers(cell) with NaN against question-relevance rules"""
    print('rule 4: replace non-relevance answers(cell) with NaN against question-relevance rules')
    for rule in RINSE_RULE_IRRELEVANT_QUESTIONS:
        print('apply rule: {}'.format(rule))
        question_index = QUESTION_TO_EXCEL_COLUMN_MAP[rule[RINSE_RULE_KEY_QUESTION]][0]
        j = 0
        for q_cell in st[question_index]:
            if q_cell.row <= HEADER_ROW_INDEX:
                continue

            answer = q_cell.value
            if answer is None:
                answer = '';

            flag = False

            if rule[RINSE_RULE_KEY_OPERATOR] == RINSE_RULE_OPERATOR_IN:
                flag = answer in rule[RINSE_RULE_KEY_ANSWER]
            elif rule[RINSE_RULE_KEY_OPERATOR] == RINSE_RULE_OPERATOR_NOTIN:
                flag = answer not in rule[RINSE_RULE_KEY_ANSWER]
            else:
                # print(">> no applicable operator: {}".format(rule[KEY_OPERATOR]))
                pass

            if flag:
                # print('>> condition meet: {} answer({}) {} {}, rinsing following question/answers: {}'.format(
                #       rule[KEY_QUESTION], answer, rule[KEY_OPERATOR], rule[KEY_ANSWER], rule[KEY_ACTION]))
                i = 0
                for question_id in rule[RINSE_RULE_KEY_ACTION]:
                    for col_index in QUESTION_TO_EXCEL_COLUMN_MAP[question_id]:
                        coordinate = '{}{}'.format(col_index, q_cell.row)
                        if st[coordinate].value is not None:
                            # print('>> rinsing {}({}) as NaN'.format(coordinate, st[coordinate].value))
                            st[coordinate].value = None
                            i += 1
                        # break
                j += i
                # print('{} cells rinsed'.format(i))
            else:
                # print('>> condition not meet: {} answer({}) {} {}'.format(
                #     rule[KEY_QUESTION], q_cell.value, rule[KEY_OPERATOR], rule[KEY_ANSWER]))
                pass
            # break
        print('>> {} cells rinsed'.format(j))


@clock
def rinse_nc_option_values(st):
    """rule 5: replace values like "无法评价", "以上均不需要改进" with NaN """
    print('rule 5: rinse answers which in {} into NaN'.format(NC_OPTION_FILTER_LIST))
    i = 0
    # for row in range(HEADER_ROW_INDEX + 1, st.max_row + 1):
    #     for col in range(A1_COLUMN_INDEX, st.max_column + 1):
    #         if st.cell(row, col).value in NC_OPTION_FILTER_LIST:
    #             cell = st.cell(row, col, None)
    #             # print('rinse cell: {} - {}'.format(cell.coordinate, cell.value))
    #             i += 1
    for row in st['{}:{}'.format(QUESTION_TO_EXCEL_COLUMN_MAP['A1'][0], QUESTION_TO_EXCEL_COLUMN_MAP['I2-22-68'][0])]:
        for cell in row:
            if cell.value in NC_OPTION_FILTER_LIST:
                # print('rinse cell: {} - {}'.format(cell.coordinate, cell.value))
                cell.value = None
                i += 1
    print('>> {} cells rinsed'.format(i))

    rinse_values_by_column_rowindex(st, H5_COLUMN_EXCEL_INDEX_NC, range(HEADER_ROW_INDEX + 1, st.max_row + 1))
    rinse_values_by_column_rowindex(st, H6_COLUMN_EXCEL_INDEX_NC, range(HEADER_ROW_INDEX + 1, st.max_row + 1))


def rinse_values_by_column_rowindex(st, col, index_list):
    for i in index_list:
        coordinate = '{}{}'.format(col, i)
        if st[coordinate] is not None:
            # print('rinse cell: {} - {}'.format(coordinate, st[coordinate].value))
            st[coordinate] = None
            i += 1
    print('>> {} cells rinsed'.format(index_list.__len__()))


@clock
def rinse_invalid_answers(st):
    """rule 6: replace invalid answers(cell) with NaN"""
    print('rule 6: rinse G1 answers which in {}'.format(G1_OPTION_FILTER_LIST))
    # find them
    rinse_list = query_row_indexes_by_column_filter(st, QUESTION_TO_EXCEL_COLUMN_MAP['G1'][0],
                                                    lambda val: val in G1_OPTION_FILTER_LIST)
    # remove them
    rinse_values_by_column_rowindex(st, QUESTION_TO_EXCEL_COLUMN_MAP['G1'][0], rinse_list)
    rinse_values_by_column_rowindex(st, QUESTION_TO_EXCEL_COLUMN_MAP['G1'][1], rinse_list)


@clock
def rinse_unusual_salary_values(st):
    """rule 7: remove < 1000, top 0.3%, ABS(diff of MEAN) > 4 * STDEV """
    print('rule 7: remove < 1000, top 0.3%, ABS(diff of MEAN) > 4 * STDEV ')
    print('>> rinsing salary < 1000')
    rinse_list = query_row_indexes_by_column_filter(st, QUESTION_TO_EXCEL_COLUMN_MAP['B6'][0], filter_low_salary)
    rinse_values_by_column_rowindex(st, QUESTION_TO_EXCEL_COLUMN_MAP['B6'][0], rinse_list)

    print('>> rinsing top N salary')
    sort_range = '{}{}:{}{}'.format(QUESTION_TO_EXCEL_COLUMN_MAP['B6'][0], 2,
                                    QUESTION_TO_EXCEL_COLUMN_MAP['B6'][0], st.max_row);
    # st.auto_filter.add_sort_condition(sort_range)
    salary_list = {}
    for row in st[sort_range]:
        if row[0].value is not None and row[0].value != '':
            salary_list[row[0].coordinate] = int(row[0].value)

    sorted_salary_list = sorted(salary_list.items(), key=lambda kv: kv[1], reverse=True)
    top_n = round(sorted_salary_list.__len__() * 0.003)
    i = 0
    for item in sorted_salary_list:
        coordinate = item[0]
        # print('rinse cell: {} - {}'.format(coordinate, st[coordinate].value))
        st[coordinate] = None
        salary_list.pop(coordinate)
        i += 1
        if i >= top_n:
            break
    print('>> {} cells rinsed from {}'.format(top_n, sorted_salary_list.__len__()))

    print('>> rinsing ABS(salary - MEAN) > 4 * STDEV')
    np_salary_list = np.array(list(salary_list.values()), dtype=int)
    print('>> {} values in total'.format(np_salary_list.size))
    salary_mean = np_salary_list.mean()
    print('>> MEAN = {}'.format(salary_mean))
    salary_stdev = np_salary_list.std()
    print('>> STDEV = {}'.format(salary_stdev))
    salary_stdev_4 = salary_stdev * 4
    print('>> * 4 = {}'.format(salary_stdev_4))
    i = 0
    for coordinate in salary_list:
        salary = int(st[coordinate].value)
        if abs(salary - salary_mean) > salary_stdev_4:
            # print('rinse cell: {} - {}'.format(coordinate, st[coordinate].value))
            st[coordinate] = None
            i += 1
    print('>> {} cells rinsed'.format(i))


def filter_low_salary(val):
    if val is None or val == '':
        return False
    result = False;
    try:
        s = int(val)
        result = s < 1000
    except ValueError as e:
        print('>> failed to process {} - {}'.format(val, e))
    finally:
        pass
    return result


def test():
    src = '../test-data/san-ming/raw/answer20181016_1740112347.xlsx'
    dst = '../result/cleaned/answer20181016_1740112347_cleaned.xlsx'

    wb = xl.load_workbook(src)
    st = wb.worksheets[0]

    validate_data_dimensions(st)
    # remove_unnecessary_headers(st)
    # batch_reset_column_names(st)
    # reset_emplty_values_with_na

    # # Rule 1
    # remove_fake_records(st)
    # # Rule 2, 3
    # remove_unsubmitted_records(st)
    # # Rule 2, 3
    # remove_unqualified_records(st)
    # Rule 4
    rinse_irrelevant_answers(st)
    # Rule 5
    rinse_nc_option_values(st)
    # Rule 6
    rinse_invalid_answers(st)
    # Rule 7
    rinse_unusual_salary_values(st)
    wb.save(dst)


if __name__ == '__main__':
    test()
