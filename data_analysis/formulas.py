#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'formulas.py'

__author__ = 'kuoren'

import pandas as pd
import data_analysis.config as CONFIG
from data_cleansing.logging import *

logger = get_logger(__name__)


def formula_rate(data, subject, top=0):
    """

    AnswerRate 计算某题的答案占比
    :param data: 数据
    :param subject: 题号
    :return: '答案', '比例', '答题总人数',
    """

    # 答题总人数
    count = data[subject].count()
    if count:
        # 答案占比
        df_rate = data[subject].value_counts()
        df_rate = pd.DataFrame({CONFIG.RATE_COLUMN[0]: df_rate.index,
                                CONFIG.RATE_COLUMN[1]: df_rate.values,
                                CONFIG.RATE_COLUMN[-1]: df_rate.values / count
                                })
    else:
        df_rate = pd.DataFrame({CONFIG.RATE_COLUMN[0]: [''],
                                CONFIG.RATE_COLUMN[1]: [0],
                                CONFIG.RATE_COLUMN[-1]: [0]
                                })
    df_rate[CONFIG.RATE_COLUMN[2]] = count
    # 答题总人数为0时，出现NaN值
    df_rate.fillna(0, inplace=True)
    if top:
        df_rate.sort_values(CONFIG.RATE_COLUMN[-1], ascending=0, inplace=True)
        df_rate = df_rate.head(top)
    return df_rate


def formula_rate_grp_top(data, subject, grp, top=5):
    """
    分组取top n
    """
    # 分组算总数
    df_count = data.groupby(grp)[subject].count()
    df_count = df_count.to_frame(name=CONFIG.RATE_COLUMN[2])
    df_count.reset_index(inplace=True)
    # 分组算各答案分布
    sub_grp = grp.copy()
    sub_grp.append(subject)
    df_rate = data.groupby(sub_grp)[subject].count()
    df_rate = df_rate.to_frame(name=CONFIG.RATE_COLUMN[1])
    df_rate.reset_index(inplace=True)
    df_merge = pd.merge(df_rate, df_count, how='left', on=grp)
    print(df_merge)

    # 计算比例
    df_merge[CONFIG.RATE_COLUMN[-1]] = df_merge[CONFIG.RATE_COLUMN[1]] / df_merge[CONFIG.RATE_COLUMN[2]]
    df_merge.rename(columns={subject: CONFIG.RATE_COLUMN[0]}, inplace=True)
    df_merge.fillna(0, inplace=True)

    if top:
        df_merge.sort_values(CONFIG.RATE_COLUMN[-1], ascending=0, inplace=True)
        df_merge = df_merge.groupby(grp, as_index=False).head(top)

    return df_merge


def formula_rate_grp(data, subject, grp):
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
    df_rate.reset_index(inplace=True)
    return df_rate


def formula_five_rate(data, subject, measure_type):
    """
    五维占比
    :param data:
    :param subject:
    :param measure_type:
    :return:
    """
    # step1：各个答案占比
    df_rate = formula_rate(data, subject)
    # 行转列
    df_t = formate_rate_t(df_rate)
    # 相关度/满意度/符合度
    ls_measure = parse_measure(measure_type)
    dict_measure_score = parse_measure_score(measure_type)
    measure_name = parse_measure_name(measure_type)
    # 列重排
    order_cols=[col for col in ls_measure if col in df_t.columns]
    df_t = df_t[order_cols]
    # step3: 度量值
    measure_cols=[col for col in ls_measure[0:3] if col in df_t.columns]
    measure_rate = 0
    for measure in measure_cols:
        measure_rate = measure_rate + df_t[measure]
    df_t[measure_name] = measure_rate

    # step4: 均值
    mean = data[subject].map(dict_measure_score).mean()
    df_t[CONFIG.MEAN_COLUMN[-1]] = mean
    if df_rate.empty:
        df_t[CONFIG.MEAN_COLUMN[2]] = 0
    else:
        df_t[CONFIG.MEAN_COLUMN[2]] = df_rate.loc[0, CONFIG.RATE_COLUMN[2]]

    # 列重排
    order_cols = [col for col in ls_measure if col in df_t.columns]
    order_cols.extend([measure_name,CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]])
    df_t = df_t[order_cols]
    return df_t


