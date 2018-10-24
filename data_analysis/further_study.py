#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'further_study.py'

__author__ = 'kuoren'

import pandas as pd
import numpy as np
import data_analysis.utils as answerUtil
import data_analysis.read_excel_util as excelUtil
import data_analysis.config as config


def study_abroad_report(data, filePath):
    a2_count = answerUtil.answer_count(data, 'A2')
    study_value = answer_value_rate(data, 'F1')
    study_value['答A2题总人数'] = a2_count
    study_value.drop(config.VALUE_RATE_COLUMN[2:4], axis='columns', inplace=True)
    study_value[config.VALUE_RATE_COLUMN[-1]] = (
            study_value[config.VALUE_RATE_COLUMN[1]] / study_value['答A2题总人数'] * 100).round(decimals=2)
    excelUtil.writeExcel(study_value, filePath, '留学比列')

    study_satisfy = answer_five_rate(data, 'F2', 2)
    excelUtil.writeExcel(study_satisfy, filePath, '留学录取结果满意度')

    study_relative = answer_five_rate(data, 'F3', 1)
    excelUtil.writeExcel(study_relative, filePath, '留学专业一致性')

    change_study_reason = answer_value_rate(data, 'F4')
    excelUtil.writeExcel(change_study_reason, filePath, '跨专业升学原因')


def further_report(data, filePath):
    further_rate = answer_rate(data, 'A2', config.A2_ANSWER[3])
    excelUtil.writeExcel(further_rate, filePath, '总体国内升学比例')

    further_reason = answer_value_rate(data, 'E2')
    excelUtil.writeExcel(further_reason, filePath, '升学原因')

    further_satisfy = answer_five_rate(data, 'E1', 2)
    excelUtil.writeExcel(further_satisfy, filePath, '升学录取结果满意度')

    further_relative = answer_five_rate(data, 'E3', 1)
    excelUtil.writeExcel(further_relative, filePath, '升学专业相关度')

    change_reason = answer_value_rate(data, 'E4')
    excelUtil.writeExcel(change_reason, filePath, '跨专业升学原因')


def work_stability_report(data, filePath):
    change_times = answer_value_rate(data, 'B10-1')
    no_changes = change_times[change_times[config.VALUE_RATE_COLUMN[0]].isin([config.B10_1_ANSWER[0]])][
        [config.VALUE_RATE_COLUMN[-1]]]
    no_changes.fillna(0, inplace=True)
    change_times['离职率'] = 100 - no_changes
    excelUtil.writeExcel(change_times, filePath, '总体离职情况分布')

    college_changes = answer_college_value_rate(data, 'B10-1')
    college_no_change = college_changes[college_changes['答案'].isin([config.B10_1_ANSWER[0]])][['学院', '比例']]
    college_no_change['离职率'] = 100 - college_no_change['比例']
    college_no_change.drop('比例', axis='columns', inplace=True)
    college_changes_left = pd.merge(college_changes, college_no_change,
                                    how='left',
                                    on='学院')
    excelUtil.writeExcel(college_changes_left, filePath, '各学院离职情况')

    major_changes = answer_major_value_rate(data, 'B10-1')
    major_no_change = major_changes[major_changes['答案'].isin([config.B10_1_ANSWER[0]])][['学院', '专业', '比例']]
    major_no_change['离职率'] = 100 - major_no_change['比例']
    major_no_change.drop('比例', axis='columns', inplace=True)
    major_changes_left = pd.merge(major_changes, major_no_change,
                                  how='left',
                                  on=['学院', '专业'])
    excelUtil.writeExcel(major_changes_left, filePath, '各专业离职情况')

    change_reason = answer_value_rate(data, 'B10-2')
    excelUtil.writeExcel(change_reason, filePath, '更换工作原因')


