#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'formulas.py'

__author__ = 'kuoren'

import pandas as pd
import numpy as np
import data_analysis.config as CONFIG
import data_analysis.utils as Util
from data_cleansing.logging import *

logger = get_logger(__name__)


def formulas_rate(data, subject):
    """

    AnswerRate 计算某题的答案占比
    :param data: 数据
    :param subject: 题号
    :return: '答案', '比例', '答题总人数',
    """

    # 答题总人数
    count = data[subject].count()
    # 答案占比
    df_rate = data[subject].value_counts()
    df_rate = pd.DataFrame({CONFIG.RATE_COLUMN[0]: df_rate.index,
                            CONFIG.RATE_COLUMN[1]: df_rate.values,
                            CONFIG.RATE_COLUMN[-1]: df_rate.values / count
                            })
    df_rate[CONFIG.RATE_COLUMN[2]] = count
    print(df_rate)
    return df_rate


def formulas_rate_grp(data, subject, grp):
    """

    AnswerRateGrp：分组计算某题的答案占比
    :param data:
    :param subject:
    :param grp:
    :return:
    """

    # 分组算总数
    df_count = data.groupby(grp)[subject].count()
    # 分组算各答案分布
    sub_grp = grp.copy()
    sub_grp.append(subject)
    df_rate = data.groupby(sub_grp)[subject].count().unstack(fill_value=0)
    # 计算比例
    df_rate = df_rate.apply(lambda x: x / df_count)
    df_rate[CONFIG.RATE_COLUMN[2]] = df_count
    df_rate.fillna(0, inplace=True)
    df_rate.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)
    return df_rate


def formulas_five_rate(data, subject, measure_type):
    """
    五维占比
    :param data:
    :param subject:
    :param measure_type:
    :return:
    """
    # step1：各个答案占比
    df_rate = formulas_rate(data, subject)
    # 行转列
    df_t = formate_rate_t(df_rate)
    # 相关度/满意度/符合度
    ls_measure = parse_measure(measure_type)
    dict_measure_score = parse_measure_score(measure_type)
    measure_name = parse_measure_name(measure_type)
    # 列重排
    df_t = df_t[ls_measure[0:5]]
    # step3: 度量值
    measure_rate = 0
    for measure in ls_measure[0:3]:
        measure_rate = measure_rate + df_t[measure]
    df_t[measure_name] = measure_rate

    # step4: 均值
    mean = data[subject].map(dict_measure_score).mean()
    df_t[CONFIG.MEAN_COLUMN[-1]] = mean
    df_t[CONFIG.MEAN_COLUMN[2]] = df_rate.loc[0, CONFIG.RATE_COLUMN[2]]

    return df_t


def formulas_five_rate_grp(data, subject, grp, measure_type):
    """
    分组计算某题的五维占比
    :param data:
    :param subject:
    :param grp:
    :return:
    """

    # 答案占比
    df_rate = formulas_rate_grp(data, subject,grp)
    # 相关度/满意度/符合度
    ls_measure = parse_measure(measure_type)
    dict_measure_score = parse_measure_score(measure_type)
    measure_name = parse_measure_name(measure_type)
    # 列重排
    df_sub = df_rate[ls_measure[0:5]]
    # step3: 度量值
    measure_rate = 0
    for measure in ls_measure[0:3]:
        measure_rate = measure_rate + df_rate[measure]
    df_sub[measure_name] = measure_rate

    data["measure_score"]=data[subject].map(dict_measure_score)
    df_mean=data.groupby(grp)["measure_score"].mean()
    df_sub[CONFIG.MEAN_COLUMN[-1]]=df_mean
    df_sub[CONFIG.MEAN_COLUMN[2]]=df_rate[CONFIG.MEAN_COLUMN[2]]
    df_sub.fillna(0, inplace=True)
    df_sub.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)
    print(df_sub)
    return df_sub


def formate_rate_t(df_data):
    """格式化：总体比率行转列"""
    if df_data.empty:
        return df_data
    # 答题总人数
    count = df_data.loc[0, CONFIG.RATE_COLUMN[2]]

    # 比例转置
    df_t = df_data.pivot_table(CONFIG.RATE_COLUMN[-1], index=None,
                               columns=CONFIG.RATE_COLUMN[0])
    df_t[CONFIG.RATE_COLUMN[2]] = count
    print(df_t)
    return df_t


def formulas_employe_rate(data):
    '''

    Employe rate:就业率
    公式：（就业人数-未就业人数）/答题总人数
    :param data:
    :return: 就业率 答题总人数
    '''
    subject = 'A2'

    # step1:答题总人数
    count = data[subject].count()

    # step2:回答"未就业"人数
    unemployee_count = data[data[subject] == CONFIG.A2_ANSWER[-1]][subject].count()

    employee_rate = ((count - unemployee_count) / count).round(decimals=CONFIG.DECIMALS6)
    # 就业率 答题总人数
    pd_result = pd.DataFrame({CONFIG.EMPLOYEE_RATE_COLUMN: [employee_rate],
                              CONFIG.RATE_COLUMN[2]: [count]})
    print(pd_result)
    return pd_result


