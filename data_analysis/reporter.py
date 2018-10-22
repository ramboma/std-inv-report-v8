#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'reporter.py'

__author__ = 'kuoren'

import pandas as pd
import data_analysis.utils as answerUtil
import data_analysis.read_excel_util as excelUtil

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


def sum_subject_report(data, subject, answerType, filePath):
    '''就业竞争力报告'''

    column_relative = list(BASE_COLUMN)
    column_relative.append(subject)
    print(column_relative)
    data_relative = pd.DataFrame(data, columns=column_relative)
    data_where = data_relative[data_relative['A2'] == A2_ANSWER[0]]
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


def college_subject_report(data, subject, answerType, filePath):
    '''
    按学院分组，产生某个题目的总人数、五维占比、均值报告
    前提：和A2相关，需要去除一部分答案
    :param data: 元数据
    :param subject: 题目号
    :param answerType:0-符合；1-相关；
    :param filePath:输出文件
    :return:
    '''
    column_relative = list(BASE_COLUMN)
    column_relative.append(subject)
    data_relative = pd.DataFrame(data, columns=column_relative)
    data_where = data_relative[data_relative['A2'] == A2_ANSWER[0]]

    # step1:各学院答题总人数
    answer_count = answerUtil.answer_grp_count(data_where, [BASE_COLUMN[0], subject], BASE_COLUMN[0], subject)
    print("各学院{}回答总人数：\n".format(subject))
    print(answer_count)

    # step2:回答"无法评价"人数
    if answerType == 0:
        answer_except_count = answerUtil.answer_of_subject_count_grp(data_where,
                                                                     [BASE_COLUMN[0], subject],
                                                                     BASE_COLUMN[0],
                                                                     subject, ANSWER_NORMAL_1[-1])
        print("各学院各专业{}回答'{}'人数：\n".format(subject, ANSWER_NORMAL_1[-1]))
        print(answer_except_count)
    elif answerType == 1:
        answer_except_count = answerUtil.answer_of_subject_count_grp(data_where,
                                                                     [BASE_COLUMN[0], subject],
                                                                     BASE_COLUMN[0],
                                                                     subject, ANSWER_NORMAL_2[-1])
        print("各学院各专业{}回答'{}'人数：\n".format(subject, ANSWER_NORMAL_2[-1]))
        print(answer_except_count)
    elif answerType == 2:
        answer_except_count = answerUtil.answer_of_subject_count_grp(data_where,
                                                                     [BASE_COLUMN[0], subject],
                                                                     BASE_COLUMN[0],
                                                                     subject, ANSWER_NORMAL_3[-1])
        print("各学院各专业{}回答'{}'人数：\n".format(subject, ANSWER_NORMAL_3[-1]))
        print(answer_except_count)

    print("各学院{}回答'{}'人数：\n".format(subject, ANSWER_NORMAL_1[-1]))
    print(answer_except_count)

    # step3:B9-1 填答此题总人数-选项6无法评价的人数
    if answer_except_count.empty:
        print('no except')
        pd_five_total = pd.DataFrame({'college': answer_count[BASE_COLUMN[0]],
                                      'count': answer_count[subject]})
    else:
        print('need except')
        pd_left = pd.merge(answer_count, answer_except_count, how='left',
                           on=BASE_COLUMN[0], validate='one_to_one')
        pd_left['count'] = pd_left['B9-1-x'] - pd_left['B9-1-y']
        pd_left.fillna(0)
        pd_five_total = pd.DataFrame({'college': pd_left[BASE_COLUMN[0]],
                                      'count': pd_left['count']})
    print("各学院{}有效回答总人数：\n".format(subject))
    print(pd_five_total)

    # step3:分组统计有效答题人数=总人数-选项6无法评价的人数
    if answer_except_count.empty:
        print('no except')
        pd_five_total = pd.DataFrame({'college': answer_count[BASE_COLUMN[0]],
                                      'count': answer_count[subject]})
    else:
        print('need except')
        pd_left = pd.merge(answer_count, answer_except_count, how='left',
                           on=list(BASE_COLUMN[0]), validate='one_to_one')
        pd_left.fillna(0)
        pd_left['count'] = pd_left[subject + '-x'] - pd_left[subject + '-y']
        pd_five_total = pd.DataFrame({'college': pd_left[BASE_COLUMN[0]],
                                      'count': pd_left['count']})

    answer_values_grp = answerUtil.answer_grp_count(data_where, [BASE_COLUMN[0], subject, 'A2'],
                                                    [BASE_COLUMN[0], subject], subject)
    print("{}各答案分布：".format(subject))
    print(answer_values_grp)

    # step4:B9-1五维占比
    pd_five = pd.merge(answer_values_grp, pd_five_total, how='inner',
                       left_on=BASE_COLUMN[0], right_on='college', validate='many_to_one')
    pd_five['rate'] = (pd_five['A2'] / pd_five['count'] * 100).round(decimals=2)

    pd_five_rate = pd.DataFrame(pd_five, columns=[BASE_COLUMN[0], subject, 'rate'])
    print("各学院{}五维占比：\n".format(subject))
    print(pd_five_rate)

    if answerType == 0:
        matches = pd_five_rate[pd_five_rate[subject].isin(ANSWER_NORMAL_1[0:3])]
    elif answerType == 1:
        matches = pd_five_rate[pd_five_rate[subject].isin(ANSWER_NORMAL_2[0:3])]
    elif answerType == 2:
        matches = pd_five_rate[pd_five_rate[subject].isin(ANSWER_NORMAL_3[0:3])]

    matches_sum = answerUtil.answer_grp_sum(matches,
                                            [BASE_COLUMN[0], 'rate'],
                                            [BASE_COLUMN[0]])
    print("各学院{}吻合度：\n".format(subject))
    print(matches_sum)

    # step5:计算alpha
    answer_values_grp['val_score'] = answer_values_grp[subject]
    if answerType == 0:
        answer_values_grp.replace({'val_score': ANSWER_SCORE_DICT_1}, inplace=True)
    elif answerType == 1:
        answer_values_grp.replace({'val_score': ANSWER_SCORE_DICT_2}, inplace=True)
    elif answerType == 2:
        answer_values_grp.replace({'val_score': ANSWER_SCORE_DICT_3}, inplace=True)
    answer_values_grp['total_score'] = answer_values_grp['A2'] * answer_values_grp['val_score']
    answer_alpha = answerUtil.answer_grp_sum(answer_values_grp, [BASE_COLUMN[0], 'total_score'], [BASE_COLUMN[0]])

    # step5:计算mean
    pd_mean = pd.merge(answer_alpha, pd_five_total, how='inner',
                       left_on=BASE_COLUMN[0], right_on='college', validate='one_to_one')
    pd_mean['mean'] = (pd_mean['total_score'] / pd_mean['count']).round(decimals=2)
    print("各学院{}均值：".format(subject))
    print(pd_mean)

    pd_mean_match = pd.DataFrame({'college': pd_mean[BASE_COLUMN[0]],
                                  'mean': pd_mean['mean'],
                                  'match': matches_sum['rate'],
                                  'count': answer_count[subject]})
    pd_rate_mean_match = pd.merge(pd_five_rate, pd_mean_match, how='left',
                                  left_on=BASE_COLUMN[0], right_on='college', validate='many_to_one')
    print(pd_rate_mean_match)
    pd_result = pd.DataFrame(pd_rate_mean_match, columns=['college',
                                                          subject, 'rate', 'match',
                                                          'mean', 'count'])
    excelUtil.writeExcel(pd_result, filePath, subject + '各学院')
    return pd_result


