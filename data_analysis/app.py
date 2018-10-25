#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'cleanse.py'

__author__ = 'kuoren'

import data_analysis.read_excel_util as excelUtil
import data_analysis.utils as answerUtil
import data_analysis.reporter as report
import data_analysis.further_study as further


def main(file):

    data = excelUtil.read_excel(file)

    report.sum_subject_report(data, 'B9-1', 1, report.REPORT_FOLDER + '专业相关度.xlsx')
    report.college_subject_report(data, 'B9-1', 1, report.REPORT_FOLDER + '专业相关度.xlsx')
    report.major_subject_report(data, 'B9-1', 1, report.REPORT_FOLDER + '专业相关度.xlsx')

    report.sum_subject_report(data, 'B8', 0, report.REPORT_FOLDER + '职业期待吻合度.xlsx')
    report.college_subject_report(data, 'B8', 0, report.REPORT_FOLDER + '职业期待吻合度.xlsx')
    report.major_subject_report(data, 'B8', 0, report.REPORT_FOLDER + '职业期待吻合度.xlsx')

    report.sum_subject_report(data, 'B7-A', 2, report.REPORT_FOLDER + '职业满意度.xlsx')
    report.college_subject_report(data, 'B7-A', 2, report.REPORT_FOLDER + '职业满意度.xlsx')
    report.major_subject_report(data, 'B7-A', 2, report.REPORT_FOLDER + '职业满意度.xlsx')
    report.sum_subject_report(data, 'B7-B', 2, report.REPORT_FOLDER + '职业满意度.xlsx')
    report.college_subject_report(data, 'B7-B', 2, report.REPORT_FOLDER + '职业满意度.xlsx')
    report.major_subject_report(data, 'B7-B', 2, report.REPORT_FOLDER + '职业满意度.xlsx')
    report.sum_subject_report(data, 'B7-C', 2, report.REPORT_FOLDER + '职业满意度.xlsx')
    report.college_subject_report(data, 'B7-C', 2, report.REPORT_FOLDER + '职业满意度.xlsx')
    report.major_subject_report(data, 'B7-C', 2, report.REPORT_FOLDER + '职业满意度.xlsx')
    report.sum_subject_report(data, 'B7-D', 2, report.REPORT_FOLDER + '职业满意度.xlsx')
    report.college_subject_report(data, 'B7-D', 2, report.REPORT_FOLDER + '职业满意度.xlsx')
    report.major_subject_report(data, 'B7-D', 2, report.REPORT_FOLDER + '职业满意度.xlsx')

    report.sum_employee_report(data, 'A2', report.REPORT_FOLDER + '就业率.xlsx')
    report.college_employee_report(data, 'A2', report.REPORT_FOLDER + '就业率.xlsx')
    report.major_employee_report(data, 'A2', report.REPORT_FOLDER + '就业率.xlsx')

    further.further_report(data, report.REPORT_FOLDER + '国内升学.xlsx')
    further.study_abroad_report(data, report.REPORT_FOLDER + '出国境留学.xlsx')
    further.work_stability_report(data,report.REPORT_FOLDER + '工作稳定性.xlsx')
    further.work_option_report(data,report.REPORT_FOLDER + '就业机会.xlsx')

    further.non_employee_report(data, report.REPORT_FOLDER + '未就业分析.xlsx')
    further.income_report(data, report.REPORT_FOLDER + '月均收入.xlsx')
    further.employee_industry_type(data, report.REPORT_FOLDER + '就业单位分布.xlsx')
    further.employee_industry_size(data, report.REPORT_FOLDER + '就业单位分布.xlsx')

    further.employee_region_report(data, report.REPORT_FOLDER + '就业地区分布.xlsx')

    further.employee_indurstry(data, report.REPORT_FOLDER + '就业行业分布.xlsx')
    further.employee_job(data, report.REPORT_FOLDER + '就业职业分布.xlsx')

    further.employee_difficult_report(data,report.REPORT_FOLDER + '求职过程.xlsx')

    further.school_satisfy_report(data,report.REPORT_FOLDER + '母校满意度.xlsx')
    report.college_subject_report(data, 'F2', 2, report.REPORT_FOLDER + '母校满意度.xlsx')
    report.major_subject_report(data, 'F2', 2, report.REPORT_FOLDER + '母校满意度.xlsx')

    further.school_recommed_report(data,report.REPORT_FOLDER + '母校推荐度.xlsx')


if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/answer1022_new.xlsx")
