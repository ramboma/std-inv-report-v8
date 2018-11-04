#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'cleanse.py'

__author__ = 'kuoren'

import data_analysis.read_excel_util as excelUtil
import data_analysis.report as further
import data_analysis.config as CONFIG


def main(file):

    data = excelUtil.read_excel(file)
    # 学生指导与服务
    further.school_satisfy_report(data, CONFIG.REPORT_FOLDER + '母校满意度.xlsx')
    #further.income_report(data, CONFIG.REPORT_FOLDER + '月均收入.xlsx')


if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/answer1022_new.xlsx")