def work_option_report(data, filePath):
    option = answer_value_rate(data, 'A3')
    no_option = option[option['答案'].isin([config.EXCEPTED_ANSWER])][[config.VALUE_RATE_COLUMN[1]]]
    no_option.fillna(0, inplace=True)
    option['有效人数'] = option[config.VALUE_RATE_COLUMN[2]] - no_option[config.VALUE_RATE_COLUMN[1]]

    option[config.VALUE_RATE_COLUMN[-1]] = (option[config.VALUE_RATE_COLUMN[1]] / option['有效人数'] * 100).round(
        decimals=2)
    excelUtil.writeExcel(option, filePath, '总体就业机会')

    college_changes = answer_college_value_rate(data, 'A3')
    college_no_change = college_changes[college_changes['答案'].isin([config.EXCEPTED_ANSWER])][
        ['学院', config.VALUE_RATE_COLUMN[1]]]

    pd_left = pd.merge(college_changes, college_no_change,
                       how='left',
                       on='学院',
                       )
    pd_left.fillna(0, inplace=True)

    pd_left[config.VALUE_RATE_COLUMN[-1]] = (pd_left[config.VALUE_RATE_COLUMN[1] + '_x'] / (
                pd_left[config.VALUE_RATE_COLUMN[2]] - pd_left[config.VALUE_RATE_COLUMN[1] + '_y']) * 100).round(
        decimals=2)
    excelUtil.writeExcel(pd_left, filePath, '各学院就业机会')

    major_changes = answer_major_value_rate(data, 'A3')
    major_no_change = major_changes[major_changes['答案'].isin([config.EXCEPTED_ANSWER])][
        ['学院', '专业', config.VALUE_RATE_COLUMN[1]]]
    pd_left_major = pd.merge(major_changes, major_no_change, how='left', on=['学院', '专业'])
    pd_left_major.fillna(0, inplace=True)
    pd_left_major[config.VALUE_RATE_COLUMN[-1]] = (pd_left_major[config.VALUE_RATE_COLUMN[1] + '_x'] / (
                pd_left_major[config.VALUE_RATE_COLUMN[2]] - pd_left_major[
            config.VALUE_RATE_COLUMN[1] + '_y']) * 100).round(decimals=2)

    excelUtil.writeExcel(pd_left_major, filePath, '各专业就业机会')


def non_employee_report(data, filePath):
    '''未就业报告'''
    # 各选项占比
    df_value_count = answer_value_rate(data, 'C1')
    excelUtil.writeExcel(df_value_count, filePath, '一直未就业分布')

    df_value_count1 = answer_value_rate(data, 'C2')
    excelUtil.writeExcel(df_value_count1, filePath, '未就业毕业生目前去向分布')
    return


def income_report(data, filePath):
    # mean
    pd_mean = answer_mean(data, 'B6')
    excelUtil.writeExcel(pd_mean, filePath, '总体月均收入')

    pd_college_mean = college_mean(data, 'B6')
    excelUtil.writeExcel(pd_college_mean, filePath, '各学院月均收入')

    pd_major_mean = major_mean(data, 'B6')
    excelUtil.writeExcel(pd_major_mean, filePath, '各专业月均收入')

    # 500
    start = 2000
    period_n = 4
    step = 500
    pd_500 = answer_period(data, 'B6', start, start + period_n * step, step)
    excelUtil.writeExcel(pd_500, filePath, '毕业生月均收入及薪酬分布_' + str(step))

    step = 1000
    pd_1000 = answer_period(data, 'B6', start, start + period_n * step, step)
    excelUtil.writeExcel(pd_1000, filePath, '毕业生月均收入及薪酬分布_' + str(step))

    step = 2000
    pd_2000 = answer_period(data, 'B6', start, start + period_n * step, step)
    excelUtil.writeExcel(pd_2000, filePath, '毕业生月均收入及薪酬分布_' + str(step))

    step = 1500
    pd_1500 = answer_period(data, 'B6', start, start + period_n * step, step)
    excelUtil.writeExcel(pd_1500, filePath, '毕业生月均收入及薪酬分布_' + str(step))
    return


