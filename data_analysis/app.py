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
    #df_rate=formula_mean_grp(data,'B6',['_10'])
    #df_rate=formula_answer_period(data,'B6',2000,4,500)
    data=data[data["_12"]=="博士毕业生"]
    #df_rate=fml.formula_five_rate_grp(data,'G2',['_10'],CONFIG.ANSWER_TYPE_RELATIVE)
    #fml.formate_rate_t(df_rate)
    df_rate =fml.formula_employe_rate_grp(data,['_10'])
    #fml.formula_five_rate_grp(data,['_10','_14'])
    print(df_rate)




if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/cleaned.xlsx")
