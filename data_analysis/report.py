#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'report.py'

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

    subject = 'B5-B'
    df_value_rate = formulas.answer_value_rate(data_a2, subject)
    df_value_rate.sort_values('比例', ascending=0, inplace=True)
    excelUtil.writeExcel(df_value_rate, filePath, '总体就业行业分布')

    df_college_rate = formulas.answer_college_value_rate(data_a2, subject)
    df_college_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    df_college_rate_five = df_college_rate.groupby('学院', as_index=False).head(5)
    df_combine = formulas.college_row_combine(df_college_rate_five, combin_name='行业')
    excelUtil.writeExcel(df_combine, filePath, '各学院就业行业分布')

    df_major_rate = formulas.answer_major_value_rate(data_a2, subject)
    df_major_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    df_major_rate_five = df_major_rate.groupby(['学院', '专业'], as_index=False).head(5)
    df_combine = formulas.major_row_combine(df_major_rate_five, combin_name='行业')
    excelUtil.writeExcel(df_combine, filePath, '各专业就业行业分布')

    pd_single_grp_mean = formulas.single_grp_mean(data_a2, 'B6', subject)
    excelUtil.writeExcel(pd_single_grp_mean, filePath, '主要就业行业月均收入')

    single_value = formulas.answer_five_rate_single_grp(data_a2, 'B9-1', subject, CONFIG.ANSWER_TYPE_RELATIVE)
    relativeName = formulas.parse_measure_name(CONFIG.ANSWER_TYPE_RELATIVE)
    df_t = formulas.college_rate_pivot(single_value, [relativeName, CONFIG.MEAN_COLUMN[2]], hasCollege=False)
    excelUtil.writeExcel(df_t, filePath, '各就业行业专业相关度差异分析')

    single_value = formulas.answer_five_rate_single_grp(data_a2, 'B7-A', subject, CONFIG.ANSWER_TYPE_SATISFY)
    relativeName = formulas.parse_measure_name(CONFIG.ANSWER_TYPE_SATISFY)
    df_t = formulas.college_rate_pivot(single_value, [relativeName, CONFIG.MEAN_COLUMN[2]], hasCollege=False)
    excelUtil.writeExcel(df_t, filePath, '各就业行业就业满意度差异分析')

    return


def employee_job(data, filePath):
    '''就业职业分布'''

    data_a2 = data[data['A2'] == CONFIG.A2_ANSWER[0]]
    subject = 'B4-B'
    df_value_rate = formulas.answer_value_rate(data_a2, subject)
    df_value_rate.sort_values('比例', ascending=0, inplace=True)
    excelUtil.writeExcel(df_value_rate, filePath, '总体就业职业分布')

    college_value = formulas.answer_college_value_rate(data_a2, subject)
    college_value.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    college_five = college_value.groupby('学院', as_index=False).head(5)
    df_combine = formulas.college_row_combine(college_five, combin_name='职业')
    excelUtil.writeExcel(df_combine, filePath, '各学院就业职业分布')

    major_value = formulas.answer_major_value_rate(data_a2, subject)
    major_value.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    major_five = major_value.groupby(['学院', '专业'], as_index=False).head(5)
    df_combine = formulas.major_row_combine(major_five, combin_name='职业')
    excelUtil.writeExcel(df_combine, filePath, '各单位就业职业分布')

    pd_single_grp_mean = formulas.single_grp_mean(data_a2, 'B6', subject)
    excelUtil.writeExcel(pd_single_grp_mean, filePath, '主要就业职业月均收入')

    single_value = formulas.answer_five_rate_single_grp(data_a2, 'B9-1', subject,CONFIG.ANSWER_TYPE_RELATIVE)
    relativeName = formulas.parse_measure_name(CONFIG.ANSWER_TYPE_RELATIVE)
    df_t = formulas.college_rate_pivot(single_value, [relativeName, CONFIG.MEAN_COLUMN[2]], hasCollege=False)
    excelUtil.writeExcel(df_t, filePath, '各就业职业专业相关度差异分析')

    single_value = formulas.answer_five_rate_single_grp(data_a2, 'B7-A', subject,CONFIG.ANSWER_TYPE_SATISFY)
    relativeName = formulas.parse_measure_name(CONFIG.ANSWER_TYPE_SATISFY)
    df_t = formulas.college_rate_pivot(single_value, [relativeName, CONFIG.MEAN_COLUMN[2]], hasCollege=False)
    excelUtil.writeExcel(df_t, filePath, '各就业职业就业满意度差异分析')

    return


def employee_region_report(data, filePath):
    '''就业地区分布'''
    df_value_count = formulas.answer_value_rate(data, 'B3-A')
    excelUtil.writeExcel(df_value_count, filePath, '总体就业省')

    province = '福建省'
    pd_province = data[data['B3-A'] == province]
    college_value = formulas.answer_value_rate(pd_province, 'B3-B')
    excelUtil.writeExcel(college_value, filePath, '省内就业城市')

    college_value = formulas.answer_college_value_rate(data, 'B3-A')
    college_value.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    college_five = college_value.groupby('学院', as_index=False).head(5)
    df_combine = formulas.college_row_combine(college_five, combin_name='就业地区')
    excelUtil.writeExcel(df_combine, filePath, '各学院就业地区分布')

    pd_province_city = formulas.answer_college_value_rate(pd_province, 'B3-B')
    pd_province_city.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    province_college_five = pd_province_city.groupby('学院', as_index=False).head(5)
    df_combine = formulas.college_row_combine(province_college_five, combin_name='就业城市')
    excelUtil.writeExcel(df_combine, filePath, '各学院省内就业地区分布')

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

    pd_single_grp_mean = formulas.single_grp_mean(data, 'B6', 'B3-A')
    excelUtil.writeExcel(pd_single_grp_mean, filePath, '主要就业地区月均收入')

    pd_single_grp_city_mean = formulas.single_grp_mean(pd_province, 'B6', 'B3-B')
    excelUtil.writeExcel(pd_single_grp_city_mean, filePath, '省内主要就业城市月均收入')

    return


def employee_industry_type(data, filePath):
    '''就业行业类型'''
    df_value_count = formulas.answer_value_rate(data, 'B1')
    excelUtil.writeExcel(df_value_count, filePath, '总体就业单位类型分布')

    college_value = formulas.answer_college_value_rate(data, 'B1')
    college_value.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    college_five = college_value.groupby('学院', as_index=False).head(5)
    df_combine = formulas.college_row_combine(college_five, combin_name='单位类型')
    excelUtil.writeExcel(df_combine, filePath, '各学院就业单位类型分布')

    major_value = formulas.answer_major_value_rate(data, 'B1')
    major_value.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    major_five = major_value.groupby(['学院', '专业'], as_index=False).head(5)
    df_combine = formulas.major_row_combine(major_five, combin_name='单位类型')
    excelUtil.writeExcel(df_combine, filePath, '各单位就业单位类型分布')

    return


def employee_industry_size(data, filePath):
    '''就业单位规模'''
    df_value_count = formulas.answer_value_rate(data, 'B2')
    df_t=formulas.rate_T(df_value_count)
    excelUtil.writeExcel(df_t, filePath, '总体就业单位规模分布')

    college_value = formulas.answer_college_value_rate(data, 'B2')
    df_t=formulas.college_rate_pivot(college_value)
    excelUtil.writeExcel(df_t, filePath, '各学院就业单位规模分布')

    major_value = formulas.answer_major_value_rate(data, 'B2')
    df_t=formulas.major_rate_pivot(major_value)
    excelUtil.writeExcel(df_t, filePath, '各单位就业单位规模分布')

    return