def major_subject_report(data, subject, answerType, filePath):
    '''
    按专业分组，产生某个题目的总人数、五维占比、均值报告
    :param data: 元数据
    :param subject: 题目号
    :param answerType:0-符合；1-相关；
    :param filePath:输出文件
    :return:
    '''

    column_relative = list(BASE_COLUMN)
    column_relative.append(subject)
    data_relative = pd.DataFrame(data, columns=column_relative)
    data_where = data_relative[data_relative['A2'] == A2_ANSWER[0]]
    excelUtil.writeExcel(data_where, filePath, subject + '_source')

    college_major_subject = list(BASE_COLUMN[0:2])
    college_major_subject.append(subject)
    # step1:分组统计答题总人数
    answer_count = answerUtil.answer_grp_count(data_where, college_major_subject, list(BASE_COLUMN[0:2]), subject)
    print("各学院各专业{}回答总人数：\n".format(subject))
    print(answer_count)

    # step2:回答"无法评价"人数
    if answerType == 0:
        answer_except_count = answerUtil.answer_of_subject_count_grp(data_where,
                                                                     college_major_subject,
                                                                     list(BASE_COLUMN[0:2]),
                                                                     subject,
                                                                     ANSWER_NORMAL_1[-1])
        print("各学院各专业{}回答'{}'人数：\n".format(subject, ANSWER_NORMAL_1[-1]))
        print(answer_except_count)
    elif answerType == 1:
        answer_except_count = answerUtil.answer_of_subject_count_grp(data_where,
                                                                     college_major_subject,
                                                                     list(BASE_COLUMN[0:2]),
                                                                     subject,
                                                                     ANSWER_NORMAL_2[-1])
        print("各学院各专业{}回答'{}'人数：\n".format(subject, ANSWER_NORMAL_2[-1]))
        print(answer_except_count)
    elif answerType == 2:
        answer_except_count = answerUtil.answer_of_subject_count_grp(data_where,
                                                                     college_major_subject,
                                                                     list(BASE_COLUMN[0:2]),
                                                                     subject,
                                                                     ANSWER_NORMAL_3[-1])
        print("各学院各专业{}回答'{}'人数：\n".format(subject, ANSWER_NORMAL_3[-1]))
        print(answer_except_count)

    # step3:分组统计有效答题人数=总人数-选项6无法评价的人数
    if answer_except_count.empty:
        print('no except')
        pd_five_total = pd.DataFrame({'college': answer_count[BASE_COLUMN[0]],
                                      'major': answer_count[BASE_COLUMN[1]],
                                      'count': answer_count[subject]})
    else:
        print('need except')
        pd_left = pd.merge(answer_count, answer_except_count, how='left',
                           on=list(BASE_COLUMN[0:2]), validate='one_to_one')
        pd_left.fillna(0)
        pd_left['count'] = pd_left[subject + '-x'] - pd_left[subject + '-y']
        pd_five_total = pd.DataFrame({'college': pd_left[BASE_COLUMN[0]],
                                      'major': pd_left[BASE_COLUMN[1]],
                                      'count': pd_left['count']})

    # step4:分组统计各答案人数
    college_major_subject_other = list(BASE_COLUMN)
    college_major_subject_other.append(subject)
    answer_values_grp = answerUtil.answer_grp_count(data_where,
                                                    college_major_subject_other,
                                                    college_major_subject,
                                                    subject)
    print("各学院各专业{}各答案分布：".format(subject))
    print(answer_values_grp)

    # step5:五维占比
    pd_five = pd.merge(answer_values_grp, pd_five_total, how='inner',
                       left_on=list(BASE_COLUMN[0:2]), right_on=['college', 'major'],
                       validate='many_to_one')
    pd_five['rate'] = (pd_five['A2'] / pd_five['count'] * 100).round(decimals=2)

    pd_five_rate = pd.DataFrame(pd_five, columns=[BASE_COLUMN[0], BASE_COLUMN[1],
                                                  subject, 'rate'])
    print("各学院各专业{}五维占比：\n".format(subject))
    print(pd_five_rate)

    if answerType == 0:
        matches = pd_five_rate[pd_five_rate[subject].isin(ANSWER_NORMAL_1[0:3])]
    elif answerType == 1:
        matches = pd_five_rate[pd_five_rate[subject].isin(ANSWER_NORMAL_2[0:3])]
    elif answerType == 2:
        matches = pd_five_rate[pd_five_rate[subject].isin(ANSWER_NORMAL_3[0:3])]

    matches_sum = answerUtil.answer_grp_sum(matches,
                                            [BASE_COLUMN[0], BASE_COLUMN[1], 'rate'],
                                            [BASE_COLUMN[0], BASE_COLUMN[1]])
    print("各学院各专业{}吻合度：\n".format(subject))
    print(matches_sum)

    # step6:计算alpha
    answer_values_grp['val_score'] = answer_values_grp[subject]
    if answerType == 0:
        answer_values_grp.replace({'val_score': ANSWER_SCORE_DICT_1}, inplace=True)
    elif answerType == 1:
        answer_values_grp.replace({'val_score': ANSWER_SCORE_DICT_2}, inplace=True)
    elif answerType == 2:
        answer_values_grp.replace({'val_score': ANSWER_SCORE_DICT_3}, inplace=True)
    answer_values_grp['total_score'] = answer_values_grp['A2'] * answer_values_grp['val_score']
    answer_alpha = answerUtil.answer_grp_sum(answer_values_grp,
                                             [BASE_COLUMN[0], BASE_COLUMN[1], 'total_score'],
                                             [BASE_COLUMN[0], BASE_COLUMN[1]])

    # step5:计算mean
    pd_mean = pd.merge(answer_alpha, pd_five_total, how='inner',
                       left_on=list(BASE_COLUMN[0:2]), right_on=['college', 'major'], validate='one_to_one')
    pd_mean['mean'] = (pd_mean['total_score'] / pd_mean['count']).round(decimals=2)
    print("各学院{}均值：".format(subject))
    print(pd_mean)

    pd_mean_match = pd.DataFrame({'college': pd_mean[BASE_COLUMN[0]],
                                  'major': pd_mean[BASE_COLUMN[1]],
                                  'mean': pd_mean['mean'],
                                  'match': matches_sum['rate'],
                                  'count': answer_count[subject]})
    pd_rate_mean_match = pd.merge(pd_five_rate, pd_mean_match, how='left',
                                  left_on=list(BASE_COLUMN[0:2]), right_on=['college', 'major'], validate='many_to_one')
    print(pd_rate_mean_match)
    pd_result = pd.DataFrame(pd_rate_mean_match, columns=['college', 'major',
                                                          subject, 'rate', 'match',
                                                          'mean', 'count'])
    excelUtil.writeExcel(pd_result, filePath, subject + '各专业')
    return pd_result


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
    answer_count = answerUtil.answer_grp_count(data_where, college_major_subject, list(BASE_COLUMN[0:2]), subject)
    answer_count.columns = ['college', 'major', 'count']
    print("各学院各专业{}回答总人数：\n".format(subject))
    print(answer_count)

    # step2:各学院subject答题分布
    college_major_subject_other = list(BASE_COLUMN)
    college_major_subject_other.append(subject)
    answer_values_grp = answerUtil.answer_grp_count(data_where, college_major_subject_other, college_major_subject,
                                                    subject)
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
    dict={'rate': employee,'count': answer_count}
    pd_result = pd.DataFrame(list(dict.items()))
    print(pd_result)
    excelUtil.writeExcel(pd_result, filePath, '总体就业率')

    # 各答案人数
    answer_values = answerUtil.answer_val_count(data, subject)
    pd_a2_result = pd.DataFrame(data=answer_values)
    pd_a2_result['rate'] = (pd_result[subject] / answer_count * 100).round(decimals=2)
    print("{}各答案分布：".format(subject))
    print(pd_a2_result)

    pd_last = pd.DataFrame({"answer": pd_a2_result.index,
                            "rate": pd_a2_result.values})
    flexiable = pd_last[pd_last['answer'].isin(A2_ANSWER[1:3])].sum()
    pd_last['灵活就业'] = flexiable
    excelUtil.writeExcel(pd_last, filePath, '总体毕业去向')


def college_employee_report(data, subject, filePath):
    '''就业力报告'''

    # step1:各学院答题总人数
    answer_count = answerUtil.answer_grp_count(data, [BASE_COLUMN[0], subject], [BASE_COLUMN[0]])
    print("{}回答总人数：{}\n".format(subject, answer_count))

    # step2:回答"未就业"人数

    answer_except_count = answerUtil.answer_of_subject_count(data, subject, A2_ANSWER[-1])

    print("{}回答'{}'人数：{}\n".format(subject, ANSWER_NORMAL_1[-1], answer_except_count))
    print("就业率:{}".format((answer_count - answer_except_count) / answer_count).round(decimals=2))
