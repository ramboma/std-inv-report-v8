#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'formulas.py'

__author__ = 'kuoren'

import pandas as pd
import data_analysis.config as CONFIG
import data_analysis.utils as Util


def answer_rate(data, subject):
    '''

    AnswerRate 答案占比
    :param data: 数据
    :param subject: 题号
    :return: '答案', '回答此答案人数', '答题总人数', '比例'
    '''

    count = Util.answer_count(data, subject);
    pd_value_count = Util.answer_val_count(data, subject)
    pd_result = pd.DataFrame({CONFIG.RATE_COLUMN[0]: pd_value_count.index,
                              CONFIG.RATE_COLUMN[1]: pd_value_count.values})
    pd_result[CONFIG.RATE_COLUMN[2]] = count
    pd_result[CONFIG.RATE_COLUMN[3]] = (
            pd_result[CONFIG.RATE_COLUMN[1]] / pd_result[CONFIG.RATE_COLUMN[2]] * 100).round(decimals=2)

    return pd_result


def answer_rate_condition(data, subject, dict_cond={}, array_order=[],
                          array_asc=[], top=0):
    '''

    AnswerRate 答案占比 支持条件、排序、top
    ****此公式包含默认的前提：A2=在国内工作
    :param data: 数据
    :param dict_cond: 条件 {'column':'column_name','cond':'cond_val'}
    :param array_order: 排序
    :param array_asc: 排序方式，长度必须和排序长度相同
    :param top: top值
    :return:'答案', '回答此答案人数', '答题总人数', '比例'
    '''
    if not isinstance(dict_cond, dict):
        print('**********param type error')
        return

    # 前提要素
    df_primise = data[data[CONFIG.BASE_COLUMN[-1]] == CONFIG.A2_ANSWER[0]]

    # 条件过滤
    if not dict_cond:
        df_data = df_primise
    else:
        col_cond = str(dict_cond[CONFIG.DICT_KEY[0]])
        df_data = df_primise[df_primise[col_cond] == dict_cond[CONFIG.DICT_KEY[1]]]

    df_result = answer_rate(df_data, subject)

    if array_order:
        df_result.sort_values(array_order, ascending=array_asc, inplace=True)
    if top:
        df_result = df_result.head(top)

    return df_result


def formulas_employe_rate(data, dict_cond={}):
    '''

    Employe rate:就业率，支持条件过滤
    公式：（就业人数-未就业人数）/答题总人数
    :param data:
    :param dict_cond:
    :return: 就业率 答题总人数
    '''
    subject = 'A2'

    # 条件过滤
    if not dict_cond:
        df_data = data
    else:
        col_cond = str(dict_cond[CONFIG.DICT_KEY[0]])
        df_data = data[data[col_cond] == dict_cond[CONFIG.DICT_KEY[1]]]

    # step1:答题总人数
    count = Util.answer_count(data, subject)

    # step2:回答"未就业"人数
    unemployee_count = Util.answer_of_subject_count(data, subject,
                                                    CONFIG.A2_ANSWER[-1])

    employee_rate = ((count - unemployee_count) / count * 100).round(decimals=2)
    # 就业率 答题总人数
    pd_result = pd.DataFrame({CONFIG.EMPLOYEE_RATE_COLUMN: [employee_rate],
                              CONFIG.RATE_COLUMN[2]: [count]})
    return pd_result


def formulas_college_employe_rate(data):
    '''

    Employe rate:各学院就业率
    公式：（就业人数-未就业人数）/答题总人数
    :param data:
    :param dict_cond:
    :return: 就业率 答题总人数
    '''
    subject = 'A2'

    # step1:各学院答题总人数
    df_count = Util.answer_grp_count(data, [CONFIG.BASE_COLUMN[0], subject], [CONFIG.BASE_COLUMN[0]])
    df_count.columns = [CONFIG.GROUP_COLUMN[0], CONFIG.RATE_COLUMN[2]]
    # step2:各学院回答"未就业"人数
    df_unemployee = Util.answer_of_subject_count_grp(data, [CONFIG.BASE_COLUMN[0], subject],
                                                     [CONFIG.BASE_COLUMN[0]], subject,
                                                     CONFIG.A2_ANSWER[-1])
    df_unemployee.columns = [CONFIG.GROUP_COLUMN[0], 'unemployee']

    df_left = pd.merge(df_count, df_unemployee, how='left', on=CONFIG.GROUP_COLUMN[0])
    df_left.fillna(0, inplace=True)
    # 就业率 答题总人数
    df_left[CONFIG.EMPLOYEE_RATE_COLUMN] = (
            (df_left[CONFIG.RATE_COLUMN[2]] - df_left['unemployee']) / df_left[CONFIG.RATE_COLUMN[2]] * 100).round(
        decimals=2)
    df_left.drop(['unemployee'], axis='columns', inplace=True)
    df_left.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)

    return df_left


