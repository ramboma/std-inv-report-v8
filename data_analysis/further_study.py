#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'further_study.py'

__author__ = 'kuoren'

import pandas as pd
import numpy as np
import data_analysis.utils as answerUtil
import data_analysis.read_excel_util as excelUtil
import data_analysis.config as CONFIG
import data_analysis.formulas as formulas


def employee_indurstry(data, filePath):
    '''就业行业分布'''
    data_a2 = data[data['A2'] == CONFIG.A2_ANSWER[0]]

    subject='B5-B'
    df_value_rate = answer_value_rate(data_a2, subject)
    df_value_rate.sort_values('比例', ascending=1, inplace=True)
    excelUtil.writeExcel(df_value_rate, filePath, '总体就业行业分布')

    df_college_rate = answer_college_value_rate(data_a2, subject)
    df_college_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    df_college_rate_five = df_college_rate.groupby('学院', as_index=False).head(5)
    excelUtil.writeExcel(df_college_rate_five, filePath, '各学院就业行业分布')

    df_major_rate = answer_major_value_rate(data_a2, subject)
    df_major_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    df_major_rate_five = df_major_rate.groupby(['学院', '专业'], as_index=False).head(5)
    excelUtil.writeExcel(df_major_rate_five, filePath, '各专业就业行业分布')

    pd_single_grp_mean = single_grp_mean(data_a2, 'B6', subject)
    excelUtil.writeExcel(pd_single_grp_mean, filePath, '主要就业行业月均收入')

    single_value = answer_single_value_rate(data_a2, 'B9-1', subject)
    pd_relative = single_value[single_value['答案'].isin(CONFIG.ANSWER_NORMAL_2[0:3])]['比例'].sum()
    relativeName = '相关度'
    single_value[relativeName] = pd_relative
    excelUtil.writeExcel(single_value, filePath, '各就业行业专业相关度差异分析')

    single_value1 = answer_single_value_rate(data_a2, 'B7-A', subject)
    pd_relative1 = single_value1[single_value1['答案'].isin(CONFIG.ANSWER_NORMAL_3[0:3])]['比例'].sum()
    relativeName1 = '满意度'
    single_value1[relativeName1] = pd_relative1
    excelUtil.writeExcel(single_value1, filePath, '各就业行业就业满意度差异分析')

    return

def employee_industry_type(data, filePath):
    '''就业行业类型'''
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
    '''就业单位规模'''
    df_value_count = answer_value_rate(data, 'B2')
    excelUtil.writeExcel(df_value_count, filePath, '总体就业单位规模分布')

    college_value = answer_college_value_rate(data, 'B2')
    excelUtil.writeExcel(college_value, filePath, '各学院就业单位规模分布')

    major_value = answer_major_value_rate(data, 'B2')
    excelUtil.writeExcel(major_value, filePath, '各单位就业单位规模分布')

    return


def employee_region_report(data, filePath):
    '''就业地区'''
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


def employee_job(data, filePath):
    '''就业职业分布'''
    subject='B4-B'
    df_value_rate = answer_value_rate(data, subject)
    df_value_rate.sort_values('比例', ascending=0, inplace=True)
    excelUtil.writeExcel(df_value_rate, filePath, '总体就业职业分布')

    college_value = answer_college_value_rate(data, subject)
    college_value.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    college_five = college_value.groupby('学院', as_index=False).head(5)
    excelUtil.writeExcel(college_five, filePath, '各学院就业职业分布')

    major_value = answer_major_value_rate(data, subject)
    major_value.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    major_five = major_value.groupby(['学院', '专业'], as_index=False).head(5)
    excelUtil.writeExcel(major_five, filePath, '各单位就业职业分布')

    pd_single_grp_mean = single_grp_mean(data, 'B6', subject)
    excelUtil.writeExcel(pd_single_grp_mean, filePath, '主要就业职业月均收入')

    single_value = answer_single_value_rate(data, 'B9-1', subject)
    pd_relative = single_value[single_value['答案'].isin(CONFIG.ANSWER_NORMAL_2[0:3])]['比例'].sum()
    relativeName = '相关度'
    single_value[relativeName] = pd_relative
    excelUtil.writeExcel(single_value, filePath, '各就业职业专业相关度差异分析')

    single_value1 = answer_single_value_rate(data, 'B7-A', subject)
    pd_relative1 = single_value1[single_value1['答案'].isin(CONFIG.ANSWER_NORMAL_3[0:3])]['比例'].sum()
    relativeName1 = '满意度'
    single_value1[relativeName1] = pd_relative1
    excelUtil.writeExcel(single_value1, filePath, '各就业职业就业满意度差异分析')

    return


