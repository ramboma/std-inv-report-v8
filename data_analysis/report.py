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
import data_analysis.template as template


def employee_indurstry(data, filePath):
    '''就业行业分布'''
    data_a2 = data[data['A2'] == CONFIG.A2_ANSWER[0]]

    subject = 'B5-B'
    template.tdl_value_rate(data_a2, subject, filePath)
    template.tdl_college_combine(data_a2, subject, filePath)
    template.tdl_major_combine(data_a2, subject, filePath)

    pd_single_grp_mean = formulas.single_grp_mean(data_a2, 'B6', subject)
    excelUtil.writeExcel(pd_single_grp_mean, filePath, '主要就业行业月均收入')

    df_t = five_rate_single_t(data_a2, 'B9-1', CONFIG.ANSWER_TYPE_RELATIVE, subject)
    excelUtil.writeExcel(df_t, filePath, '各就业行业专业相关度差异分析')

    df_t = five_rate_single_t(data_a2, 'B7-1', CONFIG.ANSWER_TYPE_SATISFY, subject)
    excelUtil.writeExcel(df_t, filePath, '各就业行业就业满意度差异分析')

    return


def employee_job(data, filePath):
    '''就业职业分布'''

    data_a2 = data[data['A2'] == CONFIG.A2_ANSWER[0]]
    subject = 'B4-B'

    template.tdl_value_rate(data_a2, subject, filePath)
    template.tdl_college_combine(data_a2, subject, filePath)
    template.tdl_major_combine(data_a2, subject, filePath)

    pd_single_grp_mean = formulas.single_grp_mean(data_a2, 'B6', subject)
    excelUtil.writeExcel(pd_single_grp_mean, filePath, '主要就业职业月均收入')

    df_t = five_rate_single_t(data_a2, 'B9-1', CONFIG.ANSWER_TYPE_RELATIVE, subject)
    excelUtil.writeExcel(df_t, filePath, '各就业职业专业相关度差异分析')

    df_t = five_rate_single_t(data_a2, 'B7-1', CONFIG.ANSWER_TYPE_SATISFY, subject)
    excelUtil.writeExcel(df_t, filePath, '各就业职业就业满意度差异分析')

    return


def employee_industry_type(data, filePath):
    '''就业单位类型分布'''
    subject = 'B1'
    template.tdl_value_rate(data, subject, filePath)
    template.tdl_college_combine(data, subject, filePath)
    template.tdl_major_combine(data, subject, filePath)

    pd_single_grp_mean = formulas.single_grp_mean(data, 'B6', subject)
    excelUtil.writeExcel(pd_single_grp_mean, filePath, '主要就业单位月均收入差异')

    df_t = five_rate_single_t(data, 'B9-1', CONFIG.ANSWER_TYPE_RELATIVE, subject)
    excelUtil.writeExcel(df_t, filePath, '主要就业单位专业相关度差异分析')

    df_t = five_rate_single_t(data, 'B7-1', CONFIG.ANSWER_TYPE_SATISFY, subject)
    excelUtil.writeExcel(df_t, filePath, '主要就业单位满意度差异分析')
    return


def employee_industry_size(data, filePath):
    '''就业单位规模'''
    subject = 'B2'
    measure_name = '就业单位规模分布'
    df_value_count = formulas.answer_rate(data, subject)
    df_t = formulas.rate_T(df_value_count)
    excelUtil.writeExcel(df_t, filePath, CONFIG.TOTAL_COLUMN + measure_name)

    college_value = formulas.answer_college_value_rate(data, subject)
    df_t = formulas.college_rate_pivot(college_value)
    excelUtil.writeExcel(df_t, filePath, CONFIG.GROUP_COLUMN[0] + measure_name)

    major_value = formulas.answer_major_value_rate(data, subject)
    df_t = formulas.major_rate_pivot(major_value)
    excelUtil.writeExcel(df_t, filePath, CONFIG.GROUP_COLUMN[1] + measure_name)

    return


def employee_region_report(data, filePath):
    '''就业地区分布'''
    df_value_count = formulas.answer_rate(data, 'B3-A')
    excelUtil.writeExcel(df_value_count, filePath, '总体就业省')

    # 构造福建省条件 {column:B3-A,cond:福建省,oper:eq}
    cond={CONFIG.DICT_KEY[0]:'B3-A',CONFIG.DICT_KEY[1]:CONFIG.PROVINCE,
          CONFIG.DICT_KEY[2]:CONFIG.OPER[0]}
    college_value = formulas.answer_rate_condition(data,'B3-B',cond,[CONFIG.RATE_COLUMN[2]],[0])
    excelUtil.writeExcel(college_value, filePath, '省内就业城市')

    #各学院就业地区分布
    template.tdl_college_combine(data, 'B3-A', filePath)

    #各学院省内就业地区分布
    df_province = data[data['B3-A'] == CONFIG.PROVINCE]
    template.tdl_college_combine(df_province, 'B3-B', filePath)

    pd_birth = data[data['A1-A'] == CONFIG.PROVINCE]
    # 生源地答题总人数
    birth_count = answerUtil.answer_count(pd_birth, 'B3-A')
    # 生源地在本地就业人数
    birth_value_count = answerUtil.answer_of_subject_count(pd_birth, 'B3-A', CONFIG.PROVINCE)
    # 生源地当地比
    birth_value_rate = (birth_value_count / birth_count).round(CONFIG.DECIMALS6)
    pd_birth_rate = pd.DataFrame({'省内就业': [birth_value_rate],
                                  '省外就业': [100 - birth_value_rate],
                                  CONFIG.RATE_COLUMN[2]: birth_count})

    excelUtil.writeExcel(pd_birth_rate, filePath, '省内生源就业地区流向')

    pd_not_birth = data[data['A1-A'] != CONFIG.PROVINCE]
    # 外地生源答题总人数
    not_birth_count = answerUtil.answer_count(pd_not_birth, 'B3-A')
    # 外地生源本地就业人数 省内就业
    not_birth_local_count = answerUtil.answer_of_subject_count(pd_not_birth, 'B3-A', CONFIG.PROVINCE)
    not_birth_local_rate = (not_birth_local_count / not_birth_count * 100).round(2)

    # 外地生源回生源地就业人数 回生源所在地就业
    not_birth_birth_count = pd_not_birth[pd_not_birth['A1-A'] == pd_not_birth['B3-A']]['B3-A'].count()
    not_birth_birth_rate = (not_birth_birth_count / not_birth_count * 100).round(2)

    pd_not_birth_rate = pd.DataFrame({'回生源所在地就业': [not_birth_birth_rate],
                                      '其他省份就业': [100 - not_birth_local_rate - not_birth_birth_rate],
                                      '省内就业': [not_birth_local_rate],
                                      CONFIG.RATE_COLUMN[2]: not_birth_count})

    excelUtil.writeExcel(pd_not_birth_rate, filePath, '省外生源就业地区流向')

    pd_single_grp_mean = formulas.single_grp_mean(data, 'B6', 'B3-A')
    excelUtil.writeExcel(pd_single_grp_mean, filePath, '主要就业地区月均收入')

    pd_single_grp_city_mean = formulas.single_grp_mean(df_province, 'B6', 'B3-B')
    excelUtil.writeExcel(pd_single_grp_city_mean, filePath, '省内主要就业城市月均收入')

    return


