#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'reporter.py'

__author__ = 'kuoren'

import pandas as pd
import data_analysis.utils as answerUtil

#_10:学院；_14:专业
BASE_COLUMN = ['_10', '_12', '_14', 'A2']

ANSWER_NORMAL_1 = ['很符合', '比较符合', '一般', '比较不符合', '很不符合', '无法评价']
ANSWER_SCORE_DICT_1 = {'很符合': 5, '比较符合': 4, '一般': 3, '比较不符合': 2, '很不符合': 1, '无法评价': 0}
ANSWER_NORMAL_2 = ['很相关', '比较相关', '一般', '比较不相关', '很不相关', '无法评价']
ANSWER_SCORE_DICT_2 = {'很相关': 5, '比较相关': 4, '一般': 3, '比较不相关': 2, '很不相关': 1, '无法评价': 0}
A2_ANSWER = ['在国内工作', '自主创业', '自由职业', '在国内求学', '出国/出境', '未就业']


def employability(data):
    '''就业竞争力报告'''

    subject = 'B9-1'
    column_relative = BASE_COLUMN.copy()
    column_relative.append(subject)
    print(column_relative)
    data_relative = pd.DataFrame(data, columns=column_relative)
    data_where = data_relative[data_relative['A2'] == A2_ANSWER[0]]
    print(data_where)

    # step1:B9-1答题总人数
    answer_count = answerUtil.answer_count(data_where, subject)
    print("{}回答总人数：{}\n".format(subject, answer_count))

    # step2:B9-1回答"无法评价"人数
    answer_except_count = answerUtil.answer_of_subject_count(data, subject, ANSWER_NORMAL_1[-1])
    print("{}回答'{}'人数：{}\n".format(subject, ANSWER_NORMAL_1[-1], answer_except_count))

    # step3:B9-1各答案人数
    answer_values = answerUtil.answer_val_count(data, subject)
    pd_result = pd.DataFrame(data=answer_values)
    pd_result['rate'] = (pd_result[subject] / (answer_count - answer_except_count) * 100).round(decimals=2)
    print("{}各答案分布：".format(subject))
    print(pd_result)

    pd_result['val_score'] = pd_result.index
    matches = pd_result[pd_result['val_score'].isin(ANSWER_NORMAL_2[0:3])]['rate'].sum()
    print(matches)

    pd_result.replace({'val_score': ANSWER_SCORE_DICT_2},inplace=True)
    print(pd_result)

    pd_result['total_score'] = pd_result[subject] * pd_result['val_score']
    alpha_x = pd_result['total_score'].sum()

    match_mean = (alpha_x / (answer_count - answer_except_count)).round(decimals=2)
    print(match_mean)

    print(pd_result.T)


def employability_college(data):
    subject = 'B9-1'
    column_relative = BASE_COLUMN.copy()
    column_relative.append(subject)
    data_relative = pd.DataFrame(data, columns=column_relative)
    data_where = data_relative[data_relative['A2'] == A2_ANSWER[0]]
    print(data_where)

    # step1:各学院 B9-1答题总人数
    answer_count = answerUtil.answer_grp_count(data_where, [BASE_COLUMN[0],subject],BASE_COLUMN[0],subject)
    print("各学院{}回答人数：\n".format(subject))
    print(answer_count)

    # step2:B9-1回答"无法评价"人数
    answer_except_count = answerUtil.answer_of_subject_count_grp(data_where, [BASE_COLUMN[0],subject],BASE_COLUMN[0],subject,ANSWER_NORMAL_1[-1])
    print("各学院{}回答'{}'人数：\n".format(subject, ANSWER_NORMAL_1[-1]))
    print(answer_except_count)

    # step3:B9-1各答案人数
    answer_values = answerUtil.answer_grp_count(data_where, [BASE_COLUMN[0],subject],[BASE_COLUMN[0],subject],subject)
    pd_result = pd.DataFrame(data=answer_values)
    print("{}各答案分布：".format(subject))
    print(pd_result)
    