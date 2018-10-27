#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'reporter.py'

__author__ = 'kuoren'

import pandas as pd
import data_analysis.utils as answerUtil
import data_analysis.read_excel_util as excelUtil
import data_analysis.formulas as formulas
import data_analysis.config as CONFIG

# _10:学院；_14:专业; 元组不能被修改
BASE_COLUMN = ('_10', '_14', 'A2')

ANSWER_NORMAL_1 = ['很符合', '比较符合', '一般', '比较不符合', '很不符合', '无法评价']
ANSWER_SCORE_DICT_1 = {'很符合': 5, '比较符合': 4, '一般': 3, '比较不符合': 2, '很不符合': 1, '无法评价': 0}
ANSWER_NORMAL_2 = ['很相关', '比较相关', '一般', '比较不相关', '很不相关', '无法评价']
ANSWER_SCORE_DICT_2 = {'很相关': 5, '比较相关': 4, '一般': 3, '比较不相关': 2, '很不相关': 1, '无法评价': 0}
ANSWER_NORMAL_3 = ['很满意', '比较满意', '一般', '比较不满意', '很不满意', '无法评价']
ANSWER_SCORE_DICT_3 = {'很满意': 5, '比较满意': 4, '一般': 3, '比较不满意': 2, '很不满意': 1, '无法评价': 0}
A2_ANSWER = ['在国内工作', '自主创业', '自由职业', '在国内求学', '出国/出境', '未就业']

REPORT_FOLDER = '../test-data/san-ming/report/'


def sum_subject_report(data, subject, answerType, filePath,a2_answer_index=0):
    '''就业竞争力报告'''

    column_relative = list(BASE_COLUMN)
    column_relative.append(subject)
    print(column_relative)
    data_relative = pd.DataFrame(data, columns=column_relative)
    data_where = data_relative[data_relative['A2'] == A2_ANSWER[a2_answer_index]]
    print(data_where)

    # step1:答题总人数
    answer_count = answerUtil.answer_count(data_where, subject)
    print("{}回答总人数：{}\n".format(subject, answer_count))

    # step2:回答"无法评价"人数
    if answerType == 0:
        answer_except_count = answerUtil.answer_of_subject_count(data, subject, ANSWER_NORMAL_1[-1])
    elif answerType == 1:
        answer_except_count = answerUtil.answer_of_subject_count(data, subject, ANSWER_NORMAL_2[-1])
    elif answerType == 2:
        answer_except_count = answerUtil.answer_of_subject_count(data, subject, ANSWER_NORMAL_3[-1])
    print("{}回答'{}'人数：{}\n".format(subject, ANSWER_NORMAL_1[-1], answer_except_count))

    # step3:B9-1各答案人数
    answer_values = answerUtil.answer_val_count(data, subject)
    pd_result = pd.DataFrame(data=answer_values)
    pd_result['rate'] = (pd_result[subject] / (answer_count - answer_except_count) * 100).round(decimals=2)
    print("{}各答案分布：".format(subject))
    print(pd_result)

    pd_result['val_score'] = pd_result.index
    if answerType == 0:
        matches = pd_result[pd_result['val_score'].isin(ANSWER_NORMAL_1[0:3])]['rate'].sum()
    elif answerType == 1:
        matches = pd_result[pd_result['val_score'].isin(ANSWER_NORMAL_2[0:3])]['rate'].sum()
    elif answerType == 2:
        matches = pd_result[pd_result['val_score'].isin(ANSWER_NORMAL_3[0:3])]['rate'].sum()
    print(matches)

    if answerType == 0:
        pd_result.replace({'val_score': ANSWER_SCORE_DICT_1}, inplace=True)
    elif answerType == 1:
        pd_result.replace({'val_score': ANSWER_SCORE_DICT_2}, inplace=True)
    elif answerType == 2:
        pd_result.replace({'val_score': ANSWER_SCORE_DICT_3}, inplace=True)
    print(pd_result)

    pd_result['total_score'] = pd_result[subject] * pd_result['val_score']
    alpha_x = pd_result['total_score'].sum()

    match_mean = (alpha_x / (answer_count - answer_except_count)).round(decimals=2)
    print(match_mean)
    pd_ret = pd.DataFrame({"answer": pd_result.index,
                           "rate": pd_result['rate']})
    pd_ret['match'] = matches
    pd_ret['mean'] = match_mean
    pd_ret['count'] = answer_count
    excelUtil.writeExcel(pd_ret, filePath, subject + '_总体')
    print(pd_ret)
    return pd_ret