def study_abroad_report(data, filePath):
    '''出国境留学'''
    count = answerUtil.answer_count(data, 'A2')
    study_value = formulas.answer_rate(data, 'F1')
    study_value.loc[:, CONFIG.RATE_COLUMN[2]] = count
    study_value.loc[:, CONFIG.RATE_COLUMN[-1]] = (
            study_value.loc[:, CONFIG.RATE_COLUMN[1]] / study_value.loc[:, CONFIG.RATE_COLUMN[2]] * 100).round(
        decimals=2)
    data_t = formulas.rate_T(study_value)
    excelUtil.writeExcel(data_t, filePath, '留学比列')

    study_satisfy = five_rate_t(data, 'F2', CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(study_satisfy, filePath, '留学录取结果满意度')

    study_relative = five_rate_t(data, 'F3', CONFIG.ANSWER_TYPE_RELATIVE)
    excelUtil.writeExcel(study_relative, filePath, '留学专业一致性')

    change_study_reason = formulas.answer_rate(data, 'F4')
    excelUtil.writeExcel(change_study_reason, filePath, '跨专业升学原因')


def further_report(data, filePath):
    # 总体情况
    further_rate = formulas.answer_rate(data, 'A2')
    # 只统计求学比例
    further_rate = further_rate[further_rate[CONFIG.RATE_COLUMN[0]] == CONFIG.A2_ANSWER[3]]
    excelUtil.writeExcel(further_rate, filePath, '总体国内升学比例')

    further_reason = formulas.answer_rate(data, 'E2')
    excelUtil.writeExcel(further_reason, filePath, '升学原因')

    further_satisfy = five_rate_t(data, 'E1', CONFIG.ANSWER_TYPE_SATISFY)
    excelUtil.writeExcel(further_satisfy, filePath, '升学录取结果满意度')

    further_relative = five_rate_t(data, 'E3', CONFIG.ANSWER_TYPE_RELATIVE)
    excelUtil.writeExcel(further_relative, filePath, '升学专业相关度')

    change_reason = formulas.answer_rate(data, 'E4')
    excelUtil.writeExcel(change_reason, filePath, '跨专业升学原因')


def work_stability_report(data, filePath):
    subject='B10-1'
    # 追加离职率计算
    report_value_rate(data,subject,'离职情况分布',filePath,CONFIG.DIMISSION,CONFIG.DIMISSION_COLUMNS)

    change_reason = formulas.answer_rate(data, 'B10-2')
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
    df_concat = pd.concat([df_rate, df_rate], sort=False)
    df_concat.insert(0, CONFIG.TOTAL_COLUMN, CONFIG.TOTAL_COLUMN)
    excelUtil.writeExcel(df_concat, filePath, '总体就业率')
    # 各学院就业率
    df_college_value = formulas.formulas_college_employe_rate(df_metrics)
    df_concat = pd.concat([df_college_value, df_rate], sort=False)
    df_concat.iloc[-1, 0] = CONFIG.TOTAL_COLUMN
    excelUtil.writeExcel(df_concat, filePath, '各学院就业率')
    # 各专业就业率
    df_major_value = formulas.formulas_major_employe_rate(df_metrics)
    df_concat = pd.concat([df_major_value, df_rate], sort=False)
    df_concat.iloc[-1, 0:1] = CONFIG.TOTAL_COLUMN
    excelUtil.writeExcel(df_concat, filePath, '各专业就业率')

    # 总体就业去向 追加灵活就业率
    report_value_rate(data,subject,'毕业去向',filePath,CONFIG.EMP_FREE,CONFIG.EMP_FREE_COLUMNS)
    return


def work_option_report(data, filePath):
    '''
    就业率及就业状态
    :param data:
    :param filePath:
    :return:
    '''
    subject = 'A3'
    title = '就业机会'

    report_value_rate(data, subject, title, filePath, measure_type=CONFIG.ANSWER_TYPE_NUM)


def non_employee_report(data, filePath):
    '''未就业报告'''
    # 一直未就业分布
    subject='C1'
    template.tdl_value_rate(data,subject,filePath)

    # 未就业毕业生目前去向分布
    subject = 'C2'
    template.tdl_value_rate(data, subject, filePath)
    return

def income_report(data, filePath):
    # mean
    subject = 'B6'
    pd_mean = formulas.answer_mean(data, subject)
    excelUtil.writeExcel(pd_mean, filePath, '总体月均收入')

    pd_college_mean = formulas.single_grp_mean(data, subject, CONFIG.BASE_COLUMN[0], True)
    excelUtil.writeExcel(pd_college_mean, filePath, '各学院月均收入')

    pd_major_mean = formulas.major_mean(data, subject)
    excelUtil.writeExcel(pd_major_mean, filePath, '各专业月均收入')

    # 500
    start = 2000
    period_n = 4
    step = 500
    pd_500 = formulas.answer_period(data, subject, start, start + period_n * step, step)
    data_t = formulas.rate_T(pd_500, [CONFIG.MEAN_COLUMN[-1]])
    excelUtil.writeExcel(data_t, filePath, '毕业生月均收入及薪酬分布_' + str(step))

    step = 1000
    pd_1000 = formulas.answer_period(data, subject, start, start + period_n * step, step)
    data_t = formulas.rate_T(pd_1000)
    excelUtil.writeExcel(data_t, filePath, '毕业生月均收入及薪酬分布_' + str(step))

    step = 2000
    pd_2000 = formulas.answer_period(data, subject, start, start + period_n * step, step)
    data_t = formulas.rate_T(pd_2000)
    excelUtil.writeExcel(data_t, filePath, '毕业生月均收入及薪酬分布_' + str(step))

    step = 1500
    pd_1500 = formulas.answer_period(data, subject, start, start + period_n * step, step)
    data_t = formulas.rate_T(pd_1500)
    excelUtil.writeExcel(data_t, filePath, '毕业生月均收入及薪酬分布_' + str(step))
    return


def school_satisfy_report(data, filePath):
    '''母校满意度报告'''
    subject = 'H7'
    sheet_name = '母校满意度'
    report_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY, sheet_name, filePath)

    return