def employee_industry_type(data, filePath):
    df_value_count = answer_value_rate(data, 'B1')
    excelUtil.writeExcel(df_value_count, filePath, '总体就业单位类型分布')

    college_value = answer_college_value_rate(data, 'B1')
    college_value.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    college_five = college_value.groupby('学院', as_index=False).head(5)
    excelUtil.writeExcel(college_five, filePath, '各学院就业单位类型分布')

    major_value = answer_major_value_rate(data, 'B1')
    major_value.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    major_five = major_value.groupby(['学院', '专业'], as_index=False).head(5)
    excelUtil.writeExcel(major_five, filePath, '各单位就业单位类型分布')

    return


def employee_industry_size(data, filePath):
    df_value_count = answer_value_rate(data, 'B2')
    excelUtil.writeExcel(df_value_count, filePath, '总体就业单位规模分布')

    college_value = answer_college_value_rate(data, 'B2')
    excelUtil.writeExcel(college_value, filePath, '各学院就业单位规模分布')

    major_value = answer_major_value_rate(data, 'B2')
    excelUtil.writeExcel(major_value, filePath, '各单位就业单位规模分布')

    return


def employee_region_report(data, filePath):
    df_value_count = answer_value_rate(data, 'B3-A')
    excelUtil.writeExcel(df_value_count, filePath, '总体就业省')

    province = '福建省'
    pd_province = data[data['B3-A'] == province]
    college_value = answer_value_rate(pd_province, 'B3-B')
    excelUtil.writeExcel(college_value, filePath, '省内就业城市')

    college_value = answer_college_value_rate(data, 'B3-A')
    college_value.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    college_five = college_value.groupby('学院', as_index=False).head(5)
    excelUtil.writeExcel(college_five, filePath, '各学院就业地区分布')

    pd_province_city = answer_college_value_rate(pd_province, 'B3-B')
    pd_province_city.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    province_college_five = pd_province_city.groupby('学院', as_index=False).head(5)
    excelUtil.writeExcel(province_college_five, filePath, '各学院省内就业地区分布')

    pd_birth = data[data['A1-A'] == province]
    # 生源地答题总人数
    birth_count = answerUtil.answer_count(pd_birth, 'B3-A')
    # 生源地在本地就业人数
    birth_value_count = answerUtil.answer_of_subject_count(pd_birth, 'B3-A', province)
    # 生源地当地比
    birth_value_rate = (birth_value_count / birth_count * 100).round(2)
    pd_birth_rate = pd.DataFrame({'生源地在本地就业人数': [birth_value_count],
                                  '生源地当地比': [birth_value_rate],
                                  '生源地外地比': [100 - birth_value_rate],
                                  '生源地答题总人数': birth_count})

    excelUtil.writeExcel(pd_birth_rate, filePath, '省内生源就业地区流向')

    pd_not_birth = data[data['A1-A'] != province]
    # 外地生源答题总人数
    not_birth_count = answerUtil.answer_count(pd_not_birth, 'B3-A')
    # 外地生源本地就业人数
    not_birth_local_count = answerUtil.answer_of_subject_count(pd_not_birth, 'B3-A', province)
    not_birth_local_rate = (not_birth_local_count / not_birth_count * 100).round(2)

    # 外地生源回生源地就业人数
    not_birth_birth_count = pd_not_birth[pd_not_birth['A1-A'] == pd_not_birth['B3-A']]['B3-A'].count()
    not_birth_birth_rate = (not_birth_local_count / not_birth_count * 100).round(2)

    pd_not_birth_rate = pd.DataFrame({'外地生源在本地就业人数': [not_birth_local_count],
                                      '外地生源在本地就业比例': [not_birth_local_rate],
                                      '外地生源回生源地就业人数': [not_birth_birth_count],
                                      '外地生源回生源地就业比例': [not_birth_birth_rate],
                                      '外地生源外地比': [100 - not_birth_local_rate - not_birth_birth_rate],
                                      '生源地答题总人数': not_birth_count})

    excelUtil.writeExcel(pd_not_birth_rate, filePath, '省外生源就业地区流向')

    pd_single_grp_mean = single_grp_mean(data, 'B6', 'B3-A')
    excelUtil.writeExcel(pd_single_grp_mean, filePath, '主要就业地区月均收入')

    pd_single_grp_city_mean = single_grp_mean(pd_province, 'B6', 'B3-B')
    excelUtil.writeExcel(pd_single_grp_city_mean, filePath, '省内主要就业城市月均收入')

    return

