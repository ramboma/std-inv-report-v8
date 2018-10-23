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
    # a2_count=answerUtil.answer_count(data,"A2")
    # a2_dic=answerUtil.answer_val_count(data,"A2")
    # answerUtil.answer_grp_count(data,['_10','A2'],['_10'],'A2')
    # answerUtil.answer_grp_count(data,['_10','_14','A2'],['_10','_14'],'A2')
    # answerUtil.answer_of_subject_count(data,"A3","无法评价")

    #period = list(range(2000, 4000, 500))
    #print(period)

    report.sum_subject_report(data,'B9-1',1,report.REPORT_FOLDER+'专业相关度.xlsx')
    report.college_subject_report(data,'B9-1',1,report.REPORT_FOLDER+'专业相关度.xlsx')
    report.major_subject_report(data,'B9-1',1,report.REPORT_FOLDER+'专业相关度.xlsx')

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

    report.sum_employee_report(data,'A2',report.REPORT_FOLDER + '就业率.xlsx')
    report.college_employee_report(data,'A2',report.REPORT_FOLDER + '就业率.xlsx')
    report.major_employee_report(data,'A2',report.REPORT_FOLDER + '就业率.xlsx')

    further.further_report(data,report.REPORT_FOLDER + '国内升学.xlsx')
    further.study_abroad_report(data,report.REPORT_FOLDER + '出国境留学.xlsx')


    # answerUtil.answer_grp_period(data, ['B6'], ['B6'], period)


if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/answer1022_new.xlsx")