def employee_industry_mertrics(data, filePath):
    '''主要就业单位 收入、工作满意度、专业相关度报告'''
    data_a2 = data[data['A2'] == CONFIG.A2_ANSWER[0]]
    subject = 'B1'
    pd_single_grp_mean = formulas.single_grp_mean(data_a2, 'B6', subject)
    excelUtil.writeExcel(pd_single_grp_mean, filePath, '主要就业单位月均收入差异')

    single_value = formulas.answer_five_rate_single_grp(data_a2, 'B9-1', subject,CONFIG.ANSWER_TYPE_RELATIVE)
    relativeName = formulas.parse_measure_name(CONFIG.ANSWER_TYPE_RELATIVE)
    df_t = formulas.college_rate_pivot(single_value, [relativeName, CONFIG.MEAN_COLUMN[2]], hasCollege=False)
    excelUtil.writeExcel(df_t, filePath, '各就业单位专业相关度差异分析')

    single_value = formulas.answer_five_rate_single_grp(data_a2, 'B7-A', subject,CONFIG.ANSWER_TYPE_SATISFY)
    relativeName = formulas.parse_measure_name(CONFIG.ANSWER_TYPE_SATISFY)
    df_t = formulas.college_rate_pivot(single_value, [relativeName, CONFIG.MEAN_COLUMN[2]], hasCollege=False)
    excelUtil.writeExcel(df_t, filePath, '各就业职业单位满意度差异分析')



def study_abroad_report(data, filePath):
    a2_count = answerUtil.answer_count(data, 'A2')
    study_value = formulas.answer_value_rate(data, 'F1')
    study_value['答A2题总人数'] = a2_count
    study_value.drop(list(CONFIG.RATE_COLUMN[2:4]), axis='columns', inplace=True)
    study_value[CONFIG.RATE_COLUMN[-1]] = (
            study_value[CONFIG.RATE_COLUMN[1]] / study_value['答A2题总人数'] * 100).round(decimals=2)
    excelUtil.writeExcel(study_value, filePath, '留学比列')

    study_satisfy = formulas.answer_five_rate(data, 'F2', CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(study_satisfy, filePath, '留学录取结果满意度')

    study_relative = formulas.answer_five_rate(data, 'F3', CONFIG.ANSWER_TYPE_RELATIVE)
    excelUtil.writeExcel(study_relative, filePath, '留学专业一致性')

    change_study_reason = formulas.answer_value_rate(data, 'F4')
    excelUtil.writeExcel(change_study_reason, filePath, '跨专业升学原因')


def further_report(data, filePath):
    further_rate = formulas.answer_rate(data, 'A2', CONFIG.A2_ANSWER[3])
    excelUtil.writeExcel(further_rate, filePath, '总体国内升学比例')

    further_reason = formulas.answer_value_rate(data, 'E2')
    excelUtil.writeExcel(further_reason, filePath, '升学原因')

    further_satisfy = formulas.answer_five_rate(data, 'E1', CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(further_satisfy, filePath, '升学录取结果满意度')

    further_relative = formulas.answer_five_rate(data, 'E3', CONFIG.ANSWER_TYPE_RELATIVE)
    excelUtil.writeExcel(further_relative, filePath, '升学专业相关度')

    change_reason = formulas.answer_value_rate(data, 'E4')
    excelUtil.writeExcel(change_reason, filePath, '跨专业升学原因')


def work_stability_report(data, filePath):
    change_times = formulas.answer_value_rate(data, 'B10-1')
    no_changes = change_times[change_times[CONFIG.RATE_COLUMN[0]].isin([CONFIG.B10_1_ANSWER[0]])][
        [CONFIG.RATE_COLUMN[-1]]]
    no_changes.fillna(0, inplace=True)
    change_times['离职率'] = 100 - no_changes
    excelUtil.writeExcel(change_times, filePath, '总体离职情况分布')

    college_changes = formulas.answer_college_value_rate(data, 'B10-1')
    college_no_change = college_changes[college_changes['答案'].isin([CONFIG.B10_1_ANSWER[0]])][['学院', '比例']]
    college_no_change['离职率'] = 100 - college_no_change['比例']
    college_no_change.drop('比例', axis='columns', inplace=True)
    college_changes_left = pd.merge(college_changes, college_no_change,
                                    how='left',
                                    on='学院')
    excelUtil.writeExcel(college_changes_left, filePath, '各学院离职情况')

    major_changes = formulas.answer_major_value_rate(data, 'B10-1')
    major_no_change = major_changes[major_changes['答案'].isin([CONFIG.B10_1_ANSWER[0]])][['学院', '专业', '比例']]
    major_no_change['离职率'] = 100 - major_no_change['比例']
    major_no_change.drop('比例', axis='columns', inplace=True)
    major_changes_left = pd.merge(major_changes, major_no_change,
                                  how='left',
                                  on=['学院', '专业'])
    excelUtil.writeExcel(major_changes_left, filePath, '各专业离职情况')

    change_reason = formulas.answer_value_rate(data, 'B10-2')
    excelUtil.writeExcel(change_reason, filePath, '更换工作原因')


def employee_report(data, filePath):
    '''
    就业力报告
    :param data:
    :param filePath:
    :return:
    '''
    subject = 'A2'
    ls_metrics_cols = list(CONFIG.BASE_COLUMN)
    df_metrics = data[ls_metrics_cols]
    # 总体就业率
    df_rate = formulas.formulas_employe_rate(df_metrics)
    excelUtil.writeExcel(df_rate, filePath, '总体就业率')
    # 各学院就业率
    df_college_value = formulas.formulas_college_employe_rate(df_metrics)
    excelUtil.writeExcel(df_college_value, filePath, '各学院就业率')
    # 各专业就业率
    df_major_value = formulas.formulas_major_employe_rate(df_metrics)
    excelUtil.writeExcel(df_major_value, filePath, '各专业就业率')

    # 总体就业去向
    df_value_rate = formulas.answer_value_rate(df_metrics, subject)
    # 灵活就业率
    flexible = df_value_rate[df_value_rate[CONFIG.RATE_COLUMN[0]] \
        .isin(CONFIG.A2_ANSWER[1:3])][CONFIG.RATE_COLUMN[-1]].sum()
    df_t = formulas.rate_T(df_value_rate)
    df_t[CONFIG.EMP_FREE_RATE_COLUMN] = flexible
    excelUtil.writeExcel(df_t, filePath, '总体毕业去向')

    # 各学院就业去向
    college_changes = formulas.answer_college_value_rate(df_metrics, subject)
    college_t = formulas.college_rate_pivot(college_changes)
    college_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    # 灵活就业
    df_flexiable = college_changes[college_changes[CONFIG.RATE_COLUMN[0]].isin(CONFIG.A2_ANSWER[1:3])][
        [CONFIG.GROUP_COLUMN[0], CONFIG.RATE_COLUMN[-1]]]
    df_flexiable = answerUtil.answer_grp_sum(df_flexiable, [CONFIG.GROUP_COLUMN[0], CONFIG.RATE_COLUMN[-1]],
                                             [CONFIG.GROUP_COLUMN[0]])
    df_flexiable.rename(columns={CONFIG.RATE_COLUMN[-1]: CONFIG.EMP_FREE_RATE_COLUMN}, inplace=True)
    df_result = pd.merge(college_t, df_flexiable, on=CONFIG.GROUP_COLUMN[0], how='left')
    excelUtil.writeExcel(df_result, filePath, '各学院毕业去向')

    # 各专业就业去向
    major_changes = formulas.answer_major_value_rate(df_metrics, subject)
    major_t = formulas.major_rate_pivot(major_changes)
    major_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)

    # 灵活就业
    df_flexiable = major_changes[major_changes[CONFIG.RATE_COLUMN[0]].isin(CONFIG.A2_ANSWER[1:3])][
        [CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1], CONFIG.RATE_COLUMN[-1]]]
    df_flexiable = answerUtil.answer_grp_sum(df_flexiable,
                                             [CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1], CONFIG.RATE_COLUMN[-1]],
                                             [CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1]])
    df_flexiable.rename(columns={CONFIG.RATE_COLUMN[-1]: CONFIG.EMP_FREE_RATE_COLUMN}, inplace=True)
    df_result = pd.merge(major_t, df_flexiable, on=[CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1]], how='left')

    excelUtil.writeExcel(df_result, filePath, '各专业毕业去向')
    return