def employee_job(data,filePath):
    '''就业职业分布'''

    df_value_rate = answer_value_rate(data, 'B4-A')
    df_value_rate.sort_values('比例', ascending=0, inplace=True)
    excelUtil.writeExcel(df_value_rate, filePath, '总体就业职业分布')

    college_value = answer_college_value_rate(data, 'B4-A')
    college_value.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    college_five = college_value.groupby('学院', as_index=False).head(5)
    excelUtil.writeExcel(college_five, filePath, '各学院就业职业分布')

    major_value = answer_major_value_rate(data, 'B4-A')
    major_value.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    major_five = major_value.groupby(['学院', '专业'], as_index=False).head(5)
    excelUtil.writeExcel(major_five, filePath, '各单位就业职业分布')

    pd_single_grp_mean = single_grp_mean(data, 'B6', 'B4-A')
    excelUtil.writeExcel(pd_single_grp_mean, filePath, '主要就业职业月均收入')

    single_value = answer_single_value_rate(data, 'B9-1', 'B4-A')
    pd_relative = single_value[single_value['答案'].isin(config.ANSWER_NORMAL_2[0:3])]['比例'].sum()
    relativeName = '相关度'
    single_value[relativeName] = pd_relative
    excelUtil.writeExcel(single_value, filePath, '各就业职业专业相关度差异分析')

    single_value1 = answer_single_value_rate(data, 'B7-A', 'B4-A')
    pd_relative1 = single_value1[single_value1['答案'].isin(config.ANSWER_NORMAL_3[0:3])]['比例'].sum()
    relativeName1 = '满意度'
    single_value1[relativeName1] = pd_relative1
    excelUtil.writeExcel(single_value1, filePath, '各就业职业就业满意度差异分析')


    return

def school_satisfy_report(data, filePath):
    '''母校满意度报告'''

    five_rate = answer_five_rate(data, 'H7', 2)
    excelUtil.writeExcel(five_rate, filePath, '母校满意度')

    return

def school_recommed_report(data, filePath):
    '''母校推荐报告'''

    df_value_rate = answer_value_rate(data, 'H8')
    df_value_rate.sort_values('比例', ascending=0, inplace=True)
    excelUtil.writeExcel(df_value_rate, filePath, '母校推荐度')

    df_college_rate=answer_college_value_rate(data,'H8')
    df_college_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    df_college_rate_five = df_college_rate.groupby('学院', as_index=False).head(5)
    excelUtil.writeExcel(df_college_rate_five, filePath, '各学院母校推荐度')

    df_major_rate=answer_major_value_rate(data,'H8')
    df_major_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    df_major_rate_five = df_major_rate.groupby(['学院', '专业'], as_index=False).head(5)
    excelUtil.writeExcel(df_major_rate_five, filePath, '各专业母校推荐度')

    return

