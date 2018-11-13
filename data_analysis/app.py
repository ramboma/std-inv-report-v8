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

    # 人才培养
    further.evelution_teach_report(data, CONFIG.REPORT_FOLDER + '对任课教师的评价.xlsx')



if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/AnswerList1540806254513_cleaned_本科毕业生_public_analysis_20181102235123.xlsx")
