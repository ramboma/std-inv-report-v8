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

    further.employee_report(data, report.REPORT_FOLDER + '就业率及就业就业状态.xlsx')

if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/answer1022_new.xlsx")
