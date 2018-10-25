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
    further.self_employed_report(data,report.REPORT_FOLDER + '自主创业.xlsx')
    further.basic_quality_report(data,report.REPORT_FOLDER + '基础素质.xlsx')
    further.major_quality_report(data,report.REPORT_FOLDER + '专业素质.xlsx')
    further.evelution_lesson_report(data,report.REPORT_FOLDER + '课堂教学的评价.xlsx')
    further.evelution_practice_report(data,report.REPORT_FOLDER + '实践教学的评价.xlsx')
    further.evelution_practice_report(data,report.REPORT_FOLDER + '教师和管理的评价.xlsx')

if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/answer1022_new.xlsx")