def formula_five_rate_grp(data, subject, grp, measure_type):
    """
    分组计算某题的五维占比
    :param data:
    :param subject:
    :param grp:
    :param measure_type:
    :return:
    """

    # 答案占比
    df_rate = formula_rate_grp(data, subject, grp)
    # 相关度/满意度/符合度
    ls_measure = parse_measure(measure_type)
    dict_measure_score = parse_measure_score(measure_type)
    measure_name = parse_measure_name(measure_type)

    # step3: 度量值
    measure_cols = [col for col in ls_measure[0:3] if col in df_rate.columns]
    measure_rate = 0
    for measure in measure_cols:
        measure_rate = measure_rate + df_rate[measure]
    df_rate[measure_name] = measure_rate

    data.loc[:, "measure_score"] = data[subject]
    data.loc[:, "measure_score"] = data.loc[:, "measure_score"].map(dict_measure_score)
    df_mean = data.groupby(grp)["measure_score"].mean()
    # **必须要设置index，否则无法设置mean值
    df_rate = df_rate.set_index(grp)
    df_rate[CONFIG.MEAN_COLUMN[-1]] = df_mean

    # df_rate[CONFIG.MEAN_COLUMN[2]] = df_rate[CONFIG.MEAN_COLUMN[2]]
    df_rate.fillna(0, inplace=True)

    df_rate.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)
    df_rate.reset_index(inplace=True)
    # 列重排
    order_cols = list(grp)
    order_cols.extend([col for col in ls_measure if col in df_rate.columns])
    order_cols.extend([measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]])
    print(order_cols)
    df_rate = df_rate[order_cols]
    return df_rate


def formula_employe_rate(data):
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

    return pd_result


def formula_employe_rate_grp(data, array_grps):
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
    # 当未就业不存在时，就业率为100
    df_rate.fillna(1, inplace=True)
    # 就业率 答题总人数
    df_merge = pd.DataFrame({CONFIG.EMPLOYEE_RATE_COLUMN: df_rate,
                             CONFIG.RATE_COLUMN[2]: df_count})
    df_merge.fillna(0, inplace=True)
    df_merge.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)
    df_merge.reset_index(inplace=True)
    return df_merge


def formula_mean(data, subject):
    '''
    计算某一题均值
    :param data:
    :param subject:
    :return: 均值 答题总人数
    '''
    # 均值 答题总人数
    df_mean = pd.DataFrame({CONFIG.MEAN_COLUMN[-1]: [data[subject].mean()],
                            CONFIG.MEAN_COLUMN[2]: [data[subject].count()]})
    return df_mean


def formula_mean_grp(data, subject, grp):
    """
    分组计算均值
    :param data:
    :param subject:
    :param grp:
    :return:分组列、 均值、答题总人数
    """
    df_count = data.groupby(grp)[subject].count()
    df_mean = data.groupby(grp)[subject].mean()
    df_result = pd.DataFrame({CONFIG.MEAN_COLUMN[-1]: df_mean,
                              CONFIG.MEAN_COLUMN[2]: df_count})
    df_result.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)
    df_result.fillna(0, inplace=True)
    df_result.reset_index(inplace=True)
    return df_result


def formula_answer_period(data, subject, start, period_num, step, max=100000):
    """
    统计答案区间占比
    :param data:
    :param subject: 题目
    :param start: 最小值
    :param period_num: 区间数
    :param step: 步长
    :param max: 不规则部分 ，end～max
    :return: 各区间、答题人数、比率、答题总人数
    """
    end = start + period_num * step
    # list 边界 [x,y)
    ls_period = list(range(start, end + step, step))
    # 0-start
    ls_period.insert(0, 0)
    # end-max
    ls_period.append(max)

    df_answer = data[subject]
    counts = df_answer.count()
    period = pd.cut(df_answer.values, ls_period)
    period_counts = period.value_counts()
    pd_period = pd.DataFrame({CONFIG.RATE_COLUMN[0]: period_counts.index,
                              CONFIG.RATE_COLUMN[1]: period_counts.values})
    pd_period[CONFIG.RATE_COLUMN[-1]] = (pd_period[CONFIG.RATE_COLUMN[1]] / counts).round(decimals=CONFIG.DECIMALS6)
    pd_period[CONFIG.RATE_COLUMN[2]] = counts
    # 格式化区间名称
    period_name = build_period_name(start, step, period_num, max)
    pd_period[CONFIG.RATE_COLUMN[0]] = pd_period.loc[:, CONFIG.RATE_COLUMN[0]].astype('str').map(period_name)
    # 转置
    df_t = formate_rate_t(pd_period)
    # 追加均值
    df_mean = formula_mean(data, subject)
    df_t[CONFIG.MEAN_COLUMN[-1]] = df_mean.loc[0, CONFIG.MEAN_COLUMN[-1]]
    return df_t