def school_recommed_report(data, filePath):
    '''母校推荐报告'''
    subject = 'H8'
    sheet_name = '母校推荐度'

    # 排序列 '愿意', '不确定', '不愿意'
    order_column = CONFIG.ANSWER_RECOMMED.copy()
    order_column.append(CONFIG.RATE_COLUMN[2])

    df_value_rate = formulas.answer_rate(data, subject)
    df_value_rate.sort_values('比例', ascending=0, inplace=True)
    df_t = formulas.rate_T(df_value_rate)
    df_t = df_t[order_column]
    df_combine = pd.concat([df_t, df_t])
    df_combine.insert(0, '总体', '总体')
    excelUtil.writeExcel(df_combine, filePath, '总体' + sheet_name)

    df_college_rate = formulas.answer_college_value_rate(data, subject)
    df_college_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    df_college_t = formulas.college_rate_pivot(df_college_rate)
    order_column.insert(0, CONFIG.GROUP_COLUMN[0])
    df_college_t = df_college_t[order_column]
    df_combine = pd.concat([df_college_t, df_t], sort=False)
    df_combine.iloc[-1, 0] = CONFIG.TOTAL_COLUMN
    excelUtil.writeExcel(df_combine, filePath, '各学院' + sheet_name)

    df_major_rate = formulas.answer_major_value_rate(data, subject)
    df_major_rate.sort_values(['答题总人数', '比例'], ascending=[0, 0], inplace=True)
    df_major_t = formulas.major_rate_pivot(df_major_rate)
    order_column.insert(1, CONFIG.GROUP_COLUMN[1])
    df_major_t = df_major_t[order_column]
    df_combine = pd.concat([df_major_t, df_t], sort=False)
    df_combine.iloc[-1, 0:2] = CONFIG.TOTAL_COLUMN
    excelUtil.writeExcel(df_combine, filePath, '各专业' + sheet_name)

    return


def employee_difficult_report(data, filePath):
    '''求职过程报告'''
    data_a2 = data[data['A2'].isin([CONFIG.A2_ANSWER[0], CONFIG.A2_ANSWER[2]])]
    subject='D2'
    template.tdl_value_rate(data_a2, subject, filePath)
    template.tdl_major_combine(data_a2, subject, filePath)

    subject='D1'
    template.tdl_value_rate(data_a2, subject, filePath)
    return


def self_employed_report(data, filePath):
    '''自主创业报告'''
    business_rate = formulas.answer_rate(data, 'A2')
    # 只统计自主创业的
    business_rate = business_rate[business_rate[CONFIG.RATE_COLUMN[0]] == CONFIG.A2_ANSWER[1]]
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
    df_distribution = formulas.answer_rate(data, subject)
    df_distribution.sort_values([CONFIG.RATE_COLUMN[-1]], ascending=[0], inplace=True)
    excelUtil.writeExcel(df_distribution, filePath, '创业行业')

    subject = 'G2'
    df_mean = five_rate_t(data, subject, CONFIG.ANSWER_TYPE_RELATIVE)
    excelUtil.writeExcel(df_mean, filePath, '创业行业与所学专业相关度')

    return


def basic_quality_report(data, file):
    '''基础素质报告'''
    subject = 'I2-1'
    df_distribution = answerUtil.multi_answer_distribution(data, subject)
    df_distribution.sort_values([CONFIG.RATE_COLUMN[-1]], ascending=[0], inplace=True)
    excelUtil.writeExcel(df_distribution, file, '重要度')

    subject = 'I2-2'
    df_ability = answerUtil.ability_distribution(data, subject)
    df_ability.sort_values(CONFIG.RATE_COLUMN[1], ascending=0, inplace=True)
    excelUtil.writeExcel(df_ability, file, '满足度')


def major_quality_report(data, file):
    '''专业素质报告'''
    subject = 'I1-1'
    title = '专业素质重要性'
    # I1-1-A I1-1-B
    array_subject = [subject + '-' + chr(i) for i in range(65, 67)]
    df_five = report_combine_value_five_rate(data, array_subject,
                                             CONFIG.ANSWER_TYPE_IMPORTANT, title, CONFIG.MAJOR_QUALITY_SUBJECT)
    excelUtil.writeExcel(df_five, file, title)

    subject = 'I1-2'
    title = '专业素质满意度'
    # I1-2-A I1-2-B
    array_subject = [subject + '-' + chr(i) for i in range(65, 67)]
    df_five = report_combine_value_five_rate(data, array_subject,
                                             CONFIG.ANSWER_TYPE_PLEASED, title, CONFIG.MAJOR_QUALITY_SUBJECT)

    excelUtil.writeExcel(df_five, file, title)

    return


def evelution_lesson_report(data, file):
    '''课堂教学报告'''
    focus = ['H2-' + chr(i) for i in range(65, 70)]
    measure_name = '课堂教学各方面评价'
    df_summary = report_combine_value_five_rate(data, focus, CONFIG.ANSWER_TYPE_MEET_V,
                                                measure_name, CONFIG.DICT_SUBJECT)
    excelUtil.writeExcel(df_summary, file, measure_name)

    df_college = report_combine_level(data, focus, CONFIG.ANSWER_TYPE_MEET_V,
                                      CONFIG.DICT_SUBJECT, 1)
    excelUtil.writeExcelWithIndex(df_college, file, CONFIG.GROUP_COLUMN[0] + measure_name)

    df_major = report_combine_level(data, focus, CONFIG.ANSWER_TYPE_MEET_V,
                                    CONFIG.DICT_SUBJECT, 2)
    excelUtil.writeExcelWithIndex(df_major, file, CONFIG.GROUP_COLUMN[1] + measure_name)

    return


def evelution_practice_report(data, file):
    '''实践教学报告'''
    focus = ['H3-' + chr(i) for i in range(65, 69)]
    measure_name = '实践教学各方面评价'
    df_summary = report_combine_value_five_rate(data, focus, CONFIG.ANSWER_TYPE_HELP,
                                                measure_name, CONFIG.DICT_SUBJECT)
    excelUtil.writeExcel(df_summary, file, measure_name)

    df_college = report_combine_level(data, focus, CONFIG.ANSWER_TYPE_HELP,
                                      CONFIG.DICT_SUBJECT, 1)
    excelUtil.writeExcelWithIndex(df_college, file, CONFIG.GROUP_COLUMN[0] + measure_name)

    df_major = report_combine_level(data, focus, CONFIG.ANSWER_TYPE_HELP,
                                    CONFIG.DICT_SUBJECT, 2)
    excelUtil.writeExcelWithIndex(df_major, file, CONFIG.GROUP_COLUMN[1] + measure_name)

    return


def evelution_teach_report(data, file):
    '''任课教师评价'''
    # H4A-E

    focus = ['H4-' + chr(i) for i in range(65, 70)]
    measure_name = '对任课教师的评价'
    df_summary = report_combine_value_five_rate(data, focus, CONFIG.ANSWER_TYPE_SATISFY,
                                                measure_name, CONFIG.DICT_SUBJECT)
    excelUtil.writeExcel(df_summary, file, measure_name)

    df_college = report_combine_level(data, focus, CONFIG.ANSWER_TYPE_SATISFY,
                                      CONFIG.DICT_SUBJECT, 1)
    excelUtil.writeExcelWithIndex(df_college, file, CONFIG.GROUP_COLUMN[0] + measure_name)

    df_major = report_combine_level(data, focus, CONFIG.ANSWER_TYPE_SATISFY,
                                    CONFIG.DICT_SUBJECT, 2)
    excelUtil.writeExcelWithIndex(df_major, file, CONFIG.GROUP_COLUMN[1] + measure_name)

    return