def work_option_report(data, filePath):
    '''
    就业率及就业状态
    :param data:
    :param filePath:
    :return:
    '''
    subject = 'A3'
    ls_metrics_cols = list(CONFIG.BASE_COLUMN)
    ls_metrics_cols.append(subject)
    df_metrics = data[ls_metrics_cols]

    option = formulas.answer_value_rate(df_metrics, subject, [CONFIG.EXCEPTED_ANSWER])

    rate_t = formulas.rate_T(option)
    excelUtil.writeExcel(rate_t, filePath, '总体就业机会')

    college_changes = formulas.answer_college_value_rate(df_metrics, subject,
                                                [CONFIG.EXCEPTED_ANSWER], [CONFIG.RATE_COLUMN[2]], [0])
    college_t = formulas.college_rate_pivot(college_changes)
    college_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    excelUtil.writeExcel(college_t, filePath, '各学院就业机会')

    major_changes = formulas.answer_major_value_rate(df_metrics, subject,
                                            [CONFIG.EXCEPTED_ANSWER], [CONFIG.RATE_COLUMN[2]], [0])
    major_t = formulas.major_rate_pivot(major_changes)
    major_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    excelUtil.writeExcel(major_t, filePath, '各专业就业机会')


def non_employee_report(data, filePath):
    '''未就业报告'''
    # 各选项占比
    df_value_count = formulas.answer_value_rate(data, 'C1')
    excelUtil.writeExcel(df_value_count, filePath, '一直未就业分布')

    df_value_count1 = formulas.answer_value_rate(data, 'C2')
    excelUtil.writeExcel(df_value_count1, filePath, '未就业毕业生目前去向分布')
    return


def income_report(data, filePath):
    # mean
    subject = 'B6'
    pd_mean = formulas.answer_mean(data, subject)
    excelUtil.writeExcel(pd_mean, filePath, '总体月均收入')

    pd_college_mean = formulas.single_grp_mean(data, subject,CONFIG.BASE_COLUMN[0],True)
    excelUtil.writeExcel(pd_college_mean, filePath, '各学院月均收入')

    pd_major_mean = formulas.major_mean(data, subject)
    excelUtil.writeExcel(pd_major_mean, filePath, '各专业月均收入')

    # 500
    start = 2000
    period_n = 4
    step = 500
    pd_500 = formulas.answer_period(data, subject, start, start + period_n * step, step)
    data_t=formulas.rate_T(pd_500,[CONFIG.MEAN_COLUMN[-1]])
    excelUtil.writeExcel(data_t, filePath, '毕业生月均收入及薪酬分布_' + str(step))

    step = 1000
    pd_1000 = formulas.answer_period(data, subject, start, start + period_n * step, step)
    data_t=formulas.rate_T(pd_1000)
    excelUtil.writeExcel(data_t, filePath, '毕业生月均收入及薪酬分布_' + str(step))

    step = 2000
    pd_2000 = formulas.answer_period(data, subject, start, start + period_n * step, step)
    data_t=formulas.rate_T(pd_2000)
    excelUtil.writeExcel(data_t, filePath, '毕业生月均收入及薪酬分布_' + str(step))

    step = 1500
    pd_1500 = formulas.answer_period(data, subject, start, start + period_n * step, step)
    data_t=formulas.rate_T(pd_1500)
    excelUtil.writeExcel(data_t, filePath, '毕业生月均收入及薪酬分布_' + str(step))
    return


def school_satisfy_report(data, filePath):
    '''母校满意度报告'''
    subject = 'H7'
    sheet_name='母校满意度'
    report_five_rate(data,subject,CONFIG.ANSWER_TYPE_SATISFY,sheet_name,filePath)

    return


def school_recommed_report(data, filePath):
    '''母校推荐报告'''

    df_value_rate = formulas.answer_value_rate(data, 'H8')
    df_value_rate.sort_values('比例', ascending=0, inplace=True)
    excelUtil.writeExcel(df_value_rate, filePath, '母校推荐度')

    df_college_rate = formulas.answer_college_value_rate(data, 'H8')
    df_college_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    excelUtil.writeExcel(df_college_rate, filePath, '各学院母校推荐度')

    df_major_rate = formulas.answer_major_value_rate(data, 'H8')
    df_major_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    excelUtil.writeExcel(df_major_rate, filePath, '各专业母校推荐度')

    return


def employee_difficult_report(data, filePath):
    '''求职过程报告'''
    data_a2 = data[data['A2'].isin([CONFIG.A2_ANSWER[0], CONFIG.A2_ANSWER[2]])]

    df_value_rate = formulas.answer_value_rate(data_a2, 'D2')
    df_value_rate.sort_values('比例', ascending=0, inplace=True)
    excelUtil.writeExcel(df_value_rate, filePath, '求职困难')

    df_major_rate = formulas.answer_major_value_rate(data_a2, 'D2')
    df_major_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    df_major_rate_five = df_major_rate.groupby(['学院', '专业'], as_index=False).head(3)
    df_concat = formulas.major_row_combine(df_major_rate_five)
    df_concat.sort_values(CONFIG.MEAN_COLUMN[2], 0, inplace=True)
    excelUtil.writeExcel(df_concat, filePath, '各专业求职困难')

    df_value_rate1 = formulas.answer_value_rate(data_a2, 'D1')
    df_value_rate1.sort_values('比例', ascending=1, inplace=True)
    excelUtil.writeExcel(df_value_rate1, filePath, '求职成功途径')

    return


def self_employed_report(data, filePath):
    '''自主创业报告'''
    business_rate = formulas.answer_rate(data, 'A2', CONFIG.A2_ANSWER[1])
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
    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_RELATIVE)
    excelUtil.writeExcel(df_mean, filePath, '创业行业与所学专业相关度')

    return


def basic_quality_report(data, file):
    '''基础素质报告'''
    subject = 'I2-1'
    df_distribution = answerUtil.multi_answer_distribution(data, subject)
    df_distribution.sort_values([CONFIG.RATE_COLUMN[-1]], ascending=[0], inplace=True)
    excelUtil.writeExcel(df_distribution, file, '重要度')

    subject='I2-2'
    df_ability=answerUtil.ability_distribution(data,subject)
    df_ability.sort_values(CONFIG.RATE_COLUMN[1],ascending=0,inplace=True)
    excelUtil.writeExcel(df_ability, file, '满足度')



def major_quality_report(data, file):
    '''专业素质报告'''
    subject = 'I1-1'
    df_mean_1 = formulas.answer_five_rate(data, subject + '-A', CONFIG.ANSWER_TYPE_IMPORTANT)
    df_mean_1['题目'] = 'I1-1-A'
    df_mean_2 = formulas.answer_five_rate(data, subject + '-B', CONFIG.ANSWER_TYPE_IMPORTANT)
    df_mean_2['题目'] = 'I1-1-B'
    pd_concat = pd.concat([df_mean_1, df_mean_2])
    excelUtil.writeExcel(pd_concat, file, '专业素质重要性')

    subject = 'I1-2'
    df_mean_1 = formulas.answer_five_rate(data, subject + '-A', CONFIG.ANSWER_TYPE_PLEASED)
    df_mean_1['题目'] = 'I1-2-A'
    df_mean_2 = formulas.answer_five_rate(data, subject + '-B', CONFIG.ANSWER_TYPE_PLEASED)
    df_mean_2['题目'] = 'I1-2-B'
    pd_concat = pd.concat([df_mean_1, df_mean_2])
    excelUtil.writeExcel(pd_concat, file, '专业素质满意度')

    return