def employee_indurstry(data, filePath):
    '''就业行业分布'''
    data_a2 = data[data['A2'] == config.A2_ANSWER[0]]

    df_value_rate = answer_value_rate(data_a2, 'B5-A')
    df_value_rate.sort_values('比例', ascending=1, inplace=True)
    excelUtil.writeExcel(df_value_rate, filePath, '总体就业行业分布')

    df_college_rate=answer_college_value_rate(data_a2,'B5-A')
    df_college_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    df_college_rate_five = df_college_rate.groupby('学院', as_index=False).head(5)
    excelUtil.writeExcel(df_college_rate_five, filePath, '各学院就业行业分布')

    df_major_rate=answer_major_value_rate(data_a2,'B5-A')
    df_major_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    df_major_rate_five = df_major_rate.groupby(['学院', '专业'], as_index=False).head(5)
    excelUtil.writeExcel(df_major_rate_five, filePath, '各专业就业行业分布')

    pd_single_grp_mean = single_grp_mean(data_a2, 'B6', 'B5-A')
    excelUtil.writeExcel(pd_single_grp_mean, filePath, '主要就业行业月均收入')


    single_value = answer_single_value_rate(data_a2, 'B9-1','B5-A')
    pd_relative = single_value[single_value['答案'].isin(config.ANSWER_NORMAL_2[0:3])]['比例'].sum()
    relativeName = '相关度'
    single_value[relativeName] = pd_relative
    excelUtil.writeExcel(single_value, filePath, '各就业行业专业相关度差异分析')

    single_value1 = answer_single_value_rate(data_a2, 'B7-A', 'B5-A')
    pd_relative1 = single_value1[single_value1['答案'].isin(config.ANSWER_NORMAL_3[0:3])]['比例'].sum()
    relativeName1 = '满意度'
    single_value1[relativeName1] = pd_relative1
    excelUtil.writeExcel(single_value1, filePath, '各就业行业就业满意度差异分析')

    return

def employee_difficult_report(data, filePath):
    '''求职过程报告'''
    data_a2 = data[data['A2'].isin([config.A2_ANSWER[0],config.A2_ANSWER[2]])]

    df_value_rate = answer_value_rate(data_a2, 'D2')
    df_value_rate.sort_values('比例', ascending=0, inplace=True)
    excelUtil.writeExcel(df_value_rate, filePath, '求职困难')

    df_major_rate=answer_major_value_rate(data_a2,'D2')
    df_major_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    df_major_rate_five = df_major_rate.groupby(['学院', '专业'], as_index=False).head(3)
    excelUtil.writeExcel(df_major_rate_five, filePath, '各专业求职困难')

    df_value_rate1 = answer_value_rate(data_a2, 'D1')
    df_value_rate1.sort_values('比例', ascending=1, inplace=True)
    excelUtil.writeExcel(df_value_rate1, filePath, '求职成功途径')

    return


def business_report(data,filePath):
    '''自主创业报告'''
    business_rate = answer_rate(data, 'A2', config.A2_ANSWER[1])
    excelUtil.writeExcel(business_rate, filePath, '自主创业比例')

    multi_reason=0
    g3_a_count=answerUtil.answer_count(data,'G3-A')
    g3_b_count=answerUtil.answer_count(data,'G3-A')
    g3_c_count=answerUtil.answer_count(data,'G3-A')
    g3_d_count=answerUtil.answer_count(data,'G3-A')
    g3_e_count=answerUtil.answer_count(data,'G3-A')
    g3_d_count=answerUtil.answer_count(data,'G3-A')
    g3_e_count=answerUtil.answer_count(data,'G3-A')

    business_reason = answer_value_rate(data, 'G3')
    excelUtil.writeExcel(business_reason, filePath, '自主创业原因')

    further_satisfy = answer_five_rate(data, 'E1', 2)
    excelUtil.writeExcel(further_satisfy, filePath, '自主创业行业')

    further_relative = answer_five_rate(data, 'E3', 1)
    excelUtil.writeExcel(further_relative, filePath, '自主创业与所学专业')

    change_reason = answer_value_rate(data, 'E4')
    excelUtil.writeExcel(change_reason, filePath, '自主创业资金来源')

    change_reason = answer_value_rate(data, 'E4')
    excelUtil.writeExcel(change_reason, filePath, '自主创业困难')

    return