def evelution_H4_E_report(data, file):
    '''母校任课教师总体报告'''
    subject = 'H4-E'
    sheet_name = '对任课教师的满意情况'
    report_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY, sheet_name, file)

    return


def evelution_academic_report(data, file):
    '''母校的'''
    subject = 'J5-5'
    sheet_name = '母校的学风认可度评价'
    report_five_rate(data, subject, CONFIG.ANSWER_TYPE_FEEL, sheet_name, file)

    return


def evelution_H4_T_report(data, file):
    '''教育教学报告'''
    subject = 'H4-T'
    sheet_name = '教育教学总体评价'
    report_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY, sheet_name, file)

    return


def evelution_H4_S_report(data, file):
    '''实践教学报告'''
    subject = 'H4-S'
    sheet_name = '实践教学总体评价'
    report_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY, sheet_name, file)

    return


def evelution_H4_R_report(data, file):
    '''社团活动报告'''
    subject = 'H4-R'
    sheet_name = '社团活动总体评价'
    report_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY, sheet_name, file)

    return


def evelution_H4_P_report(data, file):
    '''母校学生管理报告'''
    subject = 'H4-P'
    sheet_name = '管理工作满意度'
    report_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY, sheet_name, file)

    subject = 'H5'
    df_distribution = answerUtil.multi_answer_distribution(data, subject)
    df_distribution.sort_values([CONFIG.RATE_COLUMN[-1]], ascending=[0], inplace=True)

    excelUtil.writeExcel(df_distribution, file, '学生管理工作改进')

    return


def evelution_H4_Q_report(data, file):
    '''母校生活服务报告'''
    subject = 'H4-Q'
    sheet_name = '生活服务满意度'
    report_five_rate(data, subject, CONFIG.ANSWER_TYPE_SATISFY, sheet_name, file)

    subject = 'H6'
    df_distribution = answerUtil.multi_answer_distribution(data, subject)
    df_distribution.sort_values([CONFIG.RATE_COLUMN[-1]], ascending=[0], inplace=True)
    excelUtil.writeExcel(df_distribution, file, '生活服务需要提高的方面')

    return


def evelution_H4_F_K_report(data, file):
    # H4-F~H4-K
    focus = ['H4-' + chr(i) for i in range(70, 76)]
    df_summary = report_combine_value_five_rate(data, focus, CONFIG.ANSWER_TYPE_SATISFY,
                                                '对母校就业教育的满意度评价', CONFIG.DICT_SUBJECT)
    excelUtil.writeExcel(df_summary, file, '对母校就业教育的满意度评价')

    df_college = report_combine_level(data, focus, CONFIG.ANSWER_TYPE_SATISFY,
                                      CONFIG.DICT_SUBJECT, 1)
    excelUtil.writeExcelWithIndex(df_college, file, '各学院对母校就业教育的满意度评价')

    df_major = report_combine_level(data, focus, CONFIG.ANSWER_TYPE_SATISFY,
                                    CONFIG.DICT_SUBJECT, 2)
    excelUtil.writeExcelWithIndex(df_major, file, '各专业对母校就业教育的满意度评价')
    return


def evelution_H4_L_O_report(data, file):
    # H4-L~H4-O
    focus = ['H4-' + chr(i) for i in range(76, 80)]
    df_summary = report_combine_value_five_rate(data, focus, CONFIG.ANSWER_TYPE_SATISFY,
                                                '对母校创业教育的满意度评价', CONFIG.DICT_SUBJECT)
    excelUtil.writeExcel(df_summary, file, '对母校创业教育的满意度评价')

    df_college = report_combine_level(data, focus, CONFIG.ANSWER_TYPE_SATISFY,
                                      CONFIG.DICT_SUBJECT, 1)
    excelUtil.writeExcelWithIndex(df_college, file, '各学院对母校创业教育的满意度评价')

    df_major = report_combine_level(data, focus, CONFIG.ANSWER_TYPE_SATISFY,
                                    CONFIG.DICT_SUBJECT, 2)
    excelUtil.writeExcelWithIndex(df_major, file, '各专业对母校创业教育的满意度评价')

    # H3-E~H3-F
    focus = ['H3-' + chr(i) for i in range(69, 71)]

    df_summary = report_combine_value_five_rate(data, focus, CONFIG.ANSWER_TYPE_HELP,
                                                '对母校创业教育的帮助度评价', CONFIG.DICT_SUBJECT)
    excelUtil.writeExcel(df_summary, file, '对母校创业教育的帮助度评价')

    df_college = report_combine_level(data, focus, CONFIG.ANSWER_TYPE_HELP,
                                      CONFIG.DICT_SUBJECT, 1)
    excelUtil.writeExcelWithIndex(df_college, file, '各学院对母校创业教育的帮助度评价')

    df_major = report_combine_level(data, focus, CONFIG.ANSWER_TYPE_HELP,
                                    CONFIG.DICT_SUBJECT, 2)
    excelUtil.writeExcelWithIndex(df_major, file, '各专业对母校创业教育的帮助度评价')
    return


def report_combine_value_five_rate(data, array_subject, metric_type, metric_name, dict_subject):
    '''组合题的五维占比 总体'''
    if data.empty:
        return data
    if not array_subject:
        return data

    focus_column = rebuild_five_columns(metric_type, 0)
    focus_column.insert(0, metric_name)

    df_init = pd.DataFrame(columns=focus_column)  # 创建一个空的dataframe

    for subject in array_subject:
        df_t = five_rate_t(data, subject, metric_type)
        df_t.loc[:, metric_name] = subject
        df_init = pd.concat([df_init, df_t], sort=False)
    df_init.loc[:, metric_name] = df_init.loc[:, metric_name].map(dict_subject)
    return df_init


def report_combine_level(data, array_subject, metric_type, dict_subject, grp_level):
    '''组合题 三维 拼接'''
    if data.empty:
        return data
    if not array_subject:
        return data

    five_column = rebuild_five_columns(metric_type, 1)
    focus_column = five_column[-3:]
    if grp_level == 1:
        grp_cols = CONFIG.GROUP_COLUMN[0]
    elif grp_level == 2:
        grp_cols = [CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1]]
    else:
        return data

    df_init = pd.DataFrame()  # 创建一个空的dataframe
    for subject in array_subject:
        subject_name = dict_subject.get(subject)
        if grp_level == 1:
            df_t = five_rate_single_t_sub(data, subject, metric_type)
        elif grp_level == 2:
            df_t = five_rate_major_t_sub(data, subject, metric_type)

        df_t.set_index(grp_cols, inplace=True)
        dict_cols = {cs: subject_name + '_' + cs for cs in focus_column}
        df_t.rename(columns=dict_cols, inplace=True)
        df_init = pd.concat([df_init, df_t], sort=False, axis=1)

    df_init.columns = pd.MultiIndex.from_tuples([tuple(c.split('_')) for c in df_init.columns])
    df_init.sort_values(by=(subject_name, CONFIG.MEAN_COLUMN[2]), ascending=False, inplace=True)
    return df_init