def evelution_lesson_report(data, file):
    '''课堂教学报告'''
    subject = 'H2'
    sub_column = answerUtil.multi_columns(data, subject)
    ls_column = list(CONFIG.MEAN_COLUMN)
    ls_column = ls_column.append('题目')
    df_init1 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    df_init2 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    df_init3 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe

    for col in sub_column:
        df_mean = formulas.answer_five_rate(data, col, CONFIG.ANSWER_TYPE_MEET_V)
        df_mean['题目'] = col
        df_init1 = pd.concat([df_init1, df_mean])

        df_grp = formulas.answer_five_rate_single_grp(data, col, '_10', CONFIG.ANSWER_TYPE_MEET_V)
        df_mean['题目'] = col
        df_init2 = pd.concat([df_init2, df_mean])

        df_major = formulas.answer_five_rate_major_grp(data, col, CONFIG.ANSWER_TYPE_MEET_V)
        df_major['题目'] = col
        df_init3 = pd.concat([df_init3, df_mean])

    excelUtil.writeExcel(df_init1, file, '课堂教学各方面评价')
    excelUtil.writeExcel(df_init2, file, '学院课堂教学各方面评价')
    excelUtil.writeExcel(df_init3, file, '专业课堂教学各方面评价')

    return


def evelution_practice_report(data, file):
    '''实践教学报告'''
    subject = 'H3'
    sub_column = answerUtil.multi_columns(data, subject, 4)
    ls_column = list(CONFIG.MEAN_COLUMN)
    ls_column = ls_column.append('题目')
    df_init1 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    df_init2 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    df_init3 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe

    for col in sub_column:
        df_mean = formulas.answer_five_rate(data, col, CONFIG.ANSWER_TYPE_HELP)
        df_mean['题目'] = col
        df_init1 = pd.concat([df_init1, df_mean])

        df_grp = formulas.answer_five_rate_single_grp(data, col, '_10', CONFIG.ANSWER_TYPE_HELP)
        df_mean['题目'] = col
        df_init2 = pd.concat([df_init2, df_mean])

        df_major = formulas.answer_five_rate_major_grp(data, col, CONFIG.ANSWER_TYPE_HELP)
        df_major['题目'] = col
        df_init3 = pd.concat([df_init3, df_major])

    excelUtil.writeExcel(df_mean, file, '实践教学各方面评价')
    excelUtil.writeExcel(df_grp, file, '学院实践教学各方面评价')
    excelUtil.writeExcel(df_major, file, '专业实践教学各方面评价')

    return


def evelution_teach_report(data, file):
    '''任课教师评价'''
    subject = 'H4'
    sub_column = answerUtil.multi_columns(data, subject, 4)

    ls_column = list(CONFIG.MEAN_COLUMN)
    ls_column = ls_column.append('题目')
    df_init1 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    df_init2 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    df_init3 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe

    for col in sub_column:
        df_mean = formulas.answer_five_rate(data, col, CONFIG.ANSWER_TYPE_SATISFY)
        df_mean['题目'] = col
        df_init1 = pd.concat([df_init1, df_mean])

        df_grp = formulas.answer_five_rate_single_grp(data, col, '_10', CONFIG.ANSWER_TYPE_SATISFY)
        df_grp['题目'] = col
        df_init2 = pd.concat([df_init2, df_grp])

        df_major = formulas.answer_five_rate_major_grp(data, col, CONFIG.ANSWER_TYPE_SATISFY)
        df_major['题目'] = col
        df_init3 = pd.concat([df_init3, df_major])

    excelUtil.writeExcel(df_init1, file, '对任课教师的评价')
    excelUtil.writeExcel(df_init2, file, '各学院对任课教师的评价')
    excelUtil.writeExcel(df_init3, file, '各专业对任课教师的评价')

    return


def evelution_H4_ALL_report(data, file):
    '''H4组合'''
    subject = 'H4'
    sub_column = answerUtil.multi_columns(data, subject)

    ls_column = list(CONFIG.MEAN_COLUMN)
    ls_column = ls_column.append('题目')
    df_init1 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    df_init2 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    df_init3 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe

    for col in sub_column:
        df_mean = formulas.answer_five_rate(data, col, CONFIG.ANSWER_TYPE_SATISFY)
        df_mean['题目'] = col
        df_init1 = pd.concat([df_init1, df_mean])

        df_grp = formulas.answer_five_rate_single_grp(data, col, '_10', CONFIG.ANSWER_TYPE_SATISFY)
        df_grp['题目'] = col
        df_init2 = pd.concat([df_init2, df_grp])

        df_major = formulas.answer_five_rate_major_grp(data, col, CONFIG.ANSWER_TYPE_SATISFY)
        df_major['题目'] = col
        df_init3 = pd.concat([df_init3, df_major])

    excelUtil.writeExcel(df_init1, file, 'H4组合评价')
    excelUtil.writeExcel(df_init2, file, '学院H4组合评价')
    excelUtil.writeExcel(df_init3, file, '专业H4组合评价')

    return


def evelution_H4_E_report(data, file):
    '''母校任课教师总体报告'''
    subject = 'H4-E'

    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)

    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    excelUtil.writeExcel(df_mean, file, '母校任课教师总体评价')
    excelUtil.writeExcel(df_grp, file, '各学院对母校任课教师总体评价')
    excelUtil.writeExcel(df_major, file, '各专业对母校任课教师总体评价')

    return


def evelution_academic_report(data, file):
    '''母校的学风报告'''
    subject = '附5-5'

    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_FEEL)

    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_FEEL)

    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_FEEL)

    excelUtil.writeExcel(df_mean, file, '母校的学风总体评价')
    excelUtil.writeExcel(df_grp, file, '各学院对母校的学风评价')
    excelUtil.writeExcel(df_major, file, '各专业对母校的学风评价')

    return


def evelution_H4_T_report(data, file):
    '''教育教学报告'''
    subject = 'H4-T'

    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)

    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    excelUtil.writeExcel(df_mean, file, '教育教学总体评价')
    excelUtil.writeExcel(df_grp, file, '各学院对教育教学评价')
    excelUtil.writeExcel(df_major, file, '各专业对教育教学评价')

    return


def evelution_H4_S_report(data, file):
    '''实践教学报告'''
    subject = 'H4-S'

    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)

    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    excelUtil.writeExcel(df_mean, file, '实践教学总体评价')
    excelUtil.writeExcel(df_grp, file, '各学院对实践教学评价')
    excelUtil.writeExcel(df_major, file, '各专业对实践教学评价')

    return


def evelution_H4_R_report(data, file):
    '''社团活动报告'''
    subject = 'H4-R'

    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)

    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    excelUtil.writeExcel(df_mean, file, '社团活动总体评价')
    excelUtil.writeExcel(df_grp, file, '各学院对社团活动评价')
    excelUtil.writeExcel(df_major, file, '各专业对社团活动评价')

    return


def evelution_H4_P_report(data, file):
    '''母校学生管理报告'''
    subject = 'H4-P'

    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)

    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    subject = 'H5'
    df_distribution = answerUtil.multi_answer_distribution(data, subject)
    df_distribution.sort_values([CONFIG.RATE_COLUMN[-1]], ascending=[0], inplace=True)

    excelUtil.writeExcel(df_mean, file, '母校学生管理总体评价')
    excelUtil.writeExcel(df_grp, file, '各学院对母校学生管理评价')
    excelUtil.writeExcel(df_major, file, '各专业对母校学生管理评价')
    excelUtil.writeExcel(df_distribution, file, '学生管理工作改进')

    return


def evelution_H4_Q_report(data, file):
    '''母校生活服务报告'''
    subject = 'H4-Q'

    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)

    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    subject = 'H6'
    df_distribution = answerUtil.multi_answer_distribution(data, subject)
    df_distribution.sort_values([CONFIG.RATE_COLUMN[-1]], ascending=[0], inplace=True)

    excelUtil.writeExcel(df_mean, file, '母校生活服务总体评价')
    excelUtil.writeExcel(df_grp, file, '各学院对母校生活服务评价')
    excelUtil.writeExcel(df_major, file, '各专业对母校生活服务评价')
    excelUtil.writeExcel(df_distribution, file, '生活服务改进')

    return