def study_abroad_report(data, filePath):
    a2_count = answerUtil.answer_count(data, 'A2')
    study_value = answer_value_rate(data, 'F1')
    study_value['答A2题总人数'] = a2_count
    study_value.drop(list(CONFIG.RATE_COLUMN[2:4]), axis='columns', inplace=True)
    study_value[CONFIG.RATE_COLUMN[-1]] = (
            study_value[CONFIG.RATE_COLUMN[1]] / study_value['答A2题总人数'] * 100).round(decimals=2)
    excelUtil.writeExcel(study_value, filePath, '留学比列')

    study_satisfy = answer_five_rate(data, 'F2', CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(study_satisfy, filePath, '留学录取结果满意度')

    study_relative = answer_five_rate(data, 'F3', CONFIG.ANSWER_TYPE_RELATIVE)
    excelUtil.writeExcel(study_relative, filePath, '留学专业一致性')

    change_study_reason = answer_value_rate(data, 'F4')
    excelUtil.writeExcel(change_study_reason, filePath, '跨专业升学原因')


def further_report(data, filePath):
    further_rate = answer_rate(data, 'A2', CONFIG.A2_ANSWER[3])
    excelUtil.writeExcel(further_rate, filePath, '总体国内升学比例')

    further_reason = answer_value_rate(data, 'E2')
    excelUtil.writeExcel(further_reason, filePath, '升学原因')

    further_satisfy = answer_five_rate(data, 'E1', CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(further_satisfy, filePath, '升学录取结果满意度')

    further_relative = answer_five_rate(data, 'E3', CONFIG.ANSWER_TYPE_RELATIVE)
    excelUtil.writeExcel(further_relative, filePath, '升学专业相关度')

    change_reason = answer_value_rate(data, 'E4')
    excelUtil.writeExcel(change_reason, filePath, '跨专业升学原因')


def work_stability_report(data, filePath):
    change_times = answer_value_rate(data, 'B10-1')
    no_changes = change_times[change_times[CONFIG.RATE_COLUMN[0]].isin([CONFIG.B10_1_ANSWER[0]])][
        [CONFIG.RATE_COLUMN[-1]]]
    no_changes.fillna(0, inplace=True)
    change_times['离职率'] = 100 - no_changes
    excelUtil.writeExcel(change_times, filePath, '总体离职情况分布')

    college_changes = answer_college_value_rate(data, 'B10-1')
    college_no_change = college_changes[college_changes['答案'].isin([CONFIG.B10_1_ANSWER[0]])][['学院', '比例']]
    college_no_change['离职率'] = 100 - college_no_change['比例']
    college_no_change.drop('比例', axis='columns', inplace=True)
    college_changes_left = pd.merge(college_changes, college_no_change,
                                    how='left',
                                    on='学院')
    excelUtil.writeExcel(college_changes_left, filePath, '各学院离职情况')

    major_changes = answer_major_value_rate(data, 'B10-1')
    major_no_change = major_changes[major_changes['答案'].isin([CONFIG.B10_1_ANSWER[0]])][['学院', '专业', '比例']]
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
    no_option = option[option['答案'].isin([CONFIG.EXCEPTED_ANSWER])][[CONFIG.RATE_COLUMN[1]]]
    no_option.fillna(0, inplace=True)
    option['有效人数'] = option[CONFIG.RATE_COLUMN[2]] - no_option[CONFIG.RATE_COLUMN[1]]

    option[CONFIG.RATE_COLUMN[-1]] = (option[CONFIG.RATE_COLUMN[1]] / option['有效人数'] * 100).round(
        decimals=2)
    excelUtil.writeExcel(option, filePath, '总体就业机会')

    college_changes = answer_college_value_rate(data, 'A3')
    college_no_change = college_changes[college_changes['答案'].isin([CONFIG.EXCEPTED_ANSWER])][
        ['学院', CONFIG.RATE_COLUMN[1]]]

    pd_left = pd.merge(college_changes, college_no_change,
                       how='left',
                       on='学院',
                       )
    pd_left.fillna(0, inplace=True)

    pd_left[CONFIG.RATE_COLUMN[-1]] = (pd_left[CONFIG.RATE_COLUMN[1] + '_x'] / (
            pd_left[CONFIG.RATE_COLUMN[2]] - pd_left[CONFIG.RATE_COLUMN[1] + '_y']) * 100).round(
        decimals=2)
    excelUtil.writeExcel(pd_left, filePath, '各学院就业机会')

    major_changes = answer_major_value_rate(data, 'A3')
    major_no_change = major_changes[major_changes['答案'].isin([CONFIG.EXCEPTED_ANSWER])][
        ['学院', '专业', CONFIG.RATE_COLUMN[1]]]
    pd_left_major = pd.merge(major_changes, major_no_change, how='left', on=['学院', '专业'])
    pd_left_major.fillna(0, inplace=True)
    pd_left_major[CONFIG.RATE_COLUMN[-1]] = (pd_left_major[CONFIG.RATE_COLUMN[1] + '_x'] / (
            pd_left_major[CONFIG.RATE_COLUMN[2]] - pd_left_major[
        CONFIG.RATE_COLUMN[1] + '_y']) * 100).round(decimals=2)

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
    subject = 'B6'
    pd_mean = answer_mean(data, subject)
    excelUtil.writeExcel(pd_mean, filePath, '总体月均收入')

    pd_college_mean = college_mean(data, subject)
    excelUtil.writeExcel(pd_college_mean, filePath, '各学院月均收入')

    pd_major_mean = major_mean(data, subject)
    excelUtil.writeExcel(pd_major_mean, filePath, '各专业月均收入')

    # 500
    start = 2000
    period_n = 4
    step = 500
    pd_500 = answer_period(data, subject, start, start + period_n * step, step)
    excelUtil.writeExcel(pd_500, filePath, '毕业生月均收入及薪酬分布_' + str(step))

    step = 1000
    pd_1000 = answer_period(data, subject, start, start + period_n * step, step)
    excelUtil.writeExcel(pd_1000, filePath, '毕业生月均收入及薪酬分布_' + str(step))

    step = 2000
    pd_2000 = answer_period(data, subject, start, start + period_n * step, step)
    excelUtil.writeExcel(pd_2000, filePath, '毕业生月均收入及薪酬分布_' + str(step))

    step = 1500
    pd_1500 = answer_period(data, subject, start, start + period_n * step, step)
    excelUtil.writeExcel(pd_1500, filePath, '毕业生月均收入及薪酬分布_' + str(step))
    return


def school_satisfy_report(data, filePath):
    '''母校满意度报告'''
    subject = 'H7'
    five_rate = answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(five_rate, filePath, '母校满意度')

    df_college_rate = answer_five_rate_single_grp(data, subject,
                                                  CONFIG.BASE_COLUMN[0],
                                                  CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(df_college_rate, filePath, '各学院对母校满意度')

    df_major_rate = answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(df_major_rate, filePath, '各专业对母校满意度')
    return


def school_recommed_report(data, filePath):
    '''母校推荐报告'''

    df_value_rate = answer_value_rate(data, 'H8')
    df_value_rate.sort_values('比例', ascending=0, inplace=True)
    excelUtil.writeExcel(df_value_rate, filePath, '母校推荐度')

    df_college_rate = answer_college_value_rate(data, 'H8')
    df_college_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    excelUtil.writeExcel(df_college_rate, filePath, '各学院母校推荐度')

    df_major_rate = answer_major_value_rate(data, 'H8')
    df_major_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    excelUtil.writeExcel(df_major_rate, filePath, '各专业母校推荐度')

    return


def employee_difficult_report(data, filePath):
    '''求职过程报告'''
    data_a2 = data[data['A2'].isin([CONFIG.A2_ANSWER[0], CONFIG.A2_ANSWER[2]])]

    df_value_rate = answer_value_rate(data_a2, 'D2')
    df_value_rate.sort_values('比例', ascending=0, inplace=True)
    excelUtil.writeExcel(df_value_rate, filePath, '求职困难')

    df_major_rate = answer_major_value_rate(data_a2, 'D2')
    df_major_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    df_major_rate_five = df_major_rate.groupby(['学院', '专业'], as_index=False).head(3)
    excelUtil.writeExcel(df_major_rate_five, filePath, '各专业求职困难')

    df_value_rate1 = answer_value_rate(data_a2, 'D1')
    df_value_rate1.sort_values('比例', ascending=1, inplace=True)
    excelUtil.writeExcel(df_value_rate1, filePath, '求职成功途径')

    return


def self_employed_report(data, filePath):
    '''自主创业报告'''
    business_rate = answer_rate(data, 'A2', CONFIG.A2_ANSWER[1])
    excelUtil.writeExcel(business_rate, filePath, '自主创业比例')

    subject = 'G3'
    df_distribution = answerUtil.multi_answer_distribution(data, subject)
    df_distribution.sort_values([CONFIG.RATE_COLUMN[-1]], ascending=[0], inplace=True)
    excelUtil.writeExcel(df_distribution, filePath, '创业原因')

    subject = 'G4'
    df_distribution = answerUtil.multi_answer_distribution(data, subject)
    df_distribution.sort_values([CONFIG.RATE_COLUMN[-1]], ascending=[0], inplace=True)
    excelUtil.writeExcel(df_distribution, filePath, '创业资金来源')

    subject = 'G5'
    df_distribution = answerUtil.multi_answer_distribution(data, subject)
    df_distribution.sort_values([CONFIG.RATE_COLUMN[-1]], ascending=[0], inplace=True)
    excelUtil.writeExcel(df_distribution, filePath, '创业困难')

    subject = 'G1-B'
    df_distribution = answerUtil.multi_answer_distribution(data, subject)
    df_distribution.sort_values([CONFIG.RATE_COLUMN[-1]], ascending=[0], inplace=True)
    excelUtil.writeExcel(df_distribution, filePath, '创业行业')

    subject = 'G2'
    df_mean = answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_RELATIVE)
    excelUtil.writeExcel(df_mean, filePath, '创业行业与所学专业相关度')

    return


def basic_quality_report(data, file):
    '''基础素质报告'''
    subject = 'I2-1'
    df_distribution = answerUtil.multi_answer_distribution(data, subject)
    df_distribution.sort_values([CONFIG.RATE_COLUMN[-1]], ascending=[0], inplace=True)
    excelUtil.writeExcel(df_distribution, file, '重要度')

    return


def major_quality_report(data, file):
    '''专业素质报告'''
    subject = 'I1-1'
    df_mean_1 = answer_five_rate(data, subject + '-A', CONFIG.ANSWER_TYPE_IMPORTANT)
    df_mean_1['题目'] = 'I1-1-A'
    df_mean_2 = answer_five_rate(data, subject + '-B', CONFIG.ANSWER_TYPE_IMPORTANT)
    df_mean_2['题目'] = 'I1-1-B'
    pd_concat = pd.concat([df_mean_1, df_mean_2])
    excelUtil.writeExcel(pd_concat, file, '专业素质重要性')

    subject = 'I1-2'
    df_mean_1 = answer_five_rate(data, subject + '-A', CONFIG.ANSWER_TYPE_PLEASED)
    df_mean_1['题目'] = 'I1-2-A'
    df_mean_2 = answer_five_rate(data, subject + '-B', CONFIG.ANSWER_TYPE_PLEASED)
    df_mean_2['题目'] = 'I1-2-B'
    pd_concat = pd.concat([df_mean_1, df_mean_2])
    excelUtil.writeExcel(pd_concat, file, '专业素质满意度')

    return


def evelution_lesson_report(data, file):
    '''课堂教学报告'''
    subject = 'H2'
    sub_column = answerUtil.multi_columns(data, subject)
    ls_column=list(CONFIG.MEAN_COLUMN)
    ls_column=ls_column.append('题目')
    df_init = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe

    for col in sub_column:
        df_mean = answer_five_rate(data, col, CONFIG.ANSWER_TYPE_MEET_V)
        df_mean['题目'] = col
        excelUtil.writeExcel(df_mean, file, '课堂教学各方面评价_'+str(col))

        df_grp=answer_five_rate_single_grp(data,col,'_10',CONFIG.ANSWER_TYPE_MEET_V)
        df_mean['题目'] = col
        excelUtil.writeExcel(df_grp, file, '学院课堂教学各方面评价_' + str(col))

        df_major = answer_five_rate_major_grp(data, col,  CONFIG.ANSWER_TYPE_MEET_V)
        df_major['题目'] = col
        excelUtil.writeExcel(df_major, file, '专业课堂教学各方面评价_' + str(col))

    return

def evelution_practice_report(data, file):
    '''实践教学报告'''
    subject = 'H3'
    sub_column = answerUtil.multi_columns(data, subject)

    for col in sub_column:
        df_mean = answer_five_rate(data, col, CONFIG.ANSWER_TYPE_HELP)
        df_mean['题目'] = col
        excelUtil.writeExcel(df_mean, file, '实践教学各方面评价_'+str(col))

        df_grp=answer_five_rate_single_grp(data,col,'_10',CONFIG.ANSWER_TYPE_HELP)
        df_mean['题目'] = col
        excelUtil.writeExcel(df_grp, file, '学院实践教学各方面评价_' + str(col))

        df_major = answer_five_rate_major_grp(data, col, CONFIG.ANSWER_TYPE_HELP)
        df_major['题目'] = col
        excelUtil.writeExcel(df_major, file, '专业实践教学各方面评价_' + str(col))

    return

def evelution_teacher_report(data, file):
    '''教师管理报告'''
    subject = 'H4'
    sub_column = answerUtil.multi_columns(data, subject)

    for col in sub_column:
        df_mean = answer_five_rate(data, col, CONFIG.ANSWER_TYPE_SATISFY)
        df_mean['题目'] = col
        excelUtil.writeExcel(df_mean, file, '教师各方面评价_'+str(col))

        df_grp=answer_five_rate_single_grp(data,col,'_10',CONFIG.ANSWER_TYPE_SATISFY)
        df_mean['题目'] = col
        excelUtil.writeExcel(df_grp, file, '学院教师学各方面评价_' + str(col))

        df_major = answer_five_rate_major_grp(data, col, CONFIG.ANSWER_TYPE_HELP)
        df_major['题目'] = col
        excelUtil.writeExcel(df_major, file, '专业教师各方面评价_' + str(col))

    return

def major_relative_report(data,filePath):
    '''专业相关度'''
    subject='B9-1'
    pd_summary=answer_five_rate(data,subject,CONFIG.ANSWER_TYPE_RELATIVE)
    excelUtil.writeExcel(pd_summary, filePath, '总体专业相关情况')

    pd_college=answer_five_rate_single_grp(data,subject,
                                           CONFIG.BASE_COLUMN[0],
                                           CONFIG.ANSWER_TYPE_RELATIVE)
    excelUtil.writeExcel(pd_college, filePath, '学院专业相关情况')

    pd_major=answer_five_rate_major_grp(data,subject,CONFIG.ANSWER_TYPE_RELATIVE)
    excelUtil.writeExcel(pd_major, filePath, '各专业专业相关情况')

def job_meet_report(data,filePath):
    '''职业期待吻合度'''
    subject = 'B8'
    pd_summary = answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_MEET)
    excelUtil.writeExcel(pd_summary, filePath, '总体职业期待吻合度')

    pd_college = answer_five_rate_single_grp(data, subject,
                                             CONFIG.BASE_COLUMN[0],
                                             CONFIG.ANSWER_TYPE_MEET)
    excelUtil.writeExcel(pd_college, filePath, '学院职业期待吻合度')

    pd_major = answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_MEET)
    excelUtil.writeExcel(pd_major, filePath, '各专业职业期待吻合度')

