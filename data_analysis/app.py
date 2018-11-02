#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'cleanse.py'

__author__ = 'kuoren'

import data_analysis.read_excel_util as excelUtil
import data_analysis.utils as answerUtil
import data_analysis.reporter as report
import data_analysis.further_study as further
import  data_analysis.formulas as formulas


def main(file):

    data = excelUtil.read_excel(file)
    further.basic_quality_report(data, report.REPORT_FOLDER + '基础素质.xlsx')

if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/answer1022_new.xlsx")