def evelution_H4_L_O_report(data, file):
    '''创业教育报告'''
    ls_column = list(CONFIG.MEAN_COLUMN)
    ls_column = ls_column.append('题目')
    df_init1 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    df_init2 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    df_init3 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe

    df_init4 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    df_init5 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    df_init6 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe

    subject = 'H4-L'
    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_mean['题目'] = '创业课程和讲座'
    df_init1 = pd.concat([df_init1, df_mean])
    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)
    df_grp['题目'] = '创业课程和讲座'
    df_init2 = pd.concat([df_init2, df_grp])
    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_major['题目'] = '创业课程和讲座'
    df_init3 = pd.concat([df_init3, df_major])

    subject = 'H4-M'
    title = '创新创业大赛'
    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_mean['题目'] = title
    df_init1 = pd.concat([df_init1, df_mean])
    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)
    df_grp['题目'] = title
    df_init2 = pd.concat([df_init2, df_grp])
    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_major['题目'] = title
    df_init3 = pd.concat([df_init3, df_major])

    subject = 'H4-N'
    title = '创业模拟与实训'
    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_mean['题目'] = title
    df_init1 = pd.concat([df_init1, df_mean])
    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)
    df_grp['题目'] = title
    df_init2 = pd.concat([df_init2, df_grp])
    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_major['题目'] = title
    df_init3 = pd.concat([df_init3, df_major])

    subject = 'H4-O'
    title = '创业指导服务'
    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_mean['题目'] = title
    df_init1 = pd.concat([df_init1, df_mean])
    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)
    df_grp['题目'] = title
    df_init2 = pd.concat([df_init2, df_grp])
    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_major['题目'] = title
    df_init3 = pd.concat([df_init3, df_major])

    subject = 'H3-E'
    title = '创业场地支持'
    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_HELP)
    df_mean['题目'] = title
    df_init4 = pd.concat([df_init4, df_mean])
    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_HELP)
    df_grp['题目'] = title
    df_init5 = pd.concat([df_init5, df_grp])
    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_HELP)
    df_major['题目'] = title
    df_init6 = pd.concat([df_init6, df_major])

    subject = 'H3-F'
    title = '创业资金支持'
    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_HELP)
    df_mean['题目'] = title
    df_init4 = pd.concat([df_init4, df_mean])
    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_HELP)
    df_grp['题目'] = title
    df_init5 = pd.concat([df_init5, df_grp])
    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_HELP)
    df_major['题目'] = title
    df_init6 = pd.concat([df_init6, df_major])

    excelUtil.writeExcel(df_init1, file, '创业教育总体评价')
    excelUtil.writeExcel(df_init2, file, '各学院对创业教育评价')
    excelUtil.writeExcel(df_init3, file, '各专业对创业教育评价')
    excelUtil.writeExcel(df_init4, file, '创业总体支持')
    excelUtil.writeExcel(df_init5, file, '各学院对创业支持')
    excelUtil.writeExcel(df_init6, file, '各专业对创业支持')

    return


def evelution_H4_F_K_report(data, file):
    '''就业教育服务报告'''
    ls_column = list(CONFIG.MEAN_COLUMN)
    ls_column = ls_column.append('题目')
    df_init1 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    df_init2 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    df_init3 = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe

    subject = 'H4-F'
    title = '生涯规划和就业指导'
    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_mean['题目'] = title
    df_init1 = pd.concat([df_init1, df_mean])
    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)
    df_grp['题目'] = title
    df_init2 = pd.concat([df_init2, df_grp])
    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_major['题目'] = title
    df_init3 = pd.concat([df_init3, df_major])

    subject = 'H4-G'
    title = '职业咨询与辅导'
    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_mean['题目'] = title
    df_init1 = pd.concat([df_init1, df_mean])
    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)
    df_grp['题目'] = title
    df_init2 = pd.concat([df_init2, df_grp])
    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_major['题目'] = title
    df_init3 = pd.concat([df_init3, df_major])

    subject = 'H4-H'
    title = '校园招聘会'
    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_mean['题目'] = title
    df_init1 = pd.concat([df_init1, df_mean])
    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)
    df_grp['题目'] = title
    df_init2 = pd.concat([df_init2, df_grp])
    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_major['题目'] = title
    df_init3 = pd.concat([df_init3, df_major])

    subject = 'H4-I'
    title = '学校招聘信息发布'
    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_mean['题目'] = title
    df_init1 = pd.concat([df_init1, df_mean])
    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)
    df_grp['题目'] = title
    df_init2 = pd.concat([df_init2, df_grp])
    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_major['题目'] = title
    df_init3 = pd.concat([df_init3, df_major])
    subject = 'H4-J'
    title = '就业帮助与推荐'
    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_mean['题目'] = title
    df_init1 = pd.concat([df_init1, df_mean])
    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)
    df_grp['题目'] = title
    df_init2 = pd.concat([df_init2, df_grp])
    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_major['题目'] = title
    df_init3 = pd.concat([df_init3, df_major])
    subject = 'H4-K'
    title = '就业手续办理'
    df_mean = formulas.answer_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_mean['题目'] = title
    df_init1 = pd.concat([df_init1, df_mean])
    df_grp = formulas.answer_five_rate_single_grp(data, subject, '_10', CONFIG.ANSWER_TYPE_SATISFY)
    df_grp['题目'] = title
    df_init2 = pd.concat([df_init2, df_grp])
    df_major = formulas.answer_five_rate_major_grp(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_major['题目'] = title
    df_init3 = pd.concat([df_init3, df_major])
    excelUtil.writeExcel(df_init1, file, '就业教育服务总体评价')
    excelUtil.writeExcel(df_init2, file, '各学院对就业教育服务评价')
    excelUtil.writeExcel(df_init3, file, '各专业对就业教育服务评价')


####################   就业竞争力
def major_relative_report(data, filePath):
    '''专业相关度'''
    subject = 'B9-1'
    measure_name = formulas.parse_measure_name(CONFIG.ANSWER_TYPE_RELATIVE)
    ls_metrics_cols = list(CONFIG.BASE_COLUMN)
    ls_metrics_cols.append(subject)
    df_metrics = data[ls_metrics_cols]

    pd_summary = formulas.answer_five_rate(df_metrics, subject, CONFIG.ANSWER_TYPE_RELATIVE)
    summary_t = formulas.rate_T(pd_summary, [measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]])
    excelUtil.writeExcel(summary_t, filePath, '总体专业相关情况')

    pd_college = formulas.answer_five_rate_single_grp(df_metrics, subject,
                                             CONFIG.BASE_COLUMN[0],
                                             CONFIG.ANSWER_TYPE_RELATIVE,
                                             is_college=True)
    college_t = formulas.college_rate_pivot(pd_college, [measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]],
                                            False)
    college_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    excelUtil.writeExcel(college_t, filePath, '各学院专业相关情况')

    pd_major = formulas.answer_five_rate_major_grp(df_metrics, subject, CONFIG.ANSWER_TYPE_RELATIVE)
    major_t = formulas.major_rate_pivot(pd_major, [measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]])
    major_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    excelUtil.writeExcel(major_t, filePath, '各专业专业相关情况')

    subject = 'B9-2'
    ls_metrics_cols1 = list(CONFIG.BASE_COLUMN)
    ls_metrics_cols1.append(subject)
    df_metrics = data[ls_metrics_cols1]
    pd_unrelative = formulas.answer_value_rate(df_metrics, subject)
    pd_unrelative.sort_values([CONFIG.RATE_COLUMN[-1]], ascending=[0], inplace=True)
    excelUtil.writeExcel(pd_unrelative, filePath, '从事低专业相关工作的原因分布')