def answer_five_rate(data, subject, answerType):
    '''某一题五维占比'''
    # step1：各个答案占比
    pd_five_rate = answer_value_rate(data, subject)
    pd_five_rate.drop('比例', axis='columns', inplace=True)
    invalid_count = answerUtil.answer_of_subject_count(data, subject, config.EXCEPTED_ANSWER)
    pd_five_rate['比例'] = (pd_five_rate['回答此答案人数'] / (pd_five_rate['答题总人数'] - invalid_count) * 100).round(decimals=2)

    # step2: 相关度/满意度
    if answerType == 0:
        pd_relative = pd_five_rate[pd_five_rate['答案'].isin(config.ANSWER_NORMAL_1[0:3])]['比例'].sum()
        relativeName = '符合度'
    elif answerType == 1:
        pd_relative = pd_five_rate[pd_five_rate['答案'].isin(config.ANSWER_NORMAL_2[0:3])]['比例'].sum()
        relativeName = '相关度'
    elif answerType == 2:
        pd_relative = pd_five_rate[pd_five_rate['答案'].isin(config.ANSWER_NORMAL_3[0:3])]['比例'].sum()
        relativeName = '满意度'
    pd_five_rate[relativeName] = pd_relative

    pd_five_rate['val_score'] = pd_five_rate['答案']

    if answerType == 0:
        pd_five_rate.replace({'val_score': config.ANSWER_SCORE_DICT_1}, inplace=True)
    elif answerType == 1:
        pd_five_rate.replace({'val_score': config.ANSWER_SCORE_DICT_2}, inplace=True)
    elif answerType == 2:
        pd_five_rate.replace({'val_score': config.ANSWER_SCORE_DICT_3}, inplace=True)

    pd_five_rate['val_score'] = pd_five_rate['回答此答案人数'] * pd_five_rate['val_score']
    alpha_x = pd_five_rate['val_score'].sum()
    pd_five_rate['均值'] = (alpha_x / (pd_five_rate['答题总人数'] - invalid_count)).round(decimals=2)
    pd_five_rate.drop('val_score', axis='columns', inplace=True)
    return pd_five_rate


def answer_rate(data, subject, answer):
    '''某一题某个答案总体占比'''
    count = answerUtil.answer_count(data, subject);
    answer_count = answerUtil.answer_of_subject_count(data, subject, answer)
    rate = (answer_count / count * 100).round(decimals=2)
    title = "回答'{}'人数".format(answer)
    df = pd.DataFrame({title: [answer_count],
                       '答题总人数': [count],
                       '比例': [rate]})
    return df


def answer_value_rate(data, subject):
    '''各答案占比'''
    count = answerUtil.answer_count(data, subject);
    pd_value_count = answerUtil.answer_val_count(data, subject)
    pd_result = pd.DataFrame({'答案': pd_value_count.index,
                              '回答此答案人数': pd_value_count.values})
    pd_result['答题总人数'] = count
    pd_result['比例'] = (pd_result['回答此答案人数'] / pd_result['答题总人数'] * 100).round(decimals=2)
    return pd_result


def answer_college_value_rate(data, subject):
    pd_count = answerUtil.answer_grp_count(data, [config.BASE_COLUMN[0], subject], [config.BASE_COLUMN[0]])
    pd_value_count = answerUtil.answer_grp_count(data, [config.BASE_COLUMN[0], subject],
                                                 [config.BASE_COLUMN[0], subject])

    pd_left = pd.merge(pd_value_count, pd_count, on=config.BASE_COLUMN[0], how='left', suffixes=('_x', '_y'))
    pd_left.columns = ['学院', '答案', '回答此答案人数', '答题总人数']
    pd_left['比例'] = (pd_left['回答此答案人数'] / pd_left['答题总人数'] * 100).round(decimals=2)

    return pd_left