def formulas_major_employe_rate(data):
    '''

    Employe rate:各学院就业率
    公式：（就业人数-未就业人数）/答题总人数
    :param data:
    :param dict_cond:
    :return: 就业率 答题总人数
    '''
    subject = 'A2'

    # step1:各学院答题总人数
    df_count = Util.answer_grp_count(data,
                                     [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1], subject],
                                     [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]])
    df_count.columns = [CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1], CONFIG.RATE_COLUMN[2]]
    # step2:各学院回答"未就业"人数
    df_unemployee = Util.answer_of_subject_count_grp(data,
                                                     [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1], subject],
                                                     [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]],
                                                     subject,
                                                     CONFIG.A2_ANSWER[-1])
    df_unemployee.columns = [CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1], 'unemployee']

    df_left = pd.merge(df_count, df_unemployee,
                       how='left',
                       on=[CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1]])
    df_left.fillna(0, inplace=True)
    # 就业率 答题总人数
    df_left[CONFIG.EMPLOYEE_RATE_COLUMN] = (
            (df_left[CONFIG.RATE_COLUMN[2]] - df_left['unemployee']) / df_left[CONFIG.RATE_COLUMN[2]] * 100).round(
        decimals=2)
    df_left.drop(['unemployee'], axis='columns', inplace=True)
    df_left.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)

    return df_left


def formula_income_mean(data, dict_cond={}):
    '''

    Income mean:薪酬均值
    ****此公式包含默认的前提：A2=在国内工作
    公式：薪酬总和/答题总人数
    :param data:
    :param dict_cond:
    :return:
    '''
    subject = 'B6'
    # 前提要素
    df_primise = data[data[CONFIG.BASE_COLUMN[-1]] == CONFIG.A2_ANSWER[0]]

    # 条件过滤
    if not dict_cond:
        df_data = df_primise
    else:
        col_cond = str(dict_cond[CONFIG.DICT_KEY[0]])
        df_data = df_primise[df_primise[col_cond] == dict_cond[CONFIG.DICT_KEY[1]]]

    count = Util.answer_count(df_data, subject)
    sum = Util.answer_sum(df_data, subject)
    mean = (sum / count).round(decimals=2)
    # 均值 答题总人数
    pd_mean = pd.DataFrame({CONFIG.MEAN_COLUMN[2]: [count],
                            CONFIG.MEAN_COLUMN[-1]: [mean]})
    return pd_mean


def rate_T(df_data, array_focus=[CONFIG.MEAN_COLUMN[2]], ):
    '''总体 比率转置'''
    if df_data.empty:
        return df_data

    # 答题总人数
    summary_num = df_data.loc[0, CONFIG.RATE_COLUMN[2]]
    df_summary = df_data.loc[:,array_focus]
    df_duplicate = df_summary.drop_duplicates()

    # 转置列 比例
    df_metrics = df_data.loc[:,[CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[-1]]]
    df_metrics.loc[:,CONFIG.RATE_COLUMN[0]]=df_metrics.loc[:,CONFIG.RATE_COLUMN[0]].astype('str')
    df_metrics = df_metrics.set_index([CONFIG.RATE_COLUMN[0]])
    df_t = df_metrics.T
    df_t = df_t.reset_index()
    df_t = pd.concat([df_t, df_duplicate], axis=1)
    return df_t


def college_rate_pivot(df_data, array_focus=[CONFIG.MEAN_COLUMN[2]], hasCollege=True):
    '''学院 比率转置'''
    if df_data.empty:
        return df_data

    # 默认为按学院分组 列名为学院，由于五维占比有按其他分组条件分组，则列名为分组
    if hasCollege:
        grp_name = CONFIG.GROUP_COLUMN[0]
    else:
        grp_name = CONFIG.GROUP_COLUMN[-1]
    # 非转置列 学院、答题总人数
    ls_focus = array_focus.copy()
    ls_focus.append(grp_name)

    df_summary = df_data.loc[:,ls_focus]
    df_duplicate = df_summary.drop_duplicates()
    # 转置列 学院、比例
    df_metrics = df_data.pivot(index=grp_name,
                               columns=CONFIG.RATE_COLUMN[0],
                               values=CONFIG.RATE_COLUMN[-1])
    df_metrics.fillna(0.00, inplace=True)

    # 转置合并
    df_t = pd.merge(df_metrics, df_duplicate, how='left', on=grp_name)
    df_t.sort_values(CONFIG.MEAN_COLUMN[2],ascending=0,inplace=True)

    return df_t