def common_five_report(df_data, subject, filePath, sheetName, measureType):
    measure_name = formulas.parse_measure_name(measureType)
    ls_metrics_cols = list(CONFIG.BASE_COLUMN)
    ls_metrics_cols.append(subject)
    df_metrics = df_data[ls_metrics_cols]

    pd_summary = formulas.answer_five_rate(df_metrics, subject, measureType)
    summary_t = formulas.rate_T(pd_summary, [measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]])
    excelUtil.writeExcel(summary_t, filePath, '总体' + sheetName)

    pd_college = formulas.answer_five_rate_single_grp(df_metrics, subject,
                                             CONFIG.BASE_COLUMN[0],
                                             measureType)
    college_t = formulas.college_rate_pivot(pd_college,
                                            [measure_name,
                                             CONFIG.MEAN_COLUMN[-1],
                                             CONFIG.MEAN_COLUMN[2]],
                                            False)
    college_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    excelUtil.writeExcel(college_t, filePath, '各学院' + sheetName)

    pd_major = formulas.answer_five_rate_major_grp(df_metrics, subject, measureType)
    major_t = formulas.major_rate_pivot(pd_major,
                                        [measure_name, CONFIG.MEAN_COLUMN[-1],
                                         CONFIG.MEAN_COLUMN[2]])
    major_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    excelUtil.writeExcel(major_t, filePath, '各专业' + sheetName)


def job_meet_report(data, filePath):
    '''职业期待吻合度'''
    subject = 'B8'
    measure_name = formulas.parse_measure_name(CONFIG.ANSWER_TYPE_MEET)
    ls_metrics_cols = list(CONFIG.BASE_COLUMN)
    ls_metrics_cols.append(subject)
    df_metrics = data[ls_metrics_cols]

    pd_summary = formulas.answer_five_rate(df_metrics, subject, CONFIG.ANSWER_TYPE_MEET)
    summary_t = formulas.rate_T(pd_summary, [measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]])
    excelUtil.writeExcel(summary_t, filePath, '总体职业期待吻合情况')

    pd_college = formulas.answer_five_rate_single_grp(df_metrics, subject,
                                             CONFIG.BASE_COLUMN[0],
                                             CONFIG.ANSWER_TYPE_MEET)
    college_t = formulas.college_rate_pivot(pd_college, [measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]],
                                            False)
    college_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    excelUtil.writeExcel(college_t, filePath, '学院职业期待吻合情况')

    pd_major = formulas.answer_five_rate_major_grp(df_metrics, subject, CONFIG.ANSWER_TYPE_MEET)
    major_t = formulas.major_rate_pivot(pd_major, [measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]])
    major_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    excelUtil.writeExcel(major_t, filePath, '各专业职业期待吻合情况')


def job_satisfy_report(data, filePath):
    '''职业满意度'''

    subject = 'B7-A'
    measureType = CONFIG.ANSWER_TYPE_SATISFY
    sheetName = "对工作总体的满意情况"
    common_five_report(data, subject, filePath, sheetName, measureType)

    subject = 'B7-B'
    sheetName = "对工作薪酬的满意情况"
    common_five_report(data, subject, filePath, sheetName, measureType)

    subject = 'B7-C'
    sheetName = "对职业发展前景的满意情况"
    common_five_report(data, subject, filePath, sheetName, measureType)

    subject = 'B7-D'
    sheetName = "对工作内容意的满意情况"
    common_five_report(data, subject, filePath, sheetName, measureType)


def special_employee_featured(data, dict_where={}):
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
                           df_male_region, df_male_job], axis=1)
    return df_concat


