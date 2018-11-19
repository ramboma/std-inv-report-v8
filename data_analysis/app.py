#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'cleanse.py'

__author__ = 'kuoren'

import data_analysis.read_excel_util as excelUtil
import data_analysis.report as further
import data_analysis.config as CONFIG
import pandas as pd
from data_analysis.config_loader import *

def main(file):
    data = excelUtil.read_excel(file)
    cofigL=ConfigLoader('config.xlsx')

    further.special_medical_report(data, CONFIG.REPORT_FOLDER + '医疗卫生职业.xlsx')
    further.special_social_health_report(data, CONFIG.REPORT_FOLDER + '卫生和社会工作.xlsx')



if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/cleaned.xlsx")
