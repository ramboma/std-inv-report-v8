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

    further.special_medical_report(data, report.REPORT_FOLDER + '医疗卫生职业.xlsx')
    further.special_social_health_report(data, report.REPORT_FOLDER + '卫生和社会工作.xlsx')


if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/answer1022_new.xlsx")
