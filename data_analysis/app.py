#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'cleanse.py'

__author__ = 'kuoren'

import data_analysis.read_excel_util as excelUtil
import data_analysis.report as further
import data_analysis.config as CONFIG
import pandas as pd

def main(file):
    data = excelUtil.read_excel(file)
    # 就业率和就业状态
    further.work_option_report(data, CONFIG.REPORT_FOLDER + '就业机会.xlsx')
    further.non_employee_report(data, CONFIG.REPORT_FOLDER + '未就业分析.xlsx')
    further.employee_report(data, CONFIG.REPORT_FOLDER + '就业率及就业就业状态.xlsx')

    # 就业竞争力
    further.major_relative_report(data, CONFIG.REPORT_FOLDER + '专业相关度.xlsx')
    further.job_meet_report(data, CONFIG.REPORT_FOLDER + '职业期待吻合度.xlsx')

    further.job_satisfy_report(data, CONFIG.REPORT_FOLDER + '就业满意度.xlsx')
    further.work_stability_report(data, CONFIG.REPORT_FOLDER + '工作稳定性.xlsx')

    further.income_report(data, CONFIG.REPORT_FOLDER + '月均收入.xlsx')

    # 就业分布
    further.employee_indurstry(data, CONFIG.REPORT_FOLDER + '就业行业分布.xlsx')
    further.employee_job(data, CONFIG.REPORT_FOLDER + '就业职业分布.xlsx')
    further.employee_industry_type(data, CONFIG.REPORT_FOLDER + '就业单位分布.xlsx')
    further.employee_industry_size(data, CONFIG.REPORT_FOLDER + '就业单位分布.xlsx')
    further.employee_region_report(data, CONFIG.REPORT_FOLDER + '就业地区分布.xlsx')

    # 求职过程与就业指导服务
    further.employee_difficult_report(data, CONFIG.REPORT_FOLDER + '求职过程.xlsx')

    # 母校综合评价
    further.school_satisfy_report(data, CONFIG.REPORT_FOLDER + '母校满意度.xlsx')
    further.school_recommed_report(data, CONFIG.REPORT_FOLDER + '母校推荐度.xlsx')

    # 学生指导与服务
    further.evelution_H4_Q_report(data, CONFIG.REPORT_FOLDER + '对学生生活服务的评价.xlsx')
    further.evelution_H4_P_report(data, CONFIG.REPORT_FOLDER + '对学生管理工作的评价.xlsx')
    further.evelution_H4_F_K_report(data, CONFIG.REPORT_FOLDER + '对就业教育服务的评价.xlsx')
    further.evelution_H4_L_O_report(data, CONFIG.REPORT_FOLDER + '对创业教育服务的反馈.xlsx')

    # 附加题
    further.evelution_H4_R_report(data, CONFIG.REPORT_FOLDER + '社团活动.xlsx')
    further.evelution_academic_report(data, CONFIG.REPORT_FOLDER + '母校学风认可度.xlsx')
    further.evelution_H4_T_report(data, CONFIG.REPORT_FOLDER + '教育教学总体评价.xlsx')
    further.evelution_H4_S_report(data, CONFIG.REPORT_FOLDER + '实践教学的评价.xlsx')
    further.evelution_H4_E_report(data, CONFIG.REPORT_FOLDER + '任课教师.xlsx')

    #国内升学
    further.further_report(data, CONFIG.REPORT_FOLDER + '国内升学.xlsx')

    # 出国境留学
    further.study_abroad_report(data, CONFIG.REPORT_FOLDER + '出国境留学.xlsx')
    # 自主创业
    further.self_employed_report(data, CONFIG.REPORT_FOLDER + '自主创业.xlsx')
    # 人才培养
    further.evelution_practice_report(data, CONFIG.REPORT_FOLDER + '对实践教学的评价.xlsx')
    further.evelution_lesson_report(data, CONFIG.REPORT_FOLDER + '对课堂教学的评价.xlsx')
    further.evelution_teach_report(data, CONFIG.REPORT_FOLDER + '对任课教师的评价.xlsx')

    # 特殊人群
    further.special_gender_report(data, CONFIG.REPORT_FOLDER + '不同性别.xlsx')
    further.special_education_report(data, CONFIG.REPORT_FOLDER + '教育行业和非教育行业.xlsx')
    further.special_origin_province_report(data, CONFIG.REPORT_FOLDER + '省内省外生源.xlsx')
    further.special_indurstry_province_report(data, CONFIG.REPORT_FOLDER + '省内省外就业.xlsx')
    further.special_national_report(data, CONFIG.REPORT_FOLDER + '汉族少数名族.xlsx')

    # 学习效果
    further.major_quality_report(data, CONFIG.REPORT_FOLDER + '专业素质.xlsx')
    further.basic_quality_report(data, CONFIG.REPORT_FOLDER + '基础素质.xlsx')


if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/AnswerList1540806254513_cleaned_本科毕业生_public_analysis_20181102235123.xlsx")
