#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'formulas.py'

__author__ = 'kuoren'

import pandas as pd
import numpy as np
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

    pd_result[CONFIG.RATE_COLUMN[-1]] = pd_result.loc[:, CONFIG.RATE_COLUMN[-1]].map(lambda x: '%.2f%%' % x)
    return pd_result


def answer_rate_condition(data, subject, dict_cond={}, array_order=[],
                          array_asc=[], top=0):
    '''

    AnswerRate 答案占比 支持条件、排序、top
    ****此公式包含默认的前提：A2=在国内工作
    :param data: 数据
    :param dict_cond: 条件 {'column':'column_name','cond':'cond_val','oper':'..'}
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
        val = str(dict_cond[CONFIG.DICT_KEY[1]])
        oper = dict_cond[CONFIG.DICT_KEY[2]]
        if oper == CONFIG.OPER[0]:
            df_data = df_primise[df_primise[col_cond] == val]
        elif oper == CONFIG.OPER[1]:
            df_data = df_primise[df_primise[col_cond] != val]

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


def rate_T(df_data, array_focus=[]):
    '''总体 比率转置'''
    if df_data.empty:
        return df_data

    if not array_focus:
        focus = [CONFIG.MEAN_COLUMN[2]]
    else:
        focus = array_focus.copy()
        focus.append(CONFIG.MEAN_COLUMN[2])
    # 答题总人数 和关注的纬度
    df_summary = df_data.loc[:, focus]
    df_duplicate = df_summary.drop_duplicates()

    # 转置列 比例 选项和比例
    df_metrics = df_data.loc[:, [CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[-1]]]
    df_metrics[CONFIG.RATE_COLUMN[0]] = df_metrics.loc[:, CONFIG.RATE_COLUMN[0]].astype('str')
    df_metrics = df_metrics.set_index([CONFIG.RATE_COLUMN[0]])
    df_t = df_metrics.T
    df_t = df_t.reset_index()
    df_t = pd.concat([df_t, df_duplicate], axis=1)
    print(df_t)
    return df_t


def college_rate_pivot(df_data, array_focus=[], grp_subject=CONFIG.BASE_COLUMN[0]):
    '''学院 比率转置'''
    if df_data.empty:
        return df_data

    # 默认为按学院分组 列名为学院，由于五维占比有按其他分组条件分组，则列名为分组
    if grp_subject == CONFIG.BASE_COLUMN[0]:
        grp_name = CONFIG.GROUP_COLUMN[0]
    else:
        grp_name = CONFIG.GROUP_COLUMN[-1]

    if not array_focus:
        focus = [CONFIG.MEAN_COLUMN[2]]
    else:
        focus = array_focus.copy()
        focus.append(CONFIG.MEAN_COLUMN[2])

    # 非转置列 学院、答题总人数
    focus.append(grp_name)

    df_summary = df_data.loc[:, focus]
    df_duplicate = df_summary.drop_duplicates()
    # 转置列 学院、比例
    df_metrics = df_data.pivot(index=grp_name,
                               columns=CONFIG.RATE_COLUMN[0],
                               values=CONFIG.RATE_COLUMN[-1])
    df_metrics.fillna(0.00, inplace=True)

    # 转置合并
    df_t = pd.merge(df_metrics, df_duplicate, how='left', on=grp_name)
    df_t.sort_values(CONFIG.MEAN_COLUMN[2], ascending=0, inplace=True)

    return df_t


def major_rate_pivot(df_data, array_focus=[]):
    '''
    Major Privot:学院 比率转置
    :param df_data: 数据源
    :param array_focus: 非转置列，默认只关注答题总人数、对于均值和相关度需要自行配置
    :param column_name:
    :return: 比例行专列后的结果
    '''
    if df_data.empty:
        return df_data

    if not array_focus:
        focus = [CONFIG.MEAN_COLUMN[2]]
    else:
        focus = array_focus.copy()
        focus.append(CONFIG.MEAN_COLUMN[2])

    # 非转置列 学院、专业、答题总人数
    focus.append(CONFIG.GROUP_COLUMN[0])
    focus.append(CONFIG.GROUP_COLUMN[1])
    df_summary = df_data.loc[:, focus]
    df_duplicate = df_summary.drop_duplicates()
    # 转置列
    df_metrics = pd.pivot_table(df_data,
                                index=[CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1]],
                                columns=CONFIG.RATE_COLUMN[0],
                                values=CONFIG.RATE_COLUMN[-1])
    df_metrics.fillna(0.00, inplace=True)

    # 转置合并
    df_t = pd.merge(df_metrics, df_duplicate, how='left', on=[CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1]])
    df_t.sort_values(CONFIG.MEAN_COLUMN[2], ascending=0, inplace=True)

    return df_t


def major_row_combine(df_data, array_focus=[CONFIG.MEAN_COLUMN[2]], combin_name=CONFIG.COMBINE_RATE):
    if df_data.empty:
        return df_data

    # 非合并列 学院、专业、答题总人数
    ls_focus = array_focus.copy()
    ls_focus.append(CONFIG.GROUP_COLUMN[0])
    ls_focus.append(CONFIG.GROUP_COLUMN[1])
    df_summary = df_data.loc[:, ls_focus]
    df_duplicate = df_summary.drop_duplicates()

    # 多列合并单列
    df_combine = df_data.loc[:,
                 [CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1], CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[-1]]]
    df_combine['answer_rate'] = df_combine[CONFIG.RATE_COLUMN[0]].astype(str) + '(' + df_combine[
        CONFIG.RATE_COLUMN[-1]].astype(float).astype(str) + '%)'
    df_combined = df_combine.loc[:, [CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1], 'answer_rate']]
    df_combined.rename(columns={'answer_rate': combin_name}, inplace=True)
    df_row_combine = df_combined.groupby([CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1]],
                                         as_index=False).aggregate(
        lambda x: list(x))
    # 转置合并
    df_result = pd.merge(df_row_combine, df_duplicate, how='left', on=[CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1]])
    df_result.sort_values(CONFIG.MEAN_COLUMN[2], ascending=0, inplace=True)

    return df_result


def college_row_combine(df_data, array_focus=[CONFIG.MEAN_COLUMN[2]], combin_name=CONFIG.COMBINE_RATE):
    if df_data.empty:
        return df_data

    # 非合并列 学院、答题总人数
    ls_focus = array_focus.copy()
    ls_focus.append(CONFIG.GROUP_COLUMN[0])
    df_summary = df_data.loc[:, ls_focus]
    df_duplicate = df_summary.drop_duplicates()

    # 多列合并单列
    df_combine = df_data.loc[:,
                 [CONFIG.GROUP_COLUMN[0], CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[-1]]]
    df_combine['answer_rate'] = df_combine[CONFIG.RATE_COLUMN[0]].astype(str) + '(' + df_combine[
        CONFIG.RATE_COLUMN[-1]].astype(float).astype(str) + '%)'
    df_combined = df_combine.loc[:, [CONFIG.GROUP_COLUMN[0], 'answer_rate']]
    df_combined.rename(columns={'answer_rate': combin_name}, inplace=True)
    df_row_combine = df_combined.groupby(CONFIG.GROUP_COLUMN[0],
                                         as_index=False).aggregate(
        lambda x: list(x))
    print(df_row_combine)
    # 转置合并
    df_result = pd.merge(df_row_combine, df_duplicate, how='left', on=CONFIG.GROUP_COLUMN[0])
    df_result.sort_values(CONFIG.MEAN_COLUMN[2], ascending=0, inplace=True)
    return df_result


def single_row_combine(df_data, grp_column, array_focus=[CONFIG.MEAN_COLUMN[2]], combin_name=CONFIG.COMBINE_RATE):
    if df_data.empty:
        return df_data

    # 非合并列 学院、答题总人数
    ls_focus = array_focus.copy()
    ls_focus.append(grp_column)
    df_summary = df_data.loc[:, ls_focus]
    df_duplicate = df_summary.drop_duplicates()

    # 多列合并单列
    df_combine = df_data.loc[:,
                 [grp_column, CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[-1]]]
    df_combine['answer_rate'] = df_combine[CONFIG.RATE_COLUMN[0]].astype(str) + '(' + df_combine[
        CONFIG.RATE_COLUMN[-1]].astype(float).astype(str) + '%)'
    df_combined = df_combine.loc[:, [grp_column, 'answer_rate']]
    df_combined.rename(columns={'answer_rate': combin_name}, inplace=True)
    df_row_combine = df_combined.groupby(grp_column,
                                         as_index=False).aggregate(
        lambda x: list(x))
    print(df_row_combine)
    # 转置合并
    df_result = pd.merge(df_row_combine, df_duplicate, how='left', on=grp_column)
    df_result.sort_values(CONFIG.MEAN_COLUMN[2], ascending=0, inplace=True)
    return df_result

def row_combine(df_data, array_focus=[CONFIG.MEAN_COLUMN[2]], combin_name=CONFIG.COMBINE_RATE):
    if df_data.empty:
        return df_data

    # 非合并列、答题总人数
    df_summary = df_data.loc[:, array_focus]
    df_duplicate = df_summary.drop_duplicates()

    # 多列合并单列
    df_combine = df_data.loc[:,
                 [CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[-1]]]
    df_combine['answer_rate'] = df_combine[CONFIG.RATE_COLUMN[0]].astype(str) + '(' + df_combine[
        CONFIG.RATE_COLUMN[-1]].astype(float).astype(str) + '%)'
    df_combined = df_combine.loc[:, ['answer_rate']]
    df_combined.rename(columns={'answer_rate': combin_name}, inplace=True)
    row_combine  =';'.join(list(df_combined.loc[:,combin_name]))
    df_duplicate.insert(0,combin_name,row_combine)
    return df_duplicate



##################公式部分

def answer_college_value_rate(data, subject, eliminate_unknown=[], array_order=[], array_asc=[]):
    '''
    根据学院分组计算比例
    :param data: 源数据
    :param subject: 题号
    :param eliminate_unknown:需要剔除的选项
    :return:
    '''
    pd_count = Util.answer_grp_count(data, [CONFIG.BASE_COLUMN[0], subject], [CONFIG.BASE_COLUMN[0]])
    pd_value_count = Util.answer_grp_count(data, [CONFIG.BASE_COLUMN[0], subject],
                                           [CONFIG.BASE_COLUMN[0], subject])

    pd_left = pd.merge(pd_value_count, pd_count, on=CONFIG.BASE_COLUMN[0], how='left')
    # 结构重命名：'学院','答案', '回答此答案人数', '答题总人数'
    pd_left.columns = [CONFIG.GROUP_COLUMN[0], CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[1], CONFIG.RATE_COLUMN[2]]

    if not eliminate_unknown:
        # 为空无需剔除
        pd_left[CONFIG.RATE_COLUMN[-1]] = (pd_left[CONFIG.RATE_COLUMN[1]] / pd_left[CONFIG.RATE_COLUMN[2]] * 100).round(
            decimals=2)
    else:
        # 过滤要剔除元素的数据
        df_unknown = pd_left[pd_left[CONFIG.RATE_COLUMN[0]].isin(eliminate_unknown)][
            [CONFIG.GROUP_COLUMN[0], CONFIG.RATE_COLUMN[1]]]
        if df_unknown.empty:
            pd_left[CONFIG.RATE_COLUMN[-1]] = (
                    pd_left[CONFIG.RATE_COLUMN[1]] / pd_left[CONFIG.RATE_COLUMN[2]] * 100).round(
                decimals=2)
        else:
            df_unknown.rename(columns={CONFIG.RATE_COLUMN[1]: 'unknown'}, inplace=True)
            pd_left = pd.merge(pd_left, df_unknown, how='left', on=CONFIG.GROUP_COLUMN[0])
            pd_left.fillna(0, inplace=True)
            pd_left[CONFIG.RATE_COLUMN[2]] = pd_left[CONFIG.RATE_COLUMN[2]] - pd_left['unknown']
            pd_left.drop(['unknown'], axis='columns', inplace=True)
            pd_left[CONFIG.RATE_COLUMN[-1]] = (
                    pd_left[CONFIG.RATE_COLUMN[1]] / pd_left[CONFIG.RATE_COLUMN[2]] * 100).round(
                decimals=2)

    if array_order:
        pd_left.sort_values(array_order, ascending=array_asc, inplace=True)

    pd_left[CONFIG.RATE_COLUMN[-1]] = pd_left.loc[:, CONFIG.RATE_COLUMN[-1]].map(lambda x: '%.2f%%' % x)

    return pd_left


def answer_single_value_rate(data, subject, single_grp, eliminate_unknown=[], array_order=[], array_asc=[]):
    '''
    根据分组条件计算比例
    :param data:
    :param subject:
    :param single_grp:
    :param eliminate_unknown:
    :return:
    '''
    pd_count = Util.answer_grp_count(data, [single_grp, subject], [single_grp])
    pd_value_count = Util.answer_grp_count(data, [single_grp, subject],
                                           [single_grp, subject])

    pd_left = pd.merge(pd_value_count, pd_count, on=single_grp, how='left')
    # 结构重命名：'分组','答案', '回答此答案人数', '答题总人数'
    pd_left.columns = [CONFIG.GROUP_COLUMN[-1], CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[1], CONFIG.RATE_COLUMN[2]]

    if not eliminate_unknown:
        pd_left[CONFIG.RATE_COLUMN[-1]] = (pd_left[CONFIG.RATE_COLUMN[1]] / pd_left[CONFIG.RATE_COLUMN[2]] * 100).round(
            decimals=2)
    else:
        # 过滤要剔除元素的数据
        df_unknown = pd_left[pd_left[CONFIG.RATE_COLUMN[0]].isin(eliminate_unknown)][
            [CONFIG.GROUP_COLUMN[-1], CONFIG.RATE_COLUMN[1]]]
        if df_unknown.empty:
            pd_left[CONFIG.RATE_COLUMN[-1]] = (
                    pd_left[CONFIG.RATE_COLUMN[1]] / pd_left[CONFIG.RATE_COLUMN[2]] * 100).round(
                decimals=2)
        else:
            df_unknown.rename(columns={CONFIG.RATE_COLUMN[1]: 'unknown'}, inplace=True)
            pd_left = pd.merge(pd_left, df_unknown, how='left', on=CONFIG.GROUP_COLUMN[-1])
            pd_left.fillna(0, inplace=True)
            pd_left[CONFIG.RATE_COLUMN[2]] = pd_left[CONFIG.RATE_COLUMN[2]] - pd_left['unknown']
            pd_left.drop(['unknown'], axis='columns', inplace=True)
            pd_left[CONFIG.RATE_COLUMN[-1]] = (
                    pd_left[CONFIG.RATE_COLUMN[1]] / pd_left[CONFIG.RATE_COLUMN[2]] * 100).round(
                decimals=2)

    if array_order:
        pd_left.sort_values(array_order, ascending=array_asc, inplace=True)

    pd_left[CONFIG.RATE_COLUMN[-1]] = pd_left.loc[:, CONFIG.RATE_COLUMN[-1]].map(lambda x: '%.2f%%' % x)

    return pd_left


def answer_major_value_rate(data, subject, eliminate_unknown=[], array_order=[], array_asc=[]):
    '''
    根据专业分组，计算比例
    :param data:
    :param subject:
    :param eliminate_unknown:
    :return:
    '''
    pd_count = Util.answer_grp_count(data,
                                     [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1], subject],
                                     [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]])
    pd_value_count = Util.answer_grp_count(data,
                                           [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1], subject],
                                           [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1], subject])
    pd_left = pd.merge(pd_value_count, pd_count,
                       on=[CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]],
                       how='left')
    # 结构重命名：'学院','专业','答案', '回答此答案人数', '答题总人数'
    pd_left.columns = [CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1], CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[1],
                       CONFIG.RATE_COLUMN[2]]
    if eliminate_unknown:
        pd_left[CONFIG.RATE_COLUMN[-1]] = (pd_left[CONFIG.RATE_COLUMN[1]] / pd_left[CONFIG.RATE_COLUMN[2]] * 100).round(
            decimals=2)
    else:
        # 过滤要剔除元素的数据=> 答案列 ==某个值
        df_unknown = pd_left[pd_left[CONFIG.RATE_COLUMN[0]].isin(eliminate_unknown)][
            [CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1], CONFIG.RATE_COLUMN[1]]]
        if df_unknown.empty:
            pd_left[CONFIG.RATE_COLUMN[-1]] = (
                    pd_left[CONFIG.RATE_COLUMN[1]] / pd_left[CONFIG.RATE_COLUMN[2]] * 100).round(
                decimals=2)
        else:
            df_unknown.rename(columns={CONFIG.RATE_COLUMN[1]: 'unknown'}, inplace=True)
            pd_left = pd.merge(pd_left, df_unknown, how='left', on=[CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1]])
            pd_left.fillna(0, inplace=True)
            pd_left[CONFIG.RATE_COLUMN[2]] = pd_left[CONFIG.RATE_COLUMN[2]] - pd_left['unknown']
            pd_left.drop(['unknown'], axis='columns', inplace=True)
            pd_left[CONFIG.RATE_COLUMN[-1]] = (
                    pd_left[CONFIG.RATE_COLUMN[1]] / pd_left[CONFIG.RATE_COLUMN[2]] * 100).round(
                decimals=2)

    if array_order:
        pd_left.sort_values(array_order, ascending=array_asc, inplace=True)

    pd_left[CONFIG.RATE_COLUMN[-1]] = pd_left.loc[:, CONFIG.RATE_COLUMN[-1]].map(lambda x: '%.2f%%' % x)

    return pd_left


def answer_mean(data, subject):
    '''均值计算'''
    pd_count = Util.answer_count(data, subject)
    pd_sum = Util.answer_sum(data, subject)
    mean = (pd_sum / pd_count).round(decimals=2)
    # 返回 答题总人数，均值
    pd_mean = pd.DataFrame({CONFIG.MEAN_COLUMN[2]: [pd_count],
                            CONFIG.MEAN_COLUMN[-1]: [mean]})
    return pd_mean


def major_mean(data, subject):
    pd_source = pd.DataFrame(data, columns=[CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1], subject])
    # 处理空值，否则count_nonzero会将空值统计在内
    pd_source.dropna(inplace=True)
    grouped = pd_source.groupby([CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]], as_index=False)
    pd_result = grouped[subject].agg([np.mean, np.count_nonzero])
    formate = lambda x: "%.2f" % x
    pd_result['mean'] = pd_result['mean'].apply(formate)
    pd_result['count_nonzero'] = pd_result['count_nonzero'].astype('int')

    pd_result.reset_index(inplace=True)
    pd_result.columns = [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1], CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]]
    pd_result.sort_values(CONFIG.MEAN_COLUMN[2], ascending=0, inplace=True)

    return pd_result


def single_grp_mean(data, subject, single_grp, is_college=False):
    '''分组条件计算均值'''
    pd_source = pd.DataFrame(data, columns=[single_grp, subject])

    if is_college:
        grp_name = CONFIG.GROUP_COLUMN[0]
    else:
        grp_name = CONFIG.GROUP_COLUMN[-1]

    # 计算分组条件答题总人数
    # 处理空值，否则count_nonzero会将空值统计在内
    pd_source.dropna(inplace=True)
    grouped = pd_source.groupby(single_grp, as_index=False)
    pd_result = grouped[subject].agg([np.mean, np.count_nonzero])
    formate = lambda x: "%.2f" % x
    pd_result['mean'] = pd_result['mean'].apply(formate)
    pd_result['count_nonzero'] = pd_result['count_nonzero'].astype('int')

    pd_result.reset_index(inplace=True)
    pd_result.columns = [grp_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]]
    pd_result.sort_values(CONFIG.MEAN_COLUMN[2], ascending=0, inplace=True)
    return pd_result


def answer_period(data, subject, start, end, step):
    ind_500 = list(range(start, end + step, step))

    ind_500.insert(0, 0)
    ind_500.append(100000)

    income = data['B6']
    counts = income.count()
    period = pd.cut(income.values, ind_500)

    period_counts = period.value_counts()
    pd_period = pd.DataFrame({CONFIG.RATE_COLUMN[0]: period_counts.index,
                              CONFIG.RATE_COLUMN[1]: period_counts.values})
    pd_period[CONFIG.RATE_COLUMN[-1]] = (pd_period[CONFIG.RATE_COLUMN[1]] / counts * 100).round(2)
    pd_period[CONFIG.RATE_COLUMN[2]] = counts

    pd_period[CONFIG.RATE_COLUMN[-1]] = pd_period.loc[:,CONFIG.RATE_COLUMN[-1]].map(lambda x: '%.2f%%' % x)

    return pd_period


def parse_measure(measure_type):
    if CONFIG.ANSWER_TYPE_MEET == measure_type:
        return CONFIG.ANSWER_NORMAL_MEET
    elif CONFIG.ANSWER_TYPE_RELATIVE == measure_type:
        return CONFIG.ANSWER_NORMAL_RELATIVE
    elif CONFIG.ANSWER_TYPE_SATISFY == measure_type:
        return CONFIG.ANSWER_NORMAL_SATISFY
    elif CONFIG.ANSWER_TYPE_IMPORTANT == measure_type:
        return CONFIG.ANSWER_NORMAL_IMPORTANT
    elif CONFIG.ANSWER_TYPE_PLEASED == measure_type:
        return CONFIG.ANSWER_NORMAL_PLEASED
    elif CONFIG.ANSWER_TYPE_MEET_V == measure_type:
        return CONFIG.ANSWER_NORMAL_MEET_V
    elif CONFIG.ANSWER_TYPE_HELP == measure_type:
        return CONFIG.ANSWER_NORMAL_HELP
    elif CONFIG.ANSWER_TYPE_FEEL == measure_type:
        return CONFIG.ANSWER_NORMAL_FEEL


def parse_measure_name(measure_type):
    if CONFIG.ANSWER_TYPE_MEET == measure_type:
        return CONFIG.MEASURE_NAME_MEET
    elif CONFIG.ANSWER_TYPE_RELATIVE == measure_type:
        return CONFIG.MEASURE_NAME_RELATIVE
    elif CONFIG.ANSWER_TYPE_SATISFY == measure_type:
        return CONFIG.MEASURE_NAME_SATISFY
    elif CONFIG.ANSWER_TYPE_IMPORTANT == measure_type:
        return CONFIG.MEASURE_NAME_IMPORTANT
    elif CONFIG.ANSWER_TYPE_PLEASED == measure_type:
        return CONFIG.MEASURE_NAME_PLEASED
    elif CONFIG.ANSWER_TYPE_MEET_V == measure_type:
        return CONFIG.MEASURE_NAME_MEET_V
    elif CONFIG.ANSWER_TYPE_HELP == measure_type:
        return CONFIG.MEASURE_NAME_HELP
    elif CONFIG.ANSWER_TYPE_FEEL == measure_type:
        return CONFIG.MEASURE_NAME_FEEL


def parse_measure_score(measure_type):
    if CONFIG.ANSWER_TYPE_MEET == measure_type:
        return CONFIG.ANSWER_SCORE_DICT_MEET
    elif CONFIG.ANSWER_TYPE_RELATIVE == measure_type:
        return CONFIG.ANSWER_SCORE_DICT_RELATIVE
    elif CONFIG.ANSWER_TYPE_SATISFY == measure_type:
        return CONFIG.ANSWER_SCORE_DICT_SATISFY
    elif CONFIG.ANSWER_TYPE_IMPORTANT == measure_type:
        return CONFIG.ANSWER_SCORE_DICT_IMPORTANT
    elif CONFIG.ANSWER_TYPE_PLEASED == measure_type:
        return CONFIG.ANSWER_SCORE_DICT_PLEASED
    elif CONFIG.ANSWER_TYPE_MEET_V == measure_type:
        return CONFIG.ANSWER_SCORE_DICT_MEET_V
    elif CONFIG.ANSWER_TYPE_HELP == measure_type:
        return CONFIG.ANSWER_SCORE_DICT_HELP
    elif CONFIG.ANSWER_TYPE_FEEL == measure_type:
        return CONFIG.ANSWER_SCORE_DICT_FEEL


def answer_five_rate(data, subject, measure_type):
    '''某题五维占比'''
    # step1：各个答案占比(无法评价已被清理)
    pd_five_rate = answer_rate(data, subject)

    pd_five_rate['比例'] = (pd_five_rate['回答此答案人数'] / pd_five_rate['答题总人数'] * 100).round(2)

    # step3: 相关度/满意度/符合度
    ls_measure = parse_measure(measure_type)
    dict_measure_score = parse_measure_score(measure_type)
    measure_name = parse_measure_name(measure_type)

    pd_measure = pd_five_rate[pd_five_rate['答案'].isin(ls_measure[0:3])]
    measure_rate = pd_measure['比例'].sum().round(decimals=2)
    pd_five_rate[measure_name] = measure_rate

    # step4: 均值
    pd_five_rate['measure_score'] = pd_five_rate['答案']
    pd_five_rate.replace({'measure_score': dict_measure_score}, inplace=True)
    pd_five_rate['measure_score'] = pd_five_rate['回答此答案人数'] * pd_five_rate['measure_score']
    alpha_x = pd_five_rate['measure_score'].sum()

    pd_five_rate['均值'] = (alpha_x / pd_five_rate['答题总人数']).round(decimals=2)

    pd_five_rate.drop('measure_score', axis='columns', inplace=True)

    pd_five_rate[CONFIG.RATE_COLUMN[-1]] = pd_five_rate.loc[:, CONFIG.RATE_COLUMN[-1]].map(lambda x: '%.2f%%' % x)
    pd_five_rate[measure_name] = pd_five_rate.loc[:,measure_name].map(lambda x: '%.2f%%' % x)

    return pd_five_rate


def answer_five_rate_single_grp(data, subject, grp, measure_type):
    '''某题单维分组的五维占比'''

    if grp == CONFIG.BASE_COLUMN[0]:
        grp_name = CONFIG.GROUP_COLUMN[0]
    else:
        grp_name = CONFIG.GROUP_COLUMN[-1]

    # 分组算总数
    pd_total = Util.answer_grp_count(data, [grp, subject], [grp])
    pd_total.columns = [grp_name, '答题总人数']
    # 分组算各答案分布
    pd_distribution = Util.answer_grp_count(data, [grp, subject], [grp, subject])
    pd_distribution.columns = [grp_name, '答案', '回答此答案人数']
    # 合并答案、回答此答案人数、答题总人数
    pd_left_rate = pd.merge(pd_distribution, pd_total, how='left', on=grp_name, validate='many_to_one')
    pd_left_rate['比例'] = (pd_left_rate['回答此答案人数'] / pd_left_rate['答题总人数'] * 100).round(2)

    # step3: 相关度/满意度/符合度
    ls_measure = parse_measure(measure_type)
    dict_measure_score = parse_measure_score(measure_type)
    measure_name = parse_measure_name(measure_type)

    pd_measure = pd_left_rate[pd_left_rate['答案'].isin(ls_measure[0:3])]
    pd_measure_sum = Util.answer_grp_sum(pd_measure, [grp_name, '比例'], [grp_name])

    pd_left_rate_measure = pd.merge(pd_left_rate, pd_measure_sum, on=grp_name, how='left', suffixes=['', '_y'])
    pd_left_rate_measure.rename(columns={'比例_y': measure_name}, inplace=True)

    # step6:计算alpha
    pd_left_rate_measure['measure_score'] = pd_left_rate_measure['答案']
    pd_left_rate_measure.replace({'measure_score': dict_measure_score}, inplace=True)

    pd_left_rate_measure['measure_score'] = pd_left_rate_measure['回答此答案人数'] * pd_left_rate_measure['measure_score']
    pd_measure_sum = Util.answer_grp_sum(pd_left_rate_measure, [grp_name, 'measure_score'], [grp_name])

    # step5:计算mean
    pd_left_mean = pd.merge(pd_left_rate_measure, pd_measure_sum, how='left', on=grp_name, suffixes=['', '_y'])
    pd_left_mean['mean'] = (pd_left_mean['measure_score_y'] / pd_left_mean['答题总人数']).round(2)
    pd_left_mean.rename(columns={'mean': '均值'}, inplace=True)
    pd_left_mean.drop('measure_score', axis='columns', inplace=True)
    pd_left_mean.drop('measure_score_y', axis='columns', inplace=True)
    pd_left_mean[CONFIG.RATE_COLUMN[-1]] = pd_left_mean.loc[:, CONFIG.RATE_COLUMN[-1]].map(lambda x: '%.2f%%' % x)
    pd_left_mean[measure_name] = pd_left_mean.loc[:, measure_name].map(lambda x: '%.2f%%' % x)
    return pd_left_mean


def answer_five_rate_major_grp(data, subject, measure_type):
    '''某题按专业分组的五维占比'''

    grp_column = list(CONFIG.COLLEGE_MAJOR)
    relative_column = list(CONFIG.COLLEGE_MAJOR)
    relative_column.append(subject)
    print(relative_column)
    # 分组算总数

    pd_total = Util.answer_grp_count(data, relative_column, grp_column)
    pd_total.columns = ['学院', '专业', '答题总人数']
    # 分组算各答案分布
    pd_distribution = Util.answer_grp_count(data, relative_column, relative_column)
    pd_distribution.columns = ['学院', '专业', '答案', '回答此答案人数']

    # 合并答案、回答此答案人数、答题总人数
    pd_left_rate = pd.merge(pd_distribution, pd_total, how='left', on=['学院', '专业'], validate='many_to_one')
    pd_left_rate['比例'] = (pd_left_rate['回答此答案人数'] / pd_left_rate['答题总人数'] * 100).round(2)

    # step3: 相关度/满意度/符合度
    ls_measure = parse_measure(measure_type)
    dict_measure_score = parse_measure_score(measure_type)
    measure_name = parse_measure_name(measure_type)

    pd_measure = pd_left_rate[pd_left_rate['答案'].isin(ls_measure[0:3])]
    pd_measure_sum = Util.answer_grp_sum(pd_measure, ['学院', '专业', '比例'], ['学院', '专业'])

    pd_left_rate_measure = pd.merge(pd_left_rate, pd_measure_sum, on=['学院', '专业'], how='left', suffixes=['', '_y'])
    pd_left_rate_measure.rename(columns={'比例_y': measure_name}, inplace=True)

    # step6:计算alpha
    pd_left_rate_measure['measure_score'] = pd_left_rate_measure['答案']
    pd_left_rate_measure.replace({'measure_score': dict_measure_score}, inplace=True)

    pd_left_rate_measure['measure_score'] = pd_left_rate_measure['回答此答案人数'] * pd_left_rate_measure['measure_score']
    pd_measure_sum = Util.answer_grp_sum(pd_left_rate_measure, ['学院', '专业', 'measure_score'], ['学院', '专业'])

    # step5:计算mean
    pd_left_mean = pd.merge(pd_left_rate_measure, pd_measure_sum, how='left', on=['学院', '专业'], suffixes=['', '_y'])
    pd_left_mean['mean'] = (pd_left_mean['measure_score_y'] / pd_left_mean['答题总人数']).round(2)
    pd_left_mean.rename(columns={'mean': '均值'}, inplace=True)
    pd_left_mean.drop('measure_score', axis='columns', inplace=True)
    pd_left_mean.drop('measure_score_y', axis='columns', inplace=True)
    pd_left_mean[CONFIG.RATE_COLUMN[-1]] = pd_left_mean.loc[:, CONFIG.RATE_COLUMN[-1]].map(lambda x: '%.2f%%' % x)
    pd_left_mean[measure_name] = pd_left_mean.loc[:, measure_name].map(lambda x: '%.2f%%' % x)
    return pd_left_mean