def major_rate_pivot(df_data, array_focus=[CONFIG.MEAN_COLUMN[2]]):
    '''
    Major Privot:学院 比率转置
    :param df_data: 数据源
    :param array_focus: 非转置列，默认只关注答题总人数、对于均值和相关度需要自行配置
    :param column_name:
    :return: 比例行专列后的结果
    '''
    if df_data.empty:
        return df_data

    # 非转置列 学院、专业、答题总人数
    ls_focus = array_focus.copy()
    ls_focus.append(CONFIG.GROUP_COLUMN[0])
    ls_focus.append(CONFIG.GROUP_COLUMN[1])
    df_summary = df_data.loc[:,ls_focus]
    df_duplicate = df_summary.drop_duplicates()
    # 转置列
    df_metrics = pd.pivot_table(df_data,
                                index=[CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1]],
                                columns=CONFIG.RATE_COLUMN[0],
                                values=CONFIG.RATE_COLUMN[-1])
    df_metrics.fillna(0.00, inplace=True)

    # 转置合并
    df_t = pd.merge(df_metrics, df_duplicate, how='left', on=[CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1]])
    df_t.sort_values(CONFIG.MEAN_COLUMN[2],ascending=0,inplace=True)

    return df_t


# df = df[['user_id', 'book_id', 'rating', 'mark_date']]
# 调整列顺序为'user_id','book_id','rating','mark_date'


def major_row_combine(df_data, array_focus=[CONFIG.MEAN_COLUMN[2]], combin_name=CONFIG.COMBINE_RATE):
    if df_data.empty:
        return df_data

    # 非合并列 学院、专业、答题总人数
    ls_focus = array_focus.copy()
    ls_focus.append(CONFIG.GROUP_COLUMN[0])
    ls_focus.append(CONFIG.GROUP_COLUMN[1])
    df_summary = df_data.loc[:,ls_focus]
    df_duplicate = df_summary.drop_duplicates()

    # 多列合并单列
    df_combine = df_data.loc[:,
        [CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1], CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[-1]]]
    df_combine['answer_rate'] = df_combine[CONFIG.RATE_COLUMN[0]].astype(str) + '(' + df_combine[
        CONFIG.RATE_COLUMN[-1]].astype(float).astype(str) + '%)'
    df_combined = df_combine.loc[:,[CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1], 'answer_rate']]
    df_combined.rename(columns={'answer_rate': combin_name},inplace=True)
    df_row_combine = df_combined.groupby([CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1]],
                                         as_index=False).aggregate(
        lambda x: list(x))
    # 转置合并
    df_result = pd.merge(df_row_combine, df_duplicate, how='left', on=[CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1]])
    df_result.sort_values(CONFIG.MEAN_COLUMN[2],ascending=0,inplace=True)

    return df_result


def college_row_combine(df_data, array_focus=[CONFIG.MEAN_COLUMN[2]], combin_name=CONFIG.COMBINE_RATE):
    if df_data.empty:
        return df_data

    # 非合并列 学院、答题总人数
    ls_focus = array_focus.copy()
    ls_focus.append(CONFIG.GROUP_COLUMN[0])
    df_summary = df_data.loc[:,ls_focus]
    df_duplicate = df_summary.drop_duplicates()

    # 多列合并单列
    df_combine = df_data.loc[:,
        [CONFIG.GROUP_COLUMN[0], CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[-1]]]
    df_combine['answer_rate'] = df_combine[CONFIG.RATE_COLUMN[0]].astype(str) + '(' + df_combine[
        CONFIG.RATE_COLUMN[-1]].astype(float).astype(str) + '%)'
    df_combined = df_combine.loc[:,[CONFIG.GROUP_COLUMN[0], 'answer_rate']]
    df_combined.rename(columns={'answer_rate': combin_name},inplace=True)
    df_row_combine = df_combined.groupby(CONFIG.GROUP_COLUMN[0],
                                         as_index=False).aggregate(
        lambda x: list(x))
    print(df_row_combine)
    # 转置合并
    df_result = pd.merge(df_row_combine, df_duplicate, how='left', on=CONFIG.GROUP_COLUMN[0])
    df_result.sort_values(CONFIG.MEAN_COLUMN[2],ascending=0,inplace=True)
    return df_result