def formate_rate_t(df_data):
    """格式化：总体比率行转列"""
    if df_data.empty:
        return df_data
    # 答题总人数
    count = df_data.loc[0, CONFIG.RATE_COLUMN[2]]

    # 比例转置
    df_t = df_data.pivot_table(CONFIG.RATE_COLUMN[-1], index=None,
                               columns=CONFIG.RATE_COLUMN[0])
    colums=list(df_t.columns)

    df_t[CONFIG.RATE_COLUMN[2]] = count
    return df_t


def formate_row_combine(df_data, array_focus=[CONFIG.MEAN_COLUMN[2]],
                        combin_name=CONFIG.COMBINE_RATE):
    """合并的前提，已经计算出结果"""
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


def formate_grp_row_combine(df_data, array_focus=[CONFIG.MEAN_COLUMN[2]],
                            combin_name=CONFIG.COMBINE_RATE, array_grps=[]):
    """分组合并"""
    if df_data.empty:
        return df_data

    # 非合并列 学院、专业、答题总人数
    ls_focus = array_focus.copy()
    ls_focus.extend(array_grps)
    df_summary = df_data.loc[:, ls_focus]
    df_duplicate = df_summary.drop_duplicates()

    # 多列合并单列
    combine_cols = [CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[-1]]
    combine_cols.extend(array_grps)
    df_combine = df_data.loc[:, combine_cols]
    df_combine['answer_rate'] = df_combine[CONFIG.RATE_COLUMN[0]].astype(str) + '(' + (df_combine[
                                                                                           CONFIG.RATE_COLUMN[
                                                                                               -1]] * 100).map(
        lambda x: '%.2f%%' % x) + ')'
    combine_after_cols = ['answer_rate']
    combine_after_cols.extend(array_grps)
    df_combined = df_combine.loc[:, combine_after_cols]
    df_combined.rename(columns={'answer_rate': combin_name}, inplace=True)
    df_row_combine = df_combined.groupby(array_grps, as_index=False).aggregate(lambda x: ';'.join(list(x)))
    # 转置合并 ';'.join(list(df_combined.loc[:, combin_name]))
    df_result = pd.merge(df_row_combine, df_duplicate, how='left', on=array_grps)
    df_result.sort_values(CONFIG.MEAN_COLUMN[2], ascending=0, inplace=True)

    return df_result


def multi_answer_count(data, subject):
    """多选题 答题人数统计"""
    multi_column = multi_columns(data, subject)
    df_answer = data.loc[:, multi_column]
    df_answer.dropna(how='all', inplace=True)
    df_answer.fillna(0, inplace=True)
    answer_count = df_answer.loc[:, multi_column[0]].count()
    return answer_count


def multi_columns(data, subject, max_times=0):
    """多选题的选项列"""
    multi_column = []
    for col in data.columns:
        if subject in str(col):
            multi_column.append(col)

    if max_times:
        multi_column = multi_column[0:max_times]

    return multi_column


def ability_distribution(data, subject):
    """能力综合题"""
    multi_column = multi_columns(data, subject)
    df_answer = data.loc[:, multi_column]
    multi_grp_column = [x[0:x.rindex('-') + 1] for x in multi_column]
    multi_grp_column = list(set(multi_grp_column))
    df_init = pd.DataFrame()  # 创建一个空的dataframe
    for item in multi_grp_column:
        df_ability = ability_item_distribution(df_answer, item)
        df_init = pd.concat([df_init, df_ability])
    return df_init