####################   就业竞争力
def major_relative_report(data, filePath):
    '''专业相关度'''
    subject = 'B9-1'
    measure_name = formulas.parse_measure_name(CONFIG.ANSWER_TYPE_RELATIVE)
    report_five_rate(data, subject, CONFIG.ANSWER_TYPE_RELATIVE, '专业相关情况', filePath)

    subject = 'B9-2'
    template.tdl_value_rate(data,subject,filePath)


def job_meet_report(data, filePath):
    '''职业期待吻合度'''
    subject = 'B8'
    measure_name = formulas.parse_measure_name(CONFIG.ANSWER_TYPE_MEET)
    report_five_rate(data, subject, CONFIG.ANSWER_TYPE_MEET, '职业期待吻合情况', filePath)
    return


def job_satisfy_report(data, filePath):
    '''职业满意度'''
    subject = 'B7'
    measure_type = CONFIG.ANSWER_TYPE_SATISFY
    measure_name = formulas.parse_measure_name(measure_type)
    array_subjects = [subject + '-' + str(sub) for sub in range(1, 5)]

    # 单独产生总体职业满意度、包含学院、专业
    report_five_rate(data, array_subjects[0], measure_type, CONFIG.JOB_SATISFY_SUBJECT[array_subjects[0]], filePath)

    # 行拼接所以选项的满意度，报表格式不同
    df_init = pd.DataFrame()
    for sub in array_subjects:
        sheetName = CONFIG.JOB_SATISFY_SUBJECT[sub]
        df_five = formulas.answer_five_rate(data, sub, measure_type)
        # 关注后三项
        df_three = df_five.loc[:, [measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]]]
        df_three.insert(0, '毕业生对工作各方面的满意情况', sheetName)
        df_three.drop_duplicates(inplace=True)
        df_init = pd.concat([df_init, df_three], sort=False)

    excelUtil.writeExcel(df_init, filePath, '毕业生对工作各方面的满意情况')
    df_college = report_combine_level(data, array_subjects, measure_type, CONFIG.JOB_SATISFY_SUBJECT, 1)
    excelUtil.writeExcelWithIndex(df_college, filePath, '各学院对工作各方面的满意情况')
    df_major = report_combine_level(data, array_subjects, measure_type, CONFIG.JOB_SATISFY_SUBJECT, 2)
    excelUtil.writeExcelWithIndex(df_major, filePath, '各专业对工作各方面的满意情况')


# ====特殊人群

def special_common_report(data, subject, filePath, suffix, dict_where, title):
    # 条件过滤
    col_cond = dict_where[CONFIG.DICT_KEY[0]]
    val = dict_where[CONFIG.DICT_KEY[1]]
    df_data = data[data[col_cond] == val]
    df_data1 = data[data[col_cond] != val]
    if CONFIG.OPER_NOT + val in CONFIG.DICT_REP.keys():
        val1 = CONFIG.DICT_REP[CONFIG.OPER_NOT + val]
    else:
        val1 = CONFIG.OPER_NOT + val

    df_emp_feature1 = special_employee_featured(df_data)
    df_emp_feature1.insert(0, title, val)
    df_emp_feature2 = special_employee_featured(df_data1)
    df_emp_feature2.insert(0, title, val1)
    df_emp_feature = special_employee_featured(data)
    df_emp_feature.insert(0, title, CONFIG.TOTAL_COLUMN)

    df_concat = pd.concat([df_emp_feature1, df_emp_feature2, df_emp_feature])
    excelUtil.writeExcel(df_concat, filePath, suffix + '就业特色')

    df_emp_competitive1 = special_employee_competitive(df_data)
    df_emp_competitive1.insert(0, title, val)
    df_emp_competitive2 = special_employee_competitive(df_data1)
    df_emp_competitive2.insert(0, title, val1)
    df_emp_competitive = special_employee_competitive(data)
    df_emp_competitive.insert(0, title, CONFIG.TOTAL_COLUMN)
    df_concat = pd.concat([df_emp_competitive1, df_emp_competitive2, df_emp_competitive], sort=False)
    excelUtil.writeExcel(df_concat, filePath, suffix + '就业竞争力')
    df_lesson1 = special_lesson(df_data)
    df_lesson1.insert(0, title, val)

    df_lesson2 = special_lesson(df_data1)
    df_lesson2.insert(0, title, val1)

    df_lesson = special_lesson(data)
    df_lesson.insert(0, title, CONFIG.TOTAL_COLUMN)
    df_concat = pd.concat([df_lesson1, df_lesson2, df_lesson])
    excelUtil.writeExcel(df_concat, filePath, suffix + '就业课堂教学')

    df_practice1 = special_practice(df_data)
    df_practice1.insert(0, title, val)

    df_practice2 = special_practice(df_data1)
    df_practice2.insert(0, title, val1)

    df_practice = special_practice(data)
    df_practice.insert(0, title, CONFIG.TOTAL_COLUMN)
    df_concat = pd.concat([df_practice1, df_practice2, df_practice])
    excelUtil.writeExcel(df_concat, filePath, suffix + '实践教学')

    df_teacher1 = special_teacher(df_data)
    df_teacher1.insert(0, title, val)

    df_teacher2 = special_teacher(df_data1)
    df_teacher2.insert(0, title, val1)

    df_teacher = special_teacher(data)
    df_teacher.insert(0, title, CONFIG.TOTAL_COLUMN)
    df_concat = pd.concat([df_teacher1, df_teacher2, df_teacher])
    excelUtil.writeExcel(df_concat, filePath, suffix + '教师评价')

    df_school1 = special_school(df_data)
    df_school1.insert(0, title, val)
    df_school2 = special_school(df_data1)
    df_school2.insert(0, title, val1)
    df_school = special_school(data)
    df_school.insert(0, title, CONFIG.TOTAL_COLUMN)
    df_concat = pd.concat([df_school1, df_school2, df_school])
    excelUtil.writeExcel(df_concat, filePath, suffix + '母校总和评价')

    return


def special_employee_featured(data):
    '''特殊人群就业特色分析'''
    # 行业
    array_demensions = ['B5-B', 'B1', 'B3-A', 'B4-B']
    df_init = pd.DataFrame()

    for demension in array_demensions:
        df_indurstry = formulas.answer_rate_condition(data, demension, {}, [CONFIG.RATE_COLUMN[-1]], [0], 5)
        demension_name = CONFIG.DICT_SUBJECT[demension]
        df_combine = formulas.row_combine(df_indurstry, combin_name=demension_name)
        df_init = pd.concat([df_init, df_combine], axis=1, sort=False)
    return df_init


