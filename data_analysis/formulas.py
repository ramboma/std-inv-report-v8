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

def formulas_employe_rate(data,dict_cond={}):
    '''

    Employe rate:就业率，支持条件过滤
    公式：（就业人数-未就业人数）/答题总人数
    :param data:
    :param dict_cond:
    :return: 就业率 答题总人数
    '''
    subject='A2'

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

def formula_income_mean(data,dict_cond={}):
    '''

    Income mean:薪酬均值
    ****此公式包含默认的前提：A2=在国内工作
    公式：薪酬总和/答题总人数
    :param data:
    :param dict_cond:
    :return:
    '''
    subject='B6'
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


def rate_T(df_sigle, column_name=CONFIG.TOTAL_COLUMN):
    '''总体 比率转置'''
    if df_sigle.empty:
        return df_sigle
    join_num = df_sigle.loc[0, CONFIG.RATE_COLUMN[2]]
    df_metrics = df_sigle[[CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[-1]]]
    df_metrics = df_metrics.set_index([CONFIG.RATE_COLUMN[0]])
    df_t = df_metrics.T
    df_t[CONFIG.RATE_COLUMN[2]] = join_num
    df_t.columns.name = column_name
    return df_t


def college_rate_T(df_data, column_name=CONFIG.GROUP_COLUMN[0]):
    '''学院 比率转置'''
    if df_data.empty:
        return df_data
    df_metrics = df_data[[CONFIG.GROUP_COLUMN[0], CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[-1]]]
    df_metrics = df_metrics.set_index([CONFIG.GROUP_COLUMN[0], CONFIG.RATE_COLUMN[0]])
    df_t = df_metrics.unstack()
    # df_t.columns.name = column_name
    df_t.reset_index(inplace=True)
    df_t.fillna(0,inplace=True)
    print(df_t)
    return df_t



