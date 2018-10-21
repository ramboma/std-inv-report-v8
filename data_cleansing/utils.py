#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""utils.py"""

__author__ = 'Gary.Z'

import openpyxl as xl
import numpy as np
import sys

from data_cleansing.clock import *

from data_cleansing.config import *


@clocking
def validate_data_dimensions(st):
    """rule 0: data dimension checking: row >=3 and col >= 231 """
    print('rule 0: validating data dimensions, cols: {}, rows: {}'.format(st.max_column, st.max_row))
    if st.max_column < 231:
        raise Exception("column count must >= 231")
    if st.max_row < 3:
        raise Exception("row count must >= 3")


@clocking
def remove_unnecessary_headers(st):
    """rule 0: remove row 1~2: include question description and option description"""
    print('rule 0: removing unnecessary header rows start at {}, count 2'.format(HEADER_ROW_INDEX + 1))
    st.delete_rows(HEADER_ROW_INDEX + 1, 2)


@clocking
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


@clocking
def reset_emplty_values_with_na(st):
    """rule 0: replace empty values with NaN """
    print('rule 0: replace empty values with NaN ')
    i = 0
    for row in st['{}:{}'.format(QUESTION_TO_EXCEL_COLUMN_MAP['A1'][0], QUESTION_TO_EXCEL_COLUMN_MAP['I2-22-68'][0])]:
        for cell in row:
            if cell.value == '':
                cell.value = None
                i += 1
    print('>> {} cells replaced'.format(i))


@clocking
def clear_all_cells_bgcolor(st):
    """rule 0: clear all cells' BG color """
    print('rule 0: clear all cells\' BG color ')
    for row in st['{}:{}'.format('A', QUESTION_TO_EXCEL_COLUMN_MAP['I2-22-68'][0])]:
        for cell in row:
            cell.fill = xl.styles.PatternFill(None)


@clocking
def remove_fake_records(st):
    """rule 1: remove fake data, e.g. column 14(专业名称) with value "测试专业" """
    print('rule 1: removing rows which major in {}'.format(MAJOR_FILTER_LIST))
    # find them
    remove_list = _query_row_indexes_by_column_filter(st, MAJOR_COLUMN_EXCEL_INDEX, lambda val: val in MAJOR_FILTER_LIST)
    # remove them
    _remove_rows_by_index_list(st, remove_list)


@clocking
def remove_unsubmitted_records(st):
    """rule 2, 3: remove un-submitted row, e.g. no submit-time exist"""
    print('rule 2, 3: removing rows which have no submit time')
    # find them
    remove_list = _query_row_indexes_by_column_filter(st, SUBMIT_TIME_COLUMN_EXCEL_INDEX,
                                                      lambda val: (val is None or val == ''))
    # remove them
    _remove_rows_by_index_list(st, remove_list)


@clocking
def remove_unqualified_records(st):
    """rule 2, 3: remove un-qualified row, e.g. no answer for question A2"""
    print('rule 2, 3: removing rows which have no A2 answers')
    # find them
    remove_list = _query_row_indexes_by_column_filter(st, QUESTION_TO_EXCEL_COLUMN_MAP['A2'][0],
                                                      lambda val: (val is None or val == ''))
    # remove them
    _remove_rows_by_index_list(st, remove_list)


@clocking
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
                            _add_tracing_comment(st[coordinate], '4', sys._getframe().f_code.co_name, rule)
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


@clocking
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
    for row in st['{}:{}'.format(QUESTION_TO_EXCEL_COLUMN_MAP['A1'][0],
                                 QUESTION_TO_EXCEL_COLUMN_MAP['I2-22-68'][0])]:
        for cell in row:
            if cell.value in NC_OPTION_FILTER_LIST:
                # print('rinse cell: {} - {}'.format(cell.coordinate, cell.value))
                _add_tracing_comment(cell, '5', sys._getframe().f_code.co_name)
                cell.value = None
                i += 1
    print('>> {} cells rinsed'.format(i))

    _rinse_values_by_column_rowindex(st, H5_COLUMN_EXCEL_INDEX_NC, range(HEADER_ROW_INDEX + 1, st.max_row + 1),
                                    '5', sys._getframe().f_code.co_name)
    _rinse_values_by_column_rowindex(st, H6_COLUMN_EXCEL_INDEX_NC, range(HEADER_ROW_INDEX + 1, st.max_row + 1),
                                    '5', sys._getframe().f_code.co_name)