def special_employee_competitive(data, dict_where={}):
    '''特殊人群就业竞争力分析'''

    # 就业率
    df_income = formulas.formulas_employe_rate(data)
    df_income.rename(columns={CONFIG.RATE_COLUMN[2]: '就业率' + CONFIG.RATE_COLUMN[2]})

    # 薪酬
    df_salary = formulas.formula_income_mean(data, dict_where)
    df_salary.rename(columns={CONFIG.RATE_COLUMN[2]: '薪酬' + CONFIG.RATE_COLUMN[2]})

    # 专业相关度
    subject = 'B9-1'
    df_major_relative = five_rate_t(data, subject, CONFIG.ANSWER_TYPE_RELATIVE)
    df_major_relative = df_major_relative.loc[:, df_major_relative.columns[-3:]]
    df_major_relative.columns = [CONFIG.SPECIAL_SUBJECT[subject] + name for name in df_major_relative.columns]
    # 工作满意度
    subject = 'B7-1'
    df_job_satisfy = five_rate_t(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_job_satisfy = df_job_satisfy.loc[:, df_job_satisfy.columns[-3:]]
    df_job_satisfy.columns = [CONFIG.SPECIAL_SUBJECT[subject] + name for name in df_job_satisfy.columns]

    # 薪酬满意度
    subject = 'B7-2'
    df_salary_satisfy = five_rate_t(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_salary_satisfy = df_salary_satisfy.loc[:, df_salary_satisfy.columns[-3:]]
    df_salary_satisfy.columns = [CONFIG.SPECIAL_SUBJECT[subject] + name for name in df_salary_satisfy.columns]

    # 职业发展前景满意度
    subject = 'B7-3'
    df_industry_satisfy = five_rate_t(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_industry_satisfy = df_industry_satisfy.loc[:, df_industry_satisfy.columns[-3:]]
    df_industry_satisfy.columns = [CONFIG.SPECIAL_SUBJECT[subject] + name for name in df_industry_satisfy.columns]
    # 工作内容满意度
    subject = 'B7-4'
    df_job_content_satisfy = five_rate_t(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_job_content_satisfy = df_job_content_satisfy.loc[:, df_job_content_satisfy.columns[-3:]]
    df_job_content_satisfy.columns = [CONFIG.SPECIAL_SUBJECT[subject] + name for name in df_job_content_satisfy.columns]

    # 职业期待吻合度
    subject = 'B8'
    df_job_hope = five_rate_t(data, subject, CONFIG.ANSWER_TYPE_MEET)
    df_job_hope = df_job_hope.loc[:, df_job_hope.columns[-3:]]
    df_job_hope.columns = [CONFIG.SPECIAL_SUBJECT[subject] + name for name in df_job_hope.columns]

    # 离职率
    subject = 'B10-1'
    change_times = formulas.answer_rate(data, subject)
    no_changes = change_times[change_times[CONFIG.RATE_COLUMN[0]].isin([CONFIG.B10_1_ANSWER[0]])].loc[
        0, CONFIG.RATE_COLUMN[-1]]
    change_times.loc[:, '离职率'] = 100 - no_changes
    change_times = change_times.loc[:, ['离职率', CONFIG.RATE_COLUMN[2]]]
    change_times.drop_duplicates(inplace=True)

    df_concat = pd.concat([df_income, df_salary, df_major_relative, df_job_satisfy,
                           df_salary_satisfy, df_industry_satisfy,
                           df_job_content_satisfy, df_job_hope, change_times], axis=1)
    return df_concat


def special_lesson(data):
    '''特殊人课堂教学分析'''
    focus = ['H2-' + chr(i) for i in range(65, 70)]
    measure_name = '课堂教学各方面评价'
    df_summary = report_combine_value_five_rate(data, focus, CONFIG.ANSWER_TYPE_MEET_V,
                                                measure_name, CONFIG.DICT_SUBJECT)
    return df_summary


def special_practice(data, dict_where={}):
    '''特殊人群实践教学报告'''
    focus = ['H3-' + chr(i) for i in range(65, 69)]
    measure_name = '实践教学各方面评价'
    df_summary = report_combine_value_five_rate(data, focus, CONFIG.ANSWER_TYPE_HELP,
                                                measure_name, CONFIG.DICT_SUBJECT)
    return df_summary


def special_teacher(data):
    '''特殊人群教师评价'''
    # H4A-E

    focus = ['H4-' + chr(i) for i in range(65, 70)]
    measure_name = '对任课教师的评价'
    df_summary = report_combine_value_five_rate(data, focus, CONFIG.ANSWER_TYPE_SATISFY,
                                                measure_name, CONFIG.DICT_SUBJECT)
    return df_summary


def special_school(data):
    '''特殊人群学校总体评价'''
    # 学校满意度
    subject = 'H7'
    df_mean_satisfy = five_rate_t(data, subject, CONFIG.ANSWER_TYPE_SATISFY)
    df_mean_satisfy = df_mean_satisfy.loc[:, df_mean_satisfy.columns[-3:]]

    # 学校推荐度
    df_recommend = formulas.answer_rate(data, 'H8')
    df_recommend = df_recommend[df_recommend[CONFIG.RATE_COLUMN[0]] == CONFIG.ANSWER_RECOMMED[0]]
    df_recommend = df_recommend.loc[:, [CONFIG.RATE_COLUMN[-1], CONFIG.RATE_COLUMN[2]]]
    df_result = pd.concat([df_mean_satisfy, df_recommend], axis=1)
    return df_result


def special_gender_report(data, filePath):
    subject = '_3'
    suffix = '不同性别'
    # 性别
    title = CONFIG.SPECIAL_COLUMN[0]
    where = CONFIG.GENDER[0]

    dict_where = {CONFIG.DICT_KEY[0]: subject,
                  CONFIG.DICT_KEY[1]: where,
                  CONFIG.DICT_KEY[2]: CONFIG.OPER[0]}
    special_common_report(data, subject, filePath, suffix, dict_where, title)
    return


def special_national_report(data, filePath):
    '''特殊人群民族报告'''
    subject = '_16'
    suffix = '不同民族'
    # 民族
    title = CONFIG.SPECIAL_COLUMN[1]
    where = CONFIG.NATIONAL_COLUMN[0]

    dict_where = {CONFIG.DICT_KEY[0]: subject,
                  CONFIG.DICT_KEY[1]: where,
                  CONFIG.DICT_KEY[2]: CONFIG.OPER[0]}
    special_common_report(data, subject, filePath, suffix, dict_where, title)
    return


def special_origin_province_report(data, filePath):
    '''特殊人群生源地报告'''
    subject = 'A1-A'
    suffix = '省内省外生源'
    # 类别
    title = CONFIG.SPECIAL_COLUMN[2]
    where = CONFIG.PROVINCE

    dict_where = {CONFIG.DICT_KEY[0]: subject,
                  CONFIG.DICT_KEY[1]: where,
                  CONFIG.DICT_KEY[2]: CONFIG.OPER[0]}
    special_common_report(data, subject, filePath, suffix, dict_where, title)
    return


def special_education_report(data, filePath):
    '''特殊人群教育和非教育就业报告'''
    subject = 'B5-B'
    suffix = '教育和非教育'
    # 类别
    title = CONFIG.SPECIAL_COLUMN[2]
    where = CONFIG.EDUCATION_COLUMN[0]

    dict_where = {CONFIG.DICT_KEY[0]: subject,
                  CONFIG.DICT_KEY[1]: where,
                  CONFIG.DICT_KEY[2]: CONFIG.OPER[0]}
    special_common_report(data, subject, filePath, suffix, dict_where, title)
    return


def special_indurstry_province_report(data, filePath):
    '''特殊人群省内省外就业报告'''
    subject = 'B3-A'
    suffix = '省内省外就业'
    # 类别
    title = CONFIG.SPECIAL_COLUMN[2]
    where = CONFIG.PROVINCE

    dict_where = {CONFIG.DICT_KEY[0]: subject,
                  CONFIG.DICT_KEY[1]: where,
                  CONFIG.DICT_KEY[2]: CONFIG.OPER[0]}
    special_common_report(data, subject, filePath, suffix, dict_where, title)
    return


def special_admissions_report(data, filePath):
    '''特殊招生渠道就业报告'''
    subject = 'B4-B'
    suffix = '医药卫生'
    where = '医药卫生'

    dict_where = {CONFIG.DICT_KEY[0]: subject, CONFIG.DICT_KEY[1]: where, CONFIG.DICT_KEY[2]: CONFIG.OPER[0]}
    special_common_report(data, subject, filePath, suffix, dict_where, CONFIG.EDUCATION_COLUMN)
    return


def special_teacher_report(data, filePath):
    '''特殊人群师范和非师范就业报告'''
    subject = 'B5-B'
    suffix = '师范和非师范'
    # 类别
    title = CONFIG.SPECIAL_COLUMN[2]
    where = CONFIG.TEACHER_COLUMN[0]

    dict_where = {CONFIG.DICT_KEY[0]: subject, CONFIG.DICT_KEY[1]: where, CONFIG.DICT_KEY[2]: CONFIG.OPER[0]}
    special_common_report(data, subject, filePath, suffix, dict_where, title)
    return


def special_medical_report(data, filePath):
    '''特殊人群医疗卫生就业报告'''
    subject = 'B4-A'
    suffix = '医疗卫生'
    where = '医疗卫生'

    dict_where = {CONFIG.DICT_KEY[0]: subject, CONFIG.DICT_KEY[1]: where, CONFIG.DICT_KEY[2]: CONFIG.OPER[0]}
    special_common_report(data, subject, filePath, suffix, dict_where, CONFIG.MEDICAL_COLUMN)
    return


def special_social_health_report(data, filePath):
    '''特殊人群卫生和社会报告'''
    subject = 'B5-A'
    suffix = '卫生和社会工作'
    where = '卫生和社会工作'

    dict_where = {CONFIG.DICT_KEY[0]: subject, CONFIG.DICT_KEY[1]: where, CONFIG.DICT_KEY[2]: CONFIG.OPER[0]}
    special_common_report(data, subject, filePath, suffix, dict_where, CONFIG.HEALTH_COLUMN)
    return


def rebuild_five_columns(measure_type, level=0, minus=0):
    # 用于重排转置后的列的顺序
    five_metric = formulas.parse_measure(measure_type)
    five_metric = five_metric[0:-1]

    # 学院、专业、五纬排序、度量值、均值、答题总人数
    metric_name = formulas.parse_measure_name(measure_type)
    order_column = five_metric.copy()
    if level == 1:
        order_column.insert(0, CONFIG.GROUP_COLUMN[0])
    elif level == 2:
        order_column.insert(0, CONFIG.GROUP_COLUMN[0])
        order_column.insert(1, CONFIG.GROUP_COLUMN[1])
    elif level == 3:
        order_column.insert(0, CONFIG.GROUP_COLUMN[-1])
    # 默认不减少，即考虑度量、均值
    if not minus:
        order_column.append(metric_name)
        order_column.append(CONFIG.MEAN_COLUMN[-1])
    order_column.append(CONFIG.MEAN_COLUMN[2])
    return order_column


def five_rate_t(data, subject, measure_type):
    '''五维占比总体行专列'''
    if data.empty:
        return data
    if not subject or not measure_type:
        return data

    ls_metrics_cols = list(CONFIG.BASE_COLUMN)
    ls_metrics_cols.append(subject)
    df_metrics = data.loc[:, ls_metrics_cols]

    focus_name = formulas.parse_measure_name(measure_type)
    array_focus = [focus_name, CONFIG.MEAN_COLUMN[-1]]

    value_rate = formulas.answer_five_rate(df_metrics, subject, measure_type)
    rate_t = formulas.rate_T(value_rate, array_focus)
    rate_t = rate_t.loc[:, rebuild_five_columns(measure_type, 0)]
    return rate_t


def five_rate_single_t(data, subject, measure_type, grp_subject=CONFIG.BASE_COLUMN[0]):
    '''单条件五维占比'''
    if data.empty:
        return data
    if not subject or not measure_type:
        return data

    ls_metrics_cols = list(CONFIG.BASE_COLUMN)
    ls_metrics_cols.append(subject)
    level = 1
    # 分组不是学院时，则提取分组列
    if grp_subject != CONFIG.BASE_COLUMN[0]:
        ls_metrics_cols.append(grp_subject)
        level = 3

    df_metrics = data.loc[:, ls_metrics_cols]

    focus_name = formulas.parse_measure_name(measure_type)
    array_focus = [focus_name, CONFIG.MEAN_COLUMN[-1]]

    five_rate = formulas.answer_five_rate_single_grp(df_metrics, subject,
                                                     grp_subject,
                                                     measure_type)
    college_t = formulas.college_rate_pivot(five_rate, array_focus, grp_subject)
    college_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    college_t = college_t.loc[:, rebuild_five_columns(measure_type, level)]
    return college_t


def five_rate_major_t(data, subject, measure_type):
    if data.empty:
        return data
    if not subject or not measure_type:
        return data

    ls_metrics_cols = list(CONFIG.BASE_COLUMN)
    ls_metrics_cols.append(subject)
    df_metrics = data.loc[:, ls_metrics_cols]

    focus_name = formulas.parse_measure_name(measure_type)
    array_focus = [focus_name, CONFIG.MEAN_COLUMN[-1]]

    major_changes = formulas.answer_five_rate_major_grp(df_metrics, subject, measure_type)
    major_t = formulas.major_rate_pivot(major_changes,
                                        array_focus)
    major_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    major_t = major_t.loc[:, rebuild_five_columns(measure_type, 2)]
    return major_t


def five_rate_major_t_sub(data, subject, measure_type):
    if data.empty:
        return data
    if not subject or not measure_type:
        return data

    ls_metrics_cols = list(CONFIG.BASE_COLUMN)
    ls_metrics_cols.append(subject)
    df_metrics = data.loc[:, ls_metrics_cols]

    focus_name = formulas.parse_measure_name(measure_type)
    array_focus = [CONFIG.GROUP_COLUMN[0], CONFIG.GROUP_COLUMN[1],
                   focus_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]]

    major_changes = formulas.answer_five_rate_major_grp(df_metrics, subject, measure_type)
    five_rate = major_changes.loc[:, array_focus]
    five_rate = five_rate.drop_duplicates()
    return five_rate


def five_rate_single_t_sub(data, subject, measure_type):
    '''只关注 度量和均值、答题总人数'''
    if data.empty:
        return data
    if not subject or not measure_type:
        return data

    ls_metrics_cols = list(CONFIG.BASE_COLUMN)
    ls_metrics_cols.append(subject)
    df_metrics = data.loc[:, ls_metrics_cols]

    focus_name = formulas.parse_measure_name(measure_type)
    array_focus = [CONFIG.GROUP_COLUMN[0], focus_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]]

    five_rate = formulas.answer_five_rate_single_grp(df_metrics, subject,
                                                     CONFIG.BASE_COLUMN[0],
                                                     measure_type)
    five_rate = five_rate.loc[:, array_focus]
    five_rate = five_rate.drop_duplicates()
    return five_rate


def report_five_rate(data, subject, measure_type, measure_name, file_path):
    '''五维占比共用方法'''
    if data.empty:
        return data
    if not subject or not measure_type:
        return data

    ls_metrics_cols = list(CONFIG.BASE_COLUMN)
    ls_metrics_cols.append(subject)
    df_metrics = data.loc[:, ls_metrics_cols]

    focus_name = formulas.parse_measure_name(measure_type)
    array_focus = [focus_name, CONFIG.MEAN_COLUMN[-1]]

    value_rate = formulas.answer_five_rate(df_metrics, subject, measure_type)
    rate_t = formulas.rate_T(value_rate, array_focus)
    rate_t = rate_t.loc[:, rebuild_five_columns(measure_type, 0)]
    rate_combin = pd.concat([rate_t, rate_t])
    rate_combin.insert(0, CONFIG.TOTAL_COLUMN, CONFIG.TOTAL_COLUMN)
    excelUtil.writeExcel(rate_combin, file_path, CONFIG.TOTAL_COLUMN + measure_name)

    college_changes = formulas.answer_five_rate_single_grp(df_metrics, subject,
                                                           CONFIG.BASE_COLUMN[0], measure_type)
    college_t = formulas.college_rate_pivot(college_changes,
                                            array_focus)
    college_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    college_t = college_t.loc[:, rebuild_five_columns(measure_type, 1)]
    college_combine = pd.concat([college_t, rate_t], sort=False)
    college_combine.iloc[-1, 0] = CONFIG.TOTAL_COLUMN
    excelUtil.writeExcel(college_combine, file_path, CONFIG.GROUP_COLUMN[0] + measure_name)

    major_changes = formulas.answer_five_rate_major_grp(df_metrics, subject, measure_type)
    major_t = formulas.major_rate_pivot(major_changes,
                                        array_focus)
    major_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    major_t = major_t.loc[:, rebuild_five_columns(measure_type, 2)]
    major_conbine = pd.concat([major_t, rate_t], sort=False)
    major_conbine.iloc[-1, 0:2] = CONFIG.TOTAL_COLUMN
    excelUtil.writeExcel(major_conbine, file_path, CONFIG.GROUP_COLUMN[1] + measure_name)
    return


def report_value_rate(df_data, subject, title, filePath, add_name='',add_columns=[], measure_type=''):
    ls_metrics_cols = list(CONFIG.BASE_COLUMN)
    if subject not in list(CONFIG.BASE_COLUMN):
        ls_metrics_cols.append(subject)
    df_metrics = df_data.loc[:, ls_metrics_cols]

    option = formulas.answer_rate(df_metrics, subject)
    rate_t = formulas.rate_T(option)
    # 转置之后追加列，根据转置后的结果计算
    if add_name:
        rate_t.loc[:,add_name]=0
        for cal_num in add_columns:
            rate_t.loc[:,add_name] =rate_t.loc[:, add_name]+rate_t.loc[:,cal_num]
    if measure_type:
        rate_t = rate_t.loc[:, rebuild_five_columns(measure_type,0,1)]
    df_concat = pd.concat([rate_t, rate_t], sort=False)
    df_concat.insert(0, CONFIG.TOTAL_COLUMN, CONFIG.TOTAL_COLUMN)
    excelUtil.writeExcel(df_concat, filePath, CONFIG.TOTAL_COLUMN + title)

    college_changes = formulas.answer_college_value_rate(df_metrics, subject,
                                                         array_order=[CONFIG.RATE_COLUMN[2]],
                                                         array_asc=[0])
    college_t = formulas.college_rate_pivot(college_changes)
    college_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    if add_name:
        college_t.loc[:, add_name]=0
        for cal_num in add_columns:
            college_t.loc[:, add_name] =college_t.loc[:, add_name]+college_t.loc[:,cal_num]
    if measure_type:
        college_t = college_t.loc[:, rebuild_five_columns(measure_type,1,1)]
    college_t = pd.concat([college_t, rate_t], sort=False)
    college_t.iloc[-1, 0] = CONFIG.TOTAL_COLUMN
    excelUtil.writeExcel(college_t, filePath, CONFIG.GROUP_COLUMN[0] + title)

    major_changes = formulas.answer_major_value_rate(df_metrics, subject,
                                                     array_order=[CONFIG.RATE_COLUMN[2]],
                                                     array_asc=[0])
    major_t = formulas.major_rate_pivot(major_changes)
    if add_name:
        major_t.loc[:, add_name] = 0
        for cal_num in add_columns:
            major_t.loc[:, add_name] = major_t.loc[:, add_name] + major_t.loc[:, cal_num]
    if measure_type:
        major_t = major_t.loc[:, rebuild_five_columns(measure_type,2,1)]
    major_t.sort_values([CONFIG.RATE_COLUMN[2]], ascending=[0], inplace=True)
    major_t = pd.concat([major_t, rate_t], sort=False)
    major_t.iloc[-1, 0:2] = CONFIG.TOTAL_COLUMN
    excelUtil.writeExcel(major_t, filePath, CONFIG.GROUP_COLUMN[1] + title)

    return