def answer_single_value_rate(data, subject, single_grp):
    pd_count = answerUtil.answer_grp_count(data, [single_grp, subject], [single_grp])
    pd_value_count = answerUtil.answer_grp_count(data, [single_grp, subject],
                                                 [single_grp, subject])

    pd_left = pd.merge(pd_value_count, pd_count, on=single_grp, how='left', suffixes=('_x', '_y'))
    pd_left.columns = ['分组', '答案', '回答此答案人数', '答题总人数']
    pd_left['比例'] = (pd_left['回答此答案人数'] / pd_left['答题总人数'] * 100).round(decimals=2)

    return pd_left


def answer_major_value_rate(data, subject):
    pd_count = answerUtil.answer_grp_count(data,
                                           [config.BASE_COLUMN[0], config.BASE_COLUMN[1], subject],
                                           [config.BASE_COLUMN[0], config.BASE_COLUMN[1]])
    pd_value_count = answerUtil.answer_grp_count(data,
                                                 [config.BASE_COLUMN[0], config.BASE_COLUMN[1], subject],
                                                 [config.BASE_COLUMN[0], config.BASE_COLUMN[1], subject])
    pd_left = pd.merge(pd_value_count, pd_count,
                       on=[config.BASE_COLUMN[0], config.BASE_COLUMN[1]],
                       how='left', suffixes=('_x', '_y'))
    pd_left.columns = ['学院', '专业', '答案', '回答此答案人数', '答题总人数']
    pd_left['比例'] = (pd_left['回答此答案人数'] / pd_left['答题总人数'] * 100).round(decimals=2)

    return pd_left


def answer_mean(data, subject):
    pd_count = answerUtil.answer_count(data, subject)
    pd_sum = answerUtil.answer_sum(data, subject)
    mean = (pd_sum / pd_count).round(decimals=2)
    pd_mean = pd.DataFrame({'答题总人数': [pd_count],
                            '均值': [mean],
                            'sum值': [pd_sum]})
    return pd_mean


def college_mean(data, subject):
    pd_source = pd.DataFrame(data, columns=[config.BASE_COLUMN[0], subject])
    grouped = pd_source.groupby(config.BASE_COLUMN[0], as_index=False)
    pd_result = grouped[subject].agg([np.sum, np.mean, np.count_nonzero])
    formate = lambda x: "%.2f" % x
    pd_result = pd_result.applymap(formate)
    return pd_result


def major_mean(data, subject):
    pd_source = pd.DataFrame(data, columns=[config.BASE_COLUMN[0], config.BASE_COLUMN[1], subject])
    grouped = pd_source.groupby([config.BASE_COLUMN[0], config.BASE_COLUMN[1]], as_index=False)
    pd_result = grouped[subject].agg([np.sum, np.mean, np.count_nonzero])
    formate = lambda x: "%.2f" % x
    pd_result = pd_result.applymap(formate)
    return pd_result

def single_grp_mean(data, subject, single_grp):
    pd_source = pd.DataFrame(data, columns=[single_grp, subject])
    grouped = pd_source.groupby(single_grp, as_index=False)
    pd_result = grouped[subject].agg([np.sum, np.mean, np.count_nonzero])
    formate = lambda x: "%.2f" % x
    pd_result = pd_result.applymap(formate)
    return pd_result

def answer_period(data, subject, start, end, step):
    ind_500 = list(range(start, end + step, step))

    ind_500.insert(0, 0)
    ind_500.append(100000)
    print(ind_500)

    income = data['B6']
    counts = income.count()
    print(counts)
    period = pd.cut(income.values, ind_500)
    period_counts = period.value_counts()
    pd_period = pd.DataFrame({'区间': period_counts.index,
                              '计数': period_counts.values})
    pd_period['比例'] = (pd_period['计数'] / counts * 100).round(2)
    print(pd_period)

    return pd_period



