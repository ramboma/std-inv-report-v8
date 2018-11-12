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

    # 特殊人群
    further.special_gender_report(data, CONFIG.REPORT_FOLDER + '不同性别.xlsx')
    further.special_education_report(data, CONFIG.REPORT_FOLDER + '教育行业和非教育行业.xlsx')
    further.special_origin_province_report(data, CONFIG.REPORT_FOLDER + '省内省外生源.xlsx')
    further.special_indurstry_province_report(data, CONFIG.REPORT_FOLDER + '省内省外就业.xlsx')
    further.special_national_report(data, CONFIG.REPORT_FOLDER + '汉族少数名族.xlsx')
    further.special_medical_report(data, CONFIG.REPORT_FOLDER + '医疗卫生职业.xlsx')
    further.special_social_health_report(data, CONFIG.REPORT_FOLDER + '卫生和社会工作.xlsx')

    # 学习效果
    #further.major_quality_report(data, CONFIG.REPORT_FOLDER + '专业素质.xlsx')
    #further.basic_quality_report(data, CONFIG.REPORT_FOLDER + '基础素质.xlsx')


if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/AnswerList1540806254513_cleaned_本科毕业生_public_analysis_20181102235123.xlsx")