def demission_reason(data, subject):
    '''
    离职原因统计
    :param data:
    :param subject:
    :return:
    '''
    column_relative = list(BASE_COLUMN)
    column_relative.append(subject)
    print(column_relative)
    data_relative = pd.DataFrame(data, columns=column_relative)
    data_where = data_relative[data_relative['A2'] == A2_ANSWER[0]]
    print(data_where)

    # step1:subject答题总人数
    answer_count = answerUtil.answer_count(data_where, subject)
    print("{}回答总人数：{}\n".format(subject, answer_count))

    # step3:subject各答案人数
    answer_values = answerUtil.answer_val_count(data, subject)
    pd_result = pd.DataFrame({'reason': answer_values.index, 'answer_count': answer_values.values})
    pd_result['rate'] = (pd_result['answer_count'] / answer_count * 100).round(decimals=2)

    print("{}各答案分布：".format(subject))
    print(pd_result)
    return pd_result


def demission_major(data, subject):
    '''
    离职分布，按专业
    :param data:
    :param subject:
    :return:
    '''
    column_relative = list(BASE_COLUMN)
    column_relative.append(subject)
    data_relative = pd.DataFrame(data, columns=column_relative)
    data_where = data_relative[data_relative['A2'] == A2_ANSWER[0]]

    college_major_subject = list(BASE_COLUMN[0:2])
    college_major_subject.append(subject)
    # step1:各学院subject答题总人数
    answer_count = answerUtil.answer_grp_count(data_where, college_major_subject, list(BASE_COLUMN[0:2]))
    answer_count.columns = ['college', 'major', 'count']
    print("各学院各专业{}回答总人数：\n".format(subject))
    print(answer_count)

    # step2:各学院subject答题分布
    college_major_subject_other = list(BASE_COLUMN)
    college_major_subject_other.append(subject)
    answer_values_grp = answerUtil.answer_grp_count(data_where, college_major_subject_other,
                                                    college_major_subject)
    print("{}各答案分布：".format(subject))
    print(answer_values_grp)

    # step4:各学院subject答题占比
    pd_answers = pd.merge(answer_values_grp, answer_count, how='inner',
                          left_on=list(BASE_COLUMN[0:2]), right_on=['college', 'major'], validate='many_to_one')
    pd_answers['rate'] = (pd_answers['A2'] / pd_answers['count'] * 100).round(decimals=2)

    pd_five_rate = pd.DataFrame(pd_answers, columns=[BASE_COLUMN[0], BASE_COLUMN[1], subject, 'rate'])
    print("各学院各专业{}五维占比：\n".format(subject))
    print(pd_five_rate)


def sum_employee_report(data, subject, filePath):
    '''就业力报告'''

    # step1:答题总人数
    answer_count = answerUtil.answer_count(data, subject)
    print("{}回答总人数：{}\n".format(subject, answer_count))

    # step2:回答"未就业"人数

    answer_except_count = answerUtil.answer_of_subject_count(data, subject, A2_ANSWER[-1])

    print("{}回答'{}'人数：{}\n".format(subject, ANSWER_NORMAL_1[-1], answer_except_count))
    employee = ((answer_count - answer_except_count) / answer_count * 100).round(decimals=2)
    print("就业率:{}".format(employee))
    pd_result = pd.DataFrame({'就业率':[employee],
                              subject:[answer_count]})
    print(pd_result)
    excelUtil.writeExcel(pd_result, filePath, '总体就业率')

    # 各答案人数
    answer_values = answerUtil.answer_val_count(data, subject)
    pd_last = pd.DataFrame({"答案": answer_values.index,
                            "答案人数": answer_values.values})
    pd_last['比例'] = (pd_last['答案人数'] / answer_count * 100).round(decimals=2)
    print("{}各答案分布：".format(subject))
    print(pd_last)

    pd_last['灵活就业'] = pd_last[pd_last['答案'].isin(A2_ANSWER[1:3])]['比例'].sum()
    excelUtil.writeExcel(pd_last, filePath, '总体毕业去向')