def formulas_employe_rate_grp(data, array_grps):
    """
    Employe rate:各学院\专业\其他分组 就业率
    :param data:
    :param array_grps: 分组
    :return:
    """
    subject = 'A2'

    # step1:各分组 答题总人数
    df_count = data.groupby(array_grps)[subject].count()
    # step2:各分组 回答"未就业"人数
    df_unemployee = data[data[subject] == CONFIG.A2_ANSWER[-1]].groupby(array_grps)[subject].count()
    df_rate = (df_count - df_unemployee) / df_count
    # 就业率 答题总人数
    df_merge = pd.DataFrame({CONFIG.EMPLOYEE_RATE_COLUMN: df_rate,
                             CONFIG.RATE_COLUMN[2]: df_count})
    df_merge.fillna(0, inplace=True)
    df_merge.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)
    print(df_merge)
    return df_merge


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
    mean = (sum / count).round(decimals=CONFIG.DECIMALS2)
    # 均值 答题总人数
    pd_mean = pd.DataFrame({CONFIG.MEAN_COLUMN[2]: [count],
                            CONFIG.MEAN_COLUMN[-1]: [mean]})
    logger.info("formula_income_mean(薪酬均值)计算成功")
    return pd_mean


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
    df_combine['answer_rate'] = df_combine[CONFIG.RATE_COLUMN[0]].astype(str) + '(' + (df_combine[
                                                                                           CONFIG.RATE_COLUMN[
                                                                                               -1]] * 100).map(
        lambda x: '%.2f%%' % x) + ')'
    df_combined = df_combine.loc[:, [CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1], 'answer_rate']]
    df_combined.rename(columns={'answer_rate': combin_name}, inplace=True)
    df_row_combine = df_combined.groupby([CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1]],
                                         as_index=False).aggregate(
        lambda x: ';'.join(list(x)))
    # 转置合并 ';'.join(list(df_combined.loc[:, combin_name]))
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
    df_combine['answer_rate'] = df_combine[CONFIG.RATE_COLUMN[0]].astype(str) + '(' + (df_combine[
                                                                                           CONFIG.RATE_COLUMN[
                                                                                               -1]] * 100).map(
        lambda x: '%.2f%%' % x) + ')'
    df_combined = df_combine.loc[:, [CONFIG.GROUP_COLUMN[0], 'answer_rate']]
    df_combined.rename(columns={'answer_rate': combin_name}, inplace=True)
    df_row_combine = df_combined.groupby(CONFIG.GROUP_COLUMN[0],
                                         as_index=False).aggregate(
        lambda x: ';'.join(list(x)))
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
    df_combine['answer_rate'] = df_combine[CONFIG.RATE_COLUMN[0]].astype(str) + '(' + (df_combine[
                                                                                           CONFIG.RATE_COLUMN[
                                                                                               -1]] * 100).map(
        lambda x: '%.2f%%' % x) + ')'
    df_combined = df_combine.loc[:, [grp_column, 'answer_rate']]
    df_combined.rename(columns={'answer_rate': combin_name}, inplace=True)
    df_row_combine = df_combined.groupby(grp_column,
                                         as_index=False).aggregate(
        lambda x: ';'.join(list(x)))
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
    df_combine['answer_rate'] = df_combine[CONFIG.RATE_COLUMN[0]].astype(str) + '(' + (df_combine[
                                                                                           CONFIG.RATE_COLUMN[
                                                                                               -1]] * 100).map(
        lambda x: '%.2f%%' % x) + ')'
    df_combined = df_combine.loc[:, ['answer_rate']]
    df_combined.rename(columns={'answer_rate': combin_name}, inplace=True)
    row_combine = ';'.join(list(df_combined.loc[:, combin_name]))
    df_duplicate.insert(0, combin_name, row_combine)
    return df_duplicate

def answer_mean(data, subject):
    '''均值计算'''
    pd_count = Util.answer_count(data, subject)
    pd_sum = Util.answer_sum(data, subject)
    mean = (pd_sum / pd_count).round(decimals=CONFIG.DECIMALS2)
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
    pd_result['mean'] = pd_result['mean'].round(decimals=CONFIG.DECIMALS2)
    pd_result['count_nonzero'] = pd_result['count_nonzero'].astype('int')

    pd_result.reset_index(inplace=True)
    pd_result.columns = [CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1], CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]]
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
    pd_result['mean'] = pd_result['mean'].round(decimals=CONFIG.DECIMALS2)
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
    pd_period[CONFIG.RATE_COLUMN[-1]] = (pd_period[CONFIG.RATE_COLUMN[1]] / counts).round(decimals=CONFIG.DECIMALS6)
    pd_period[CONFIG.RATE_COLUMN[2]] = counts

    return pd_period


def percent(df_data):
    if df_data.empty:
        return df_data
    columns = [col for col in df_data.columns]
    elimite_cols = [CONFIG.MEAN_COLUMN[2], CONFIG.MEAN_COLUMN[-1],
                    CONFIG.MEAN_COLUMN[1], CONFIG.MEAN_COLUMN[0],
                    CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1], CONFIG.ABILITY_COLUMN,
                    CONFIG.GROUP_COLUMN[2], CONFIG.TOTAL_COLUMN]
    for column in elimite_cols:
        if column in columns:
            columns.remove(column)
    df_data.loc[:, columns] = df_data.loc[:, columns].applymap(lambda x: '%.2f%%' % x)

    return df_data


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
    elif CONFIG.ANSWER_TYPE_NUM == measure_type:
        return CONFIG.ANSWER_NORMAL_NUM


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
    elif CONFIG.ANSWER_TYPE_NUM == measure_type:
        return CONFIG.MEASURE_NAME_NUM
    else:
        return measure_type


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
    elif CONFIG.ANSWER_TYPE_NUM == measure_type:
        return CONFIG.ANSWER_SCORE_DICT_NUM