def special_employee_competitive(data, dict_where={}):
    '''特殊人群就业竞争力分析'''
    # 就业率
    df_income = formulas.formulas_employe_rate(data, dict_where)

    # 薪酬
    df_salary = formulas.formula_income_mean(data, dict_where)
    if dict_where:
        col_cond = str(dict_where[CONFIG.DICT_KEY[0]])
        df_data = data[data[col_cond] == dict_where[CONFIG.DICT_KEY[1]]]
    else:
        df_data = data

    # 专业相关度
    subject = 'B9-1'
    df_major_relative = formulas.answer_five_rate(df_data, subject, CONFIG.ANSWER_TYPE_RELATIVE)

    # 工作满意度
    subject = 'B7-A'
    df_job_satisfy = formulas.answer_five_rate(df_data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    # 薪酬满意度
    subject = 'B7-B'
    df_salary_satisfy = formulas.answer_five_rate(df_data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    # 职业发展前景满意度
    subject = 'B7-C'
    df_industry_satisfy = formulas.answer_five_rate(df_data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    # 工作内容满意度
    subject = 'B7-D'
    df_job_content_satisfy = formulas.answer_five_rate(df_data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    # 职业期待吻合度
    subject = 'B8'
    df_job_hope = formulas.answer_five_rate(df_data, subject, CONFIG.ANSWER_TYPE_MEET)

    # 离职率
    subject = 'B10-1'
    change_times = formulas.answer_value_rate(data, subject)
    no_changes = change_times[change_times[CONFIG.RATE_COLUMN[0]].isin([CONFIG.B10_1_ANSWER[0]])][
        [CONFIG.RATE_COLUMN[-1]]]
    no_changes.fillna(0, inplace=True)
    change_times['离职率'] = 100 - no_changes

    df_concat = pd.concat([df_income, df_salary, df_major_relative, df_job_satisfy,
                           df_salary_satisfy, df_industry_satisfy,
                           df_job_content_satisfy, df_job_hope, change_times], axis=1)
    print(df_concat)
    return df_concat


def special_lesson(data, dict_where={}):
    '''特殊人课堂教学分析'''
    subject = 'H2'

    if dict_where:
        col_cond = str(dict_where[CONFIG.DICT_KEY[0]])
        df_data = data[data[col_cond] == dict_where[CONFIG.DICT_KEY[1]]]
    else:
        df_data = data

    sub_column = answerUtil.multi_columns(df_data, subject)
    ls_column = list(CONFIG.MEAN_COLUMN)
    ls_column = ls_column.append('题目')
    df_init = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    for col in sub_column:
        df_mean = formulas.answer_five_rate(data, col, CONFIG.ANSWER_TYPE_MEET_V)
        df_mean['题目'] = col
        df_init = pd.concat([df_init, df_mean])
    print(df_init)
    return df_init


def special_practice(data, dict_where={}):
    '''特殊人群实践教学报告'''
    subject = 'H3'

    if dict_where:
        col_cond = str(dict_where[CONFIG.DICT_KEY[0]])
        df_data = data[data[col_cond] == dict_where[CONFIG.DICT_KEY[1]]]
    else:
        df_data = data

    sub_column = answerUtil.multi_columns(df_data, subject)
    ls_column = list(CONFIG.MEAN_COLUMN)
    ls_column = ls_column.append('题目')
    df_init = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    for col in sub_column:
        df_mean = formulas.answer_five_rate(data, col, CONFIG.ANSWER_TYPE_HELP)
        df_mean['题目'] = col
        df_init = pd.concat([df_init, df_mean])
    return df_init


def special_teacher(data, dict_where={}):
    '''特殊人群教师评价'''
    subject = 'H4'
    if dict_where:
        col_cond = str(dict_where[CONFIG.DICT_KEY[0]])
        df_data = data[data[col_cond] == dict_where[CONFIG.DICT_KEY[1]]]
    else:
        df_data = data

    sub_column = answerUtil.multi_columns(df_data, subject)
    ls_column = list(CONFIG.MEAN_COLUMN)
    ls_column = ls_column.append('题目')
    df_init = pd.DataFrame(columns=ls_column)  # 创建一个空的dataframe
    for col in sub_column:
        df_mean = formulas.answer_five_rate(data, col, CONFIG.ANSWER_TYPE_SATISFY)
        df_mean['题目'] = col
        df_init = pd.concat([df_init, df_mean])
    return df_init


def special_school(data, dict_where={}):
    '''特殊人群学校总体评价'''
    if dict_where:
        col_cond = str(dict_where[CONFIG.DICT_KEY[0]])
        df_data = data[data[col_cond] == dict_where[CONFIG.DICT_KEY[1]]]
    else:
        df_data = data

    # 学校满意度
    subject = 'H7'
    df_mean_satisfy = formulas.answer_five_rate(df_data, subject, CONFIG.ANSWER_TYPE_SATISFY)

    # 学校推荐度
    df_recommend = formulas.answer_value_rate(df_data, 'H8')

    df_result = pd.concat([df_mean_satisfy, df_recommend], axis=1)
    return df_result


def special_gender_report(data, filePath):
    subject = '_3'
    suffix = '不同性别'

    dict_where1 = {CONFIG.DICT_KEY[0]: subject, CONFIG.DICT_KEY[1]: CONFIG.GENDER[0]}
    dict_where2 = {CONFIG.DICT_KEY[0]: subject, CONFIG.DICT_KEY[1]: CONFIG.GENDER[1]}

    df_emp_feature1 = special_employee_featured(data, dict_where1)
    df_emp_feature1['条件'] = dict_where1[CONFIG.DICT_KEY[1]]
    df_emp_feature2 = special_employee_featured(data, dict_where2)
    df_emp_feature2['条件'] = dict_where2[CONFIG.DICT_KEY[1]]
    df_emp_feature = special_employee_featured(data)
    df_emp_feature['条件'] = CONFIG.TOTAL_COLUMN

    df_concat = pd.concat([df_emp_feature1, df_emp_feature2, df_emp_feature])
    excelUtil.writeExcel(df_concat, filePath, suffix + '就业特色')

    df_emp_competitive1 = special_employee_competitive(data, dict_where1)
    df_emp_competitive1['条件'] = dict_where1[CONFIG.DICT_KEY[1]]
    df_emp_competitive2 = special_employee_competitive(data, dict_where2)
    df_emp_competitive2['条件'] = dict_where2[CONFIG.DICT_KEY[1]]
    df_emp_competitive = special_employee_competitive(data)
    df_emp_competitive['条件'] = CONFIG.TOTAL_COLUMN

    df_concat = pd.concat([df_emp_competitive1, df_emp_competitive2, df_emp_competitive])
    excelUtil.writeExcel(df_concat, filePath, suffix + '就业竞争力')

    df_lesson1 = special_lesson(data, dict_where1)
    df_lesson1['条件'] = dict_where1[CONFIG.DICT_KEY[1]]
    df_lesson2 = special_lesson(data, dict_where2)
    df_lesson2['条件'] = dict_where2[CONFIG.DICT_KEY[1]]
    df_lesson = special_lesson(data)
    df_lesson['条件'] = CONFIG.TOTAL_COLUMN
    df_concat = pd.concat([df_lesson1, df_lesson2, df_lesson])
    excelUtil.writeExcel(df_concat, filePath, suffix + '就业课堂教学')

    df_practice1 = special_practice(data, dict_where1)
    df_practice1['条件'] = dict_where1[CONFIG.DICT_KEY[1]]
    df_practice2 = special_practice(data, dict_where2)
    df_practice2['条件'] = dict_where2[CONFIG.DICT_KEY[1]]
    df_practice = special_practice(data)
    df_practice['条件'] = CONFIG.TOTAL_COLUMN
    df_concat = pd.concat([df_practice1, df_practice2, df_practice])
    excelUtil.writeExcel(df_concat, filePath, suffix + '实践教学')

    df_teacher1 = special_teacher(data, dict_where1)
    df_teacher1['条件'] = dict_where1[CONFIG.DICT_KEY[1]]
    df_teacher2 = special_teacher(data, dict_where2)
    df_teacher2['条件'] = dict_where2[CONFIG.DICT_KEY[1]]
    df_teacher = special_teacher(data)
    df_teacher['条件'] = CONFIG.TOTAL_COLUMN
    df_concat = pd.concat([df_teacher1, df_teacher2, df_teacher])
    excelUtil.writeExcel(df_concat, filePath, suffix + '教师评价')

    df_school1 = special_school(data, dict_where1)
    df_school1['条件'] = dict_where1[CONFIG.DICT_KEY[1]]
    df_school2 = special_school(data, dict_where2)
    df_school2['条件'] = dict_where2[CONFIG.DICT_KEY[1]]
    df_school = special_school(data)
    df_school['条件'] = CONFIG.TOTAL_COLUMN
    df_concat = pd.concat([df_school1, df_school2, df_school])
    excelUtil.writeExcel(df_concat, filePath, suffix + '母校总和评价')

    return


def special_national_report(data, filePath):
    '''特殊人群民族报告'''
    subject = '_16'
    suffix = '不同名族'

    dict_where = {CONFIG.DICT_KEY[0]: subject, CONFIG.DICT_KEY[1]: CONFIG.NATIONAL_COLUMN[0]}
    special_common_report(data, subject, filePath, suffix, dict_where, CONFIG.NATIONAL_COLUMN)
    return


def special_origin_province_report(data, filePath):
    '''特殊人群生源地报告'''
    subject = 'A1-A'
    suffix = '省内省外生源'
    province = '福建省'

    dict_where = {CONFIG.DICT_KEY[0]: subject, CONFIG.DICT_KEY[1]: province}
    special_common_report(data, subject, filePath, suffix, dict_where, CONFIG.ORIGIN_COLUMN)
    return


def special_indurstry_province_report(data, filePath):
    '''特殊人群省内省外就业报告'''
    subject = 'B3-A'
    suffix = '省内省外就业'
    province = '福建省'

    dict_where = {CONFIG.DICT_KEY[0]: subject, CONFIG.DICT_KEY[1]: province}
    special_common_report(data, subject, filePath, suffix, dict_where, CONFIG.INDUSTRY_COLUMN)
    return


def special_education_report(data, filePath):
    '''特殊人群教育和非教育就业报告'''
    subject = 'B5-B'
    suffix = '教育和非教育'
    education = '教育'

    dict_where = {CONFIG.DICT_KEY[0]: subject, CONFIG.DICT_KEY[1]: education}
    special_common_report(data, subject, filePath, suffix, dict_where, CONFIG.ORIGIN_COLUMN)
    return


def special_teacher_report(data, filePath):
    '''特殊人群师范和非师范就业报告'''
    subject = 'B5-B'
    suffix = '师范和非师范'
    where = '师范'

    dict_where = {CONFIG.DICT_KEY[0]: subject, CONFIG.DICT_KEY[1]: where}
    special_common_report(data, subject, filePath, suffix, dict_where, CONFIG.EDUCATION_COLUMN)
    return


def special_medical_report(data, filePath):
    '''特殊人群医疗卫生就业报告'''
    subject = 'B4-A'
    suffix = '医疗卫生'
    where = '医疗卫生'

    dict_where = {CONFIG.DICT_KEY[0]: subject, CONFIG.DICT_KEY[1]: where}
    special_common_report(data, subject, filePath, suffix, dict_where, CONFIG.MEDICAL_COLUMN)
    return


def special_social_health_report(data, filePath):
    '''特殊人群卫生和社会报告'''
    subject = 'B5-A'
    suffix = '卫生和社会工作'
    where = '卫生和社会工作'

    dict_where = {CONFIG.DICT_KEY[0]: subject, CONFIG.DICT_KEY[1]: where}
    special_common_report(data, subject, filePath, suffix, dict_where, CONFIG.HEALTH_COLUMN)
    return


def special_admissions_report(data, filePath):
    '''特殊招生渠道就业报告'''
    subject = 'B4-B'
    suffix = '医药卫生'
    where = '医药卫生'

    dict_where = {CONFIG.DICT_KEY[0]: subject, CONFIG.DICT_KEY[1]: where}
    special_common_report(data, subject, filePath, suffix, dict_where, CONFIG.EDUCATION_COLUMN)
    return


def special_common_report(data, subject, filePath, suffix, dict_where, tuple_title):
    col_cond = str(dict_where[CONFIG.DICT_KEY[0]])
    df_data1 = data[data[col_cond] == dict_where[CONFIG.DICT_KEY[1]]]
    cond1 = tuple_title[0]

    df_data2 = data[data[subject] != dict_where[CONFIG.DICT_KEY[1]]]
    cond2 = tuple_title[1]

    df_emp_feature1 = special_employee_featured(df_data1)
    df_emp_feature1['条件'] = cond1
    df_emp_feature2 = special_employee_featured(df_data2)
    df_emp_feature2['条件'] = cond2
    df_emp_feature = special_employee_featured(data)
    df_emp_feature['条件'] = CONFIG.TOTAL_COLUMN

    df_concat = pd.concat([df_emp_feature1, df_emp_feature2, df_emp_feature])
    excelUtil.writeExcel(df_concat, filePath, suffix + '就业特色')

    df_emp_competitive1 = special_employee_competitive(df_data1)
    df_emp_competitive1['条件'] = cond1
    df_emp_competitive2 = special_employee_competitive(df_data2)
    df_emp_competitive2['条件'] = cond2
    df_emp_competitive = special_employee_competitive(data)
    df_emp_competitive['条件'] = CONFIG.TOTAL_COLUMN

    df_concat = pd.concat([df_emp_competitive1, df_emp_competitive2, df_emp_competitive])
    excelUtil.writeExcel(df_concat, filePath, suffix + '就业竞争力')

    df_lesson1 = special_lesson(df_data1)
    df_lesson1['条件'] = cond1
    df_lesson2 = special_lesson(df_data2)
    df_lesson2['条件'] = cond2
    df_lesson = special_lesson(data)
    df_lesson['条件'] = CONFIG.TOTAL_COLUMN
    df_concat = pd.concat([df_lesson1, df_lesson2, df_lesson])
    excelUtil.writeExcel(df_concat, filePath, suffix + '就业课堂教学')

    df_practice1 = special_practice(df_data1)
    df_practice1['条件'] = cond1
    df_practice2 = special_practice(df_data1)
    df_practice2['条件'] = cond2
    df_practice = special_practice(data)
    df_practice['条件'] = CONFIG.TOTAL_COLUMN
    df_concat = pd.concat([df_practice1, df_practice2, df_practice])
    excelUtil.writeExcel(df_concat, filePath, suffix + '实践教学')

    df_teacher1 = special_teacher(df_data1)
    df_teacher1['条件'] = cond1
    df_teacher2 = special_teacher(df_data1)
    df_teacher2['条件'] = cond2
    df_teacher = special_teacher(data)
    df_teacher['条件'] = CONFIG.TOTAL_COLUMN
    df_concat = pd.concat([df_teacher1, df_teacher2, df_teacher])
    excelUtil.writeExcel(df_concat, filePath, suffix + '教师评价')

    df_school1 = special_school(df_data1)
    df_school1['条件'] = cond1
    df_school2 = special_school(df_data2)
    df_school2['条件'] = cond2
    df_school = special_school(data)
    df_school['条件'] = CONFIG.TOTAL_COLUMN
    df_concat = pd.concat([df_school1, df_school2, df_school])
    excelUtil.writeExcel(df_concat, filePath, suffix + '母校总和评价')

    return


def rebuild_five_columns(measure_type, level=0):
    # 用于重排转置后的列的顺序
    five_metric = formulas.parse_measure(measure_type)
    five_metric = five_metric[0:-1]

    # 学院、专业、五纬排序、度量值、均值、答题总人数
    metric_name=formulas.parse_measure_name(measure_type)
    order_column =five_metric.copy()
    if level==1:
        order_column.insert(0, CONFIG.GROUP_COLUMN[0])
    elif level==2:
        order_column.insert(0, CONFIG.GROUP_COLUMN[0])
        order_column.insert(1, CONFIG.GROUP_COLUMN[1])
    order_column.append(metric_name)
    order_column.append(CONFIG.MEAN_COLUMN[-1])
    order_column.append(CONFIG.MEAN_COLUMN[2])
    return order_column

def report_five_rate(data,subject,measure_type,measure_name,file_path):
    if data.empty:
        return data
    if not subject or not measure_type:
        return data

    ls_metrics_cols = list(CONFIG.BASE_COLUMN)
    ls_metrics_cols.append(subject)
    df_metrics = data.loc[:,ls_metrics_cols]

    focus_name=formulas.parse_measure_name(measure_type)
    array_focus=[focus_name,CONFIG.MEAN_COLUMN[-1]]

    value_rate = formulas.answer_five_rate(df_metrics, subject, measure_type)
    rate_t = formulas.rate_T(value_rate, array_focus)
    rate_t=rate_t.loc[:,rebuild_five_columns(measure_type,0)]
    rate_combin=pd.concat([rate_t,rate_t])
    excelUtil.writeExcel(rate_combin, file_path, '总体'+measure_name)

    college_changes = formulas.answer_five_rate_single_grp(df_metrics, subject,
                                                CONFIG.BASE_COLUMN[0], measure_type, is_college=True)
    college_t = formulas.college_rate_pivot(college_changes,
                                            array_focus)
    college_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    college_t=college_t.loc[:,rebuild_five_columns(measure_type,1)]
    college_combine=pd.concat([college_t,rate_t],sort=False)
    excelUtil.writeExcel(college_combine, file_path, '各学院'+measure_name)

    major_changes = formulas.answer_five_rate_major_grp(df_metrics, subject,measure_type)
    major_t = formulas.major_rate_pivot(major_changes,
                                        array_focus)
    major_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    major_t=major_t.loc[:,rebuild_five_columns(measure_type,2)]
    major_conbine=pd.concat([major_t,rate_t],sort=False)
    excelUtil.writeExcel(major_conbine, file_path, '各专业'+measure_name)
    return

def demission_reason(data, subject):
    '''
    离职原因统计
    :param data:
    :param subject:
    :return:
    '''
    column_relative = list(CONFIG.BASE_COLUMN)
    column_relative.append(subject)
    print(column_relative)
    data_relative = pd.DataFrame(data, columns=column_relative)
    data_where = data_relative[data_relative['A2'] == CONFIG.A2_ANSWER[0]]
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
    column_relative = list(CONFIG.BASE_COLUMN)
    column_relative.append(subject)
    data_relative = pd.DataFrame(data, columns=column_relative)
    data_where = data_relative[data_relative['A2'] == CONFIG.A2_ANSWER[0]]

    college_major_subject = list(CONFIG.BASE_COLUMN[0:2])
    college_major_subject.append(subject)
    # step1:各学院subject答题总人数
    answer_count = answerUtil.answer_grp_count(data_where, college_major_subject, list(CONFIG.BASE_COLUMN[0:2]))
    answer_count.columns = ['college', 'major', 'count']
    print("各学院各专业{}回答总人数：\n".format(subject))
    print(answer_count)

    # step2:各学院subject答题分布
    college_major_subject_other = list(CONFIG.BASE_COLUMN)
    college_major_subject_other.append(subject)
    answer_values_grp = answerUtil.answer_grp_count(data_where, college_major_subject_other,
                                                    college_major_subject)
    print("{}各答案分布：".format(subject))
    print(answer_values_grp)

    # step4:各学院subject答题占比
    pd_answers = pd.merge(answer_values_grp, answer_count, how='inner',
                          left_on=list(CONFIG.BASE_COLUMN[0:2]), right_on=['college', 'major'], validate='many_to_one')
    pd_answers['rate'] = (pd_answers['A2'] / pd_answers['count'] * 100).round(decimals=2)

    pd_five_rate = pd.DataFrame(pd_answers, columns=[CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1], subject, 'rate'])
    print("各学院各专业{}五维占比：\n".format(subject))
    print(pd_five_rate)