def college_employee_report(data, subject, filePath):
    '''就业力报告'''

    # step1:各学院答题总人数
    answer_count = answerUtil.answer_grp_count(data, [BASE_COLUMN[0], subject], [BASE_COLUMN[0]])
    print("{}各学院回答总人数：".format(subject))
    print(answer_count)

    # step2:各学院回答"未就业"人数
    answer_except_count = answerUtil.answer_of_subject_count_grp(data,
                                                                 [BASE_COLUMN[0], subject],
                                                                 [BASE_COLUMN[0]], subject,
                                                                 A2_ANSWER[-1])

    # step3:左连计算占比
    pd_answers_valid = pd.merge(answer_count, answer_except_count, how='left',
                                left_on=BASE_COLUMN[0], right_on=BASE_COLUMN[0], validate='one_to_one')
    print(pd_answers_valid)
    pd_answers_valid.fillna(0)
    pd_answers_valid['rate'] = (
                (pd_answers_valid[subject + '_x'] - pd_answers_valid[subject + '_y']) / pd_answers_valid[
            subject + '_x'] * 100).round(decimals=2)

    print(pd_answers_valid)
    excelUtil.writeExcel(pd_answers_valid, filePath, '学院总体就业率')

    college_grp_value = answerUtil.answer_grp_count(data, [BASE_COLUMN[0], subject], [BASE_COLUMN[0], subject])
    pd_answers_left = pd.merge(college_grp_value, answer_count, how='left',
                                left_on=BASE_COLUMN[0], right_on=BASE_COLUMN[0], validate='many_to_one')
    print(pd_answers_left)
    pd_answers_left['rate']=(pd_answers_left['cnt']/pd_answers_left[subject+'_y']*100).round(decimals=2)
    print(pd_answers_left)

    flexiable = pd_answers_left[pd_answers_left[subject+'_x'].isin(A2_ANSWER[1:3])]
    pd_flexiable=answerUtil.answer_grp_sum(flexiable,[BASE_COLUMN[0],'rate'],[BASE_COLUMN[0]])
    pd_answers_merge = pd.merge(pd_answers_left, pd_flexiable, how='left',
                               left_on=BASE_COLUMN[0], right_on=BASE_COLUMN[0], validate='many_to_one')
    print(pd_answers_merge)
    excelUtil.writeExcel(pd_answers_merge, filePath, '学院就业去向')

def major_employee_report(data, subject, filePath):
    '''就业力报告'''

    # step1:答题总人数
    answer_count = answerUtil.answer_grp_count(data, [BASE_COLUMN[0],BASE_COLUMN[1], subject], [BASE_COLUMN[0],BASE_COLUMN[1]])
    print("{}各学院回答总人数：".format(subject))
    print(answer_count)

    # step2:各学院回答"未就业"人数
    answer_except_count = answerUtil.answer_of_subject_count_grp(data,
                                                                 [BASE_COLUMN[0],BASE_COLUMN[1], subject],
                                                                 [BASE_COLUMN[0],BASE_COLUMN[1]], subject,
                                                                 A2_ANSWER[-1])

    # step3:左连计算占比
    pd_answers_valid = pd.merge(answer_count, answer_except_count, how='left',
                                left_on=list(BASE_COLUMN[0:2]), right_on=list(BASE_COLUMN[0:2]), validate='one_to_one')
    print(pd_answers_valid)
    pd_answers_valid.fillna(0)
    pd_answers_valid['rate'] = (
            (pd_answers_valid[subject + '_x'] - pd_answers_valid[subject + '_y']) / pd_answers_valid[
        subject + '_x'] * 100).round(decimals=2)

    print(pd_answers_valid)
    excelUtil.writeExcel(pd_answers_valid, filePath, '专业总体就业率')

    college_grp_value = answerUtil.answer_grp_count(data, [BASE_COLUMN[0],BASE_COLUMN[1], subject], [BASE_COLUMN[0],BASE_COLUMN[1],subject])
    pd_answers_left = pd.merge(college_grp_value, answer_count, how='left',
                               left_on=list(BASE_COLUMN[0:2]), right_on=list(BASE_COLUMN[0:2]), validate='many_to_one')
    print(pd_answers_left)
    pd_answers_left['rate'] = (pd_answers_left['cnt'] / pd_answers_left[subject + '_y'] * 100).round(decimals=2)
    print(pd_answers_left)

    flexiable = pd_answers_left[pd_answers_left[subject + '_x'].isin(A2_ANSWER[1:3])]
    pd_flexiable = answerUtil.answer_grp_sum(flexiable, [BASE_COLUMN[0],BASE_COLUMN[1], 'rate'], [BASE_COLUMN[0],BASE_COLUMN[1]])
    pd_answers_merge = pd.merge(pd_answers_left, pd_flexiable, how='left',
                        left_on=list(BASE_COLUMN[0:2]), right_on=list(BASE_COLUMN[0:2]), validate='many_to_one')
    print(pd_answers_merge)
    excelUtil.writeExcel(pd_answers_merge, filePath, '专业就业去向')