def ability_item_distribution(data, subject):
    '''能力题 答题人数，能力水平分析'''
    # step1 答题总人数 N2
    answer_count = multi_answer_count(data, subject)

    multi_column = multi_columns(data, subject)
    # 单项能力水平题目数量N1
    item_size = len(multi_column)
    # 结果集
    df_answer = data[multi_column].copy()
    df_answer.dropna(how='all', inplace=True)
    item_ability = 0
    for col in multi_column:
        # 反向分
        if col in CONFIG.ABILITY_REVERSE:
            df_answer[col + '_score'] = df_answer.loc[:, col].map(CONFIG.ABILITY_SCORE_REVERSE)
        else:
            df_answer[col + '_score'] = df_answer.loc[:, col].map(CONFIG.ABILITY_SCORE)
        item_ability = item_ability + df_answer.loc[:, col + '_score'].sum() / df_answer.loc[:, col + '_score'].count()
    ability = (item_ability / item_size).round(CONFIG.DECIMALS2)
    df_result = pd.DataFrame({CONFIG.RATE_COLUMN[0]: [subject[0:subject.rindex('-')]],
                              CONFIG.ABILITY_COLUMN: [ability],
                              CONFIG.RATE_COLUMN[2]: [answer_count]})
    return df_result

def formulas_overall(df, except_cols, method, grp_cols=[]):
    nums = []
    others = []
    cols = df.columns
    for col in cols:
        if col in except_cols or col in grp_cols:
            continue
        if col.find(CONFIG.RATE_COLUMN[2]) >= 0:
            nums.append(col)
        else:
            others.append(col)
    if grp_cols:
        grp_num=list(grp_cols)
        grp_num.extend(nums)
        grp_other=list(grp_cols)
        grp_other.extend(others)
        print(grp_num)
        print(grp_other)
        df_num = df.loc[:, grp_num].groupby(grp_cols).agg(['sum'])
        df_mean = df.loc[:, grp_other].groupby(grp_cols).agg(['mean'])
        df_num.reset_index(inplace=True)
        df_mean.reset_index(inplace=True)
        df_sum = pd.merge(df_mean,df_num, on=grp_cols)
        df_sum.reset_index(inplace=True)
        print('grp')
        print(df_sum)


    else:
        df_num = df.loc[:, nums].agg(['max'])
        df_mean = df.loc[:, others].agg(['mean'])
        df_num.reset_index(inplace=True)
        df_mean.reset_index(inplace=True)
        df_sum = pd.concat([df_num, df_mean], axis=1)
        print('not grp')
        print(df_sum)
        nums.extend(others)
        df_sum = df_sum[nums]
    return df_sum

def parse_ability_score(column_name):
    '''解析能力分值'''
    if column_name in CONFIG.ABILITY_REVERSE:
        return CONFIG.ABILITY_SCORE_REVERSE
    else:
        return CONFIG.ABILITY_SCORE


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


def build_period_name(start, step, period_n, max=100000):
    key = '(0, {}]'.format(start)
    val = '{}元及以下'.format(start)
    name = {key: val}
    for i in range(0, period_n):
        key = '({}, {}]'.format(start + i * step, start + (i + 1) * step)
        val = '{}-{}元'.format(start + i * step, start + (i + 1) * step)
        name[key] = val
    key = '({}, {}]'.format(start + period_n * step, max)
    val = '{}元及以上'.format(start + period_n * step + 1)
    name[key] = val
    return name

def formula_total(data):
    """总体毕业生人数
    默认使用学号统计，如果学号不存在，则取第一列计数
    """
    if "学号" in data.columns:
        return data['学号'].count()
    else:
        return data.iloc[:,0].count()

def formula_grp_rate(data,tgt_col, grp):
    """

    分组计算占比
    :param data:
    :param grp:
    :return:
    """
    # 分组统计人数
    df_count = data.groupby(grp)[tgt_col].count()
    df_count=df_count.to_frame()
    # 计算比例
    df_count[CONFIG.RATE_COLUMN[-1]] = df_count/formula_total(data)
    df_count.rename(columns={tgt_col:CONFIG.RATE_COLUMN[1]}, inplace=True)
    df_count.reset_index(inplace=True)
    df_count.sort_values(CONFIG.RATE_COLUMN[-1], ascending=0, inplace=True)

    return df_count