@clocking
def rinse_invalid_answers(st):
    """rule 6: replace invalid answers(cell) with NaN"""
    print('rule 6: rinse G1 answers which in {}'.format(G1_OPTION_FILTER_LIST))
    # find them
    rinse_list = _query_row_indexes_by_column_filter(st, QUESTION_TO_EXCEL_COLUMN_MAP['G1'][0],
                                                     lambda val: val in G1_OPTION_FILTER_LIST)
    # remove them
    _rinse_values_by_column_rowindex(st, QUESTION_TO_EXCEL_COLUMN_MAP['G1'][0], rinse_list, '6', sys._getframe().f_code.co_name)
    _rinse_values_by_column_rowindex(st, QUESTION_TO_EXCEL_COLUMN_MAP['G1'][1], rinse_list, '6', sys._getframe().f_code.co_name)


def _add_tracing_comment(cell, rule, func, addition=None):
    if addition is None:
        text = 'rule {}\norigin val: {}\nfunc: {}'.format(rule, cell.value, func)
    else:
        text = 'rule {}\norigin val: {}\nfunc: {}\n{}'.format(rule, cell.value, func, addition)
    global RINSE_TRACING_ENABLED
    if (RINSE_TRACING_ENABLED):
        cell.comment = xl.comments.Comment(text, None, 150, 300)


def _query_row_indexes_by_column_filter(st, xl_col, cb_filter):
    idx_list = []
    for cell in st[xl_col]:
        if cell.row <= HEADER_ROW_INDEX:
            continue
        # print("cell: {}".format(cell.value))
        if cb_filter(cell.value):
            idx_list.append(cell.row)
    # print(idx_list)
    return idx_list


def _remove_rows_by_index_list(st, index_list):
    for i in range(0, index_list.__len__())[::-1]:
        print('remove row: {}'.format(st['A{}'.format(index_list[i])].value))
        st.delete_rows(index_list[i])
    print('>> {} rows removed'.format(index_list.__len__()))
    print('>> {}'.format(index_list))


def _rinse_values_by_column_rowindex(st, col, index_list, rule, func):
    for i in index_list:
        coordinate = '{}{}'.format(col, i)
        if st[coordinate] is not None:
            # print('rinse cell: {} - {}'.format(coordinate, st[coordinate].value))
            _add_tracing_comment(st[coordinate], rule, func)
            st[coordinate] = None
            i += 1
    print('>> {} cells rinsed'.format(index_list.__len__()))


def _filter_low_salary(val):
    if val is None or val == '':
        return False
    result = False;
    try:
        s = int(val)
        result = s < SALARY_FILTER_LOWER_LIMIT
    except ValueError as e:
        print('>> failed to process {} - {}'.format(val, e))
    finally:
        pass
    return result


@clocking
def rinse_unusual_salary_values(st):
    """rule 7: remove < 1000, top 0.3%, ABS(diff of MEAN) > 4 * STDEV """
    print('rule 7: remove < 1000, top 0.3%, ABS(diff of MEAN) > 4 * STDEV ')
    print('>> 7.1 rinsing salary < 1000')
    rinse_list = _query_row_indexes_by_column_filter(st, QUESTION_TO_EXCEL_COLUMN_MAP['B6'][0], _filter_low_salary)
    _rinse_values_by_column_rowindex(st, QUESTION_TO_EXCEL_COLUMN_MAP['B6'][0], rinse_list, '7.1', sys._getframe().f_code.co_name)

    print('>> 7.2 rinsing top N salary')
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
        _add_tracing_comment(st[coordinate], '7.2', sys._getframe().f_code.co_name)
        st[coordinate] = None
        salary_list.pop(coordinate)
        i += 1
        if i >= top_n:
            break
    print('>> {} cells rinsed from {}'.format(top_n, sorted_salary_list.__len__()))

    print('>> 7.3 rinsing ABS(salary - MEAN) > 4 * STDEV')
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
            _add_tracing_comment(st[coordinate], '7.3', sys._getframe().f_code.co_name)
            st[coordinate] = None
            i += 1
    print('>> {} cells rinsed'.format(i))


def test():
    src = '../test-data/test-20181019-raw.xlsx'
    dst = '../result/test-20181019-raw_cleaned.xlsx'

    wb = xl.load_workbook(src)
    st = wb.worksheets[0]

    validate_data_dimensions(st)
    remove_unnecessary_headers(st)
    batch_reset_column_names(st)
    # clear_all_cells_bgcolor(st)
    reset_emplty_values_with_na

    # Rule 1
    remove_fake_records(st)
    # Rule 2, 3
    remove_unsubmitted_records(st)
    # Rule 2, 3
    remove_unqualified_records(st)
    # Rule 4
    # rinse_irrelevant_answers(st)
    # Rule 5
    rinse_nc_option_values(st)
    # # Rule 6
    # rinse_invalid_answers(st)
    # # Rule 7
    # rinse_unusual_salary_values(st)
    wb.save(dst)


if __name__ == '__main__':
    test()
