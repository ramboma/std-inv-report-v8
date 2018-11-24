#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'cleanse.py'

__author__ = 'kuoren'

import data_analysis.read_excel_util as excelUtil
import data_analysis.report as further
import data_analysis.config as CONFIG
import pandas as pd
import data_analysis.formulas as fml
from data_analysis.reports.employ_rate import *

def main(file):
    data = excelUtil.read_excel(file)
    df_rate=fml.formulas_five_rate_grp(data,'G2',['_10'],CONFIG.ANSWER_TYPE_RELATIVE)
    #fml.formate_rate_t(df_rate)
    #fml.formulas_employe_rate(data)
    #fml.formulas_employe_rate_grp(data,['_10','_14'])




if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/cleaned.xlsx")