def job_satisfy_report(data,filePath):
    '''职业满意度'''

    subject = 'B7-A'
    pd_summary = answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(pd_summary, filePath, '工作总体满意情况')

    pd_college = answer_five_rate_single_grp(data, subject,
                                             CONFIG.BASE_COLUMN[0],
                                             CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(pd_college, filePath, '学院工作总体满意情况')

    pd_major = answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(pd_major, filePath, '各专业工作总体满意情况')

    subject = 'B7-B'
    pd_summary = answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(pd_summary, filePath, '工作薪酬满意情况')

    pd_college = answer_five_rate_single_grp(data, subject,
                                             CONFIG.BASE_COLUMN[0],
                                             CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(pd_college, filePath, '学院工作薪酬满意情况')

    pd_major = answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(pd_major, filePath, '各专业工作薪酬满意情况')

    subject = 'B7-C'
    pd_summary = answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(pd_summary, filePath, '职业发展前景满意情况')

    pd_college = answer_five_rate_single_grp(data, subject,
                                             CONFIG.BASE_COLUMN[0],
                                             CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(pd_college, filePath, '学院工作职业发展前景满意情况')

    pd_major = answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(pd_major, filePath, '各专业工作职业发展前景满意情况')

    subject = 'B7-D'
    pd_summary = answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(pd_summary, filePath, '工作内容意情况')

    pd_college = answer_five_rate_single_grp(data, subject,
                                             CONFIG.BASE_COLUMN[0],
                                             CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(pd_college, filePath, '学院工作内容满意情况')

    pd_major = answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(pd_major, filePath, '各专业工作内容满意情况')


def special_employee_featured(data, dict_where):
    '''特殊人群就业特色分析'''
    # 行业
    demension = 'B5-B'
    df_male_indurstry = formulas.answer_rate_condition(data, demension, dict_where, ['比例'], [0], 5)

    # 单位类型
    demension = 'B1'
    df_male_indurstry_type = formulas.answer_rate_condition(data, demension, dict_where, ['比例'], [0], 5)

    # 就业省
    demension = 'B3-A'
    df_male_region = formulas.answer_rate_condition(data, demension, dict_where, ['比例'], [0], 5)

    # 就业职业
    demension = 'B4-B'
    df_male_job = formulas.answer_rate_condition(data, demension, dict_where, ['比例'], [0], 5)

    df_concat = pd.concat([df_male_indurstry, df_male_indurstry_type,
                           df_male_region, df_male_job],axis=1)
    return df_concat

def special_employee_competitive(data, dict_where):
    '''特殊人群就业竞争力分析'''
    # 就业率
    df_income = formulas.formulas_employe_rate(data, dict_where)

    # 薪酬
    df_salary = formulas.formula_income_mean(data, dict_where)

    col_cond = str(dict_where[CONFIG.DICT_KEY[0]])
    df_data = data[data[col_cond] == dict_where[CONFIG.DICT_KEY[1]]]
    # 专业相关度
    subject = 'B9-1'
    df_major_relative = answer_five_rate(df_data, subject, CONFIG.ANSWER_TYPE_RELATIVE)

    # 工作满意度
    subject = 'B7-A'
    df_job_satisfy = answer_five_rate(df_data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    # 薪酬满意度
    subject = 'B7-B'
    df_salary_satisfy = answer_five_rate(df_data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    # 职业发展前景满意度
    subject = 'B7-C'
    df_industry_satisfy = answer_five_rate(df_data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    # 工作内容满意度
    subject = 'B7-D'
    df_job_content_satisfy = answer_five_rate(df_data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    # 职业期待吻合度
    subject = 'B8'
    df_job_hope = answer_five_rate(df_data, subject, CONFIG.ANSWER_TYPE_MEET)

    # 离职率
    subject = 'B10-1'
    change_times = answer_value_rate(data,subject)
    no_changes = change_times[change_times[CONFIG.RATE_COLUMN[0]].isin([CONFIG.B10_1_ANSWER[0]])][
        [CONFIG.RATE_COLUMN[-1]]]
    no_changes.fillna(0, inplace=True)
    change_times['离职率'] = 100 - no_changes

    df_concat = pd.concat([df_income, df_salary, df_major_relative, df_job_satisfy,
                           df_salary_satisfy, df_industry_satisfy,
                           df_job_content_satisfy,df_job_hope,change_times],axis=1)
    print(df_concat)
    return  df_concat

def special_lesson(data, dict_where):
    '''特殊人课堂教学分析'''
    subject = 'H2'

    col_cond = str(dict_where[CONFIG.DICT_KEY[0]])
    df_data = data[data[col_cond] == dict_where[CONFIG.DICT_KEY[1]]]

    sub_column = answerUtil.multi_columns(df_data, subject)
    ls_column = list(CONFIG.MEAN_COLUMN)
    ls_column = ls_column.append('题目')
    df_init = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    for col in sub_column:
        df_mean = answer_five_rate(data, col, CONFIG.ANSWER_TYPE_MEET_V)
        df_mean['题目'] = col
        df_init=pd.concat([df_init,df_mean])
    print(df_init)
    return df_init

def special_practice(data, dict_where):
    '''特殊人群实践教学报告'''
    subject = 'H3'
    col_cond = str(dict_where[CONFIG.DICT_KEY[0]])
    df_data = data[data[col_cond] == dict_where[CONFIG.DICT_KEY[1]]]

    sub_column = answerUtil.multi_columns(df_data, subject)
    ls_column = list(CONFIG.MEAN_COLUMN)
    ls_column = ls_column.append('题目')
    df_init = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    for col in sub_column:
        df_mean = answer_five_rate(data, col, CONFIG.ANSWER_TYPE_HELP)
        df_mean['题目'] = col
        df_init = pd.concat([df_init, df_mean])
    return df_init

def special_teacher(data, dict_where):
    '''特殊人群教师评价'''
    subject = 'H4'
    col_cond = str(dict_where[CONFIG.DICT_KEY[0]])
    df_data = data[data[col_cond] == dict_where[CONFIG.DICT_KEY[1]]]

    sub_column = answerUtil.multi_columns(df_data, subject)
    ls_column = list(CONFIG.MEAN_COLUMN)
    ls_column = ls_column.append('题目')
    df_init = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    for col in sub_column:
        df_mean = answer_five_rate(data, col, CONFIG.ANSWER_TYPE_SATISFY)
        df_mean['题目'] = col
        df_init = pd.concat([df_init, df_mean])
    return df_init

def special_school(data, dict_where):
    '''特殊人群学校总体评价'''

    col_cond = str(dict_where[CONFIG.DICT_KEY[0]])
    df_data = data[data[col_cond] == dict_where[CONFIG.DICT_KEY[1]]]

    # 学校满意度
    subject = 'H7'
    df_mean_satisfy = answer_five_rate(df_data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    # 学校推荐度
    df_recommend = answer_value_rate(df_data, 'H8')

    df_result=pd.concat([df_mean_satisfy,df_recommend],axis=1)
    return df_result


def special_gender_report(data,filePath):
    subject='_3'
    suffix='不同性别'

    dict_where1={CONFIG.DICT_KEY[0]:subject,CONFIG.DICT_KEY[1]:CONFIG.GENDER[0]}
    dict_where2={CONFIG.DICT_KEY[0]:subject,CONFIG.DICT_KEY[1]:CONFIG.GENDER[1]}

    df_emp_feature1=special_employee_featured(data,dict_where1)
    df_emp_feature2=special_employee_featured(data,dict_where2)
    df_concat=pd.concat([df_emp_feature1,df_emp_feature2])
    excelUtil.writeExcel(df_concat, filePath, suffix+'就业特色')

    df_emp_competitive1=special_employee_competitive(data, dict_where1)
    df_emp_competitive2=special_employee_competitive(data,dict_where2)
    df_concat=pd.concat([df_emp_competitive1,df_emp_competitive2])
    excelUtil.writeExcel(df_concat, filePath, suffix+ '就业就业竞争力')

    df_lesson1=special_lesson(data, dict_where1)
    df_lesson2=special_lesson(data, dict_where1)
    df_concat=pd.concat([df_lesson1,df_lesson2])
    excelUtil.writeExcel(df_concat, filePath, suffix+ '就业就业课堂教学')

    df_practice1=special_practice(data, dict_where1)
    df_practice2=special_practice(data, dict_where1)
    df_concat=pd.concat([df_practice1,df_practice2])
    excelUtil.writeExcel(df_concat, filePath, suffix+ '实践教学')

    df_teacher1 = special_teacher(data, dict_where1)
    df_teacher2 = special_teacher(data, dict_where1)
    df_concat = pd.concat([df_teacher1, df_teacher2])
    excelUtil.writeExcel(df_concat, filePath, suffix + '教师评价')

    df_school1 = special_school(data, dict_where1)
    df_school2 = special_school(data, dict_where1)
    df_concat = pd.concat([df_school1, df_school2])
    excelUtil.writeExcel(df_concat, filePath, suffix + '母校总和评价')

    return


##################公式部分

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

# 被formulas answer_rate替代
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
    pd_count = answerUtil.answer_grp_count(data, [CONFIG.BASE_COLUMN[0], subject], [CONFIG.BASE_COLUMN[0]])
    pd_value_count = answerUtil.answer_grp_count(data, [CONFIG.BASE_COLUMN[0], subject],
                                                 [CONFIG.BASE_COLUMN[0], subject])

    pd_left = pd.merge(pd_value_count, pd_count, on=CONFIG.BASE_COLUMN[0], how='left', suffixes=('_x', '_y'))
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
                                           [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1], subject],
                                           [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]])
    pd_value_count = answerUtil.answer_grp_count(data,
                                                 [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1], subject],
                                                 [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1], subject])
    pd_left = pd.merge(pd_value_count, pd_count,
                       on=[CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]],
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
    pd_source = pd.DataFrame(data, columns=[CONFIG.BASE_COLUMN[0], subject])
    grouped = pd_source.groupby(CONFIG.BASE_COLUMN[0], as_index=False)
    pd_result = grouped[subject].agg([np.sum, np.mean, np.count_nonzero])
    formate = lambda x: "%.2f" % x
    pd_result = pd_result.applymap(formate)
    return pd_result


def major_mean(data, subject):
    pd_source = pd.DataFrame(data, columns=[CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1], subject])
    grouped = pd_source.groupby([CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]], as_index=False)
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


def answer_five_rate(data, subject, measure_type):
    '''某题五维占比'''
    # step1：各个答案占比(无法评价已被清理)
    pd_five_rate = answer_value_rate(data, subject)

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
    print(pd_five_rate)
    pd_five_rate['measure_score'] = pd_five_rate['回答此答案人数'] * pd_five_rate['measure_score']
    alpha_x = pd_five_rate['measure_score'].sum()

    pd_five_rate['均值'] = (alpha_x / pd_five_rate['答题总人数']).round(decimals=2)

    # pd_five_rate['均值'] = pd_five_rate['均值'].map(lambda x: '%.2f' % x)
    pd_five_rate.drop('measure_score', axis='columns', inplace=True)

    return pd_five_rate


def answer_five_rate_single_grp(data, subject, grp, measure_type):
    '''某题单维分组的五维占比'''

    # 分组算总数
    pd_total = answerUtil.answer_grp_count(data, [grp, subject], [grp])
    pd_total.columns=['分组', '答题总人数']
    #pd_total.rename(columns=CONFIG.COLUMN_NAME_GRP_COUNT, inplace=True)
    print(pd_total)
    # 分组算各答案分布
    pd_distribution = answerUtil.answer_grp_count(data, [grp, subject], [grp, subject])
    pd_distribution.columns=['分组', '答案', '回答此答案人数']

    #pd_distribution.rename(columns=CONFIG.COLUMN_NAME_GRP_VAL_COUNT, inplace=True)
    print(pd_distribution)
    # 合并答案、回答此答案人数、答题总人数
    pd_left_rate = pd.merge(pd_distribution, pd_total, how='left', on='分组', validate='many_to_one')
    print(pd_left_rate)
    pd_left_rate['比例'] = (pd_left_rate['回答此答案人数'] / pd_left_rate['答题总人数'] * 100).round(2)

    # step3: 相关度/满意度/符合度
    ls_measure = parse_measure(measure_type)
    dict_measure_score = parse_measure_score(measure_type)
    measure_name = parse_measure_name(measure_type)

    pd_measure = pd_left_rate[pd_left_rate['答案'].isin(ls_measure[0:3])]
    pd_measure_sum = answerUtil.answer_grp_sum(pd_measure, ['分组', '比例'], ['分组'])
    print("各学院各专业{}吻合度：\n".format(subject))
    print(pd_measure_sum)

    pd_left_rate_measure = pd.merge(pd_left_rate, pd_measure_sum, on='分组', how='left', suffixes=['', '_y'])
    pd_left_rate_measure.rename(columns={'比例_y': measure_name}, inplace=True)

    # step6:计算alpha
    pd_left_rate_measure['measure_score'] = pd_left_rate_measure['答案']
    pd_left_rate_measure.replace({'measure_score': dict_measure_score}, inplace=True)

    pd_left_rate_measure['measure_score'] = pd_left_rate_measure['回答此答案人数'] * pd_left_rate_measure['measure_score']
    pd_measure_sum = answerUtil.answer_grp_sum(pd_left_rate_measure, ['分组', 'measure_score'], ['分组'])

    # step5:计算mean
    pd_left_mean = pd.merge(pd_left_rate_measure, pd_measure_sum, how='left', on='分组', suffixes=['', '_y'])
    pd_left_mean['mean'] = (pd_left_mean['measure_score_y'] / pd_left_mean['答题总人数']).round(2)
    pd_left_mean.rename(columns={'mean': '均值'}, inplace=True)
    pd_left_mean.drop('measure_score', axis='columns', inplace=True)
    pd_left_mean.drop('measure_score_y', axis='columns', inplace=True)

    return pd_left_mean

def answer_five_rate_major_grp(data, subject, measure_type):
    '''某题按专业分组的五维占比'''

    grp_column=list(CONFIG.COLLEGE_MAJOR)
    relative_column = list(CONFIG.COLLEGE_MAJOR)
    relative_column.append(subject)
    print(relative_column)
    # 分组算总数

    pd_total = answerUtil.answer_grp_count(data, relative_column,grp_column)
    pd_total.columns=['学院','专业', '答题总人数']
    # 分组算各答案分布
    pd_distribution = answerUtil.answer_grp_count(data,relative_column, relative_column)
    pd_distribution.columns=['学院','专业', '答案', '回答此答案人数']

    # 合并答案、回答此答案人数、答题总人数
    pd_left_rate = pd.merge(pd_distribution, pd_total, how='left', on=['学院','专业'], validate='many_to_one')
    pd_left_rate['比例'] = (pd_left_rate['回答此答案人数'] / pd_left_rate['答题总人数'] * 100).round(2)

    # step3: 相关度/满意度/符合度
    ls_measure = parse_measure(measure_type)
    dict_measure_score = parse_measure_score(measure_type)
    measure_name = parse_measure_name(measure_type)

    pd_measure = pd_left_rate[pd_left_rate['答案'].isin(ls_measure[0:3])]
    pd_measure_sum = answerUtil.answer_grp_sum(pd_measure, ['学院','专业', '比例'], ['学院','专业'])

    pd_left_rate_measure = pd.merge(pd_left_rate, pd_measure_sum, on=['学院','专业'], how='left', suffixes=['', '_y'])
    pd_left_rate_measure.rename(columns={'比例_y': measure_name}, inplace=True)


    # step6:计算alpha
    pd_left_rate_measure['measure_score'] = pd_left_rate_measure['答案']
    pd_left_rate_measure.replace({'measure_score': dict_measure_score}, inplace=True)

    pd_left_rate_measure['measure_score'] = pd_left_rate_measure['回答此答案人数'] * pd_left_rate_measure['measure_score']
    pd_measure_sum = answerUtil.answer_grp_sum(pd_left_rate_measure, ['学院','专业', 'measure_score'], ['学院','专业'])

    # step5:计算mean
    pd_left_mean = pd.merge(pd_left_rate_measure, pd_measure_sum, how='left', on=['学院','专业'], suffixes=['', '_y'])
    pd_left_mean['mean'] = (pd_left_mean['measure_score_y'] / pd_left_mean['答题总人数']).round(2)
    pd_left_mean.rename(columns={'mean': '均值'}, inplace=True)
    pd_left_mean.drop('measure_score', axis='columns', inplace=True)
    pd_left_mean.drop('measure_score_y', axis='columns', inplace=True)

    return pd_left_mean
