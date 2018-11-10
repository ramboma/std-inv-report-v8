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
    further.job_satisfy_report(data, CONFIG.REPORT_FOLDER + '就业满意度.xlsx')
    further.income_report(data, CONFIG.REPORT_FOLDER + '月均收入.xlsx')

def test():
    data = pd.DataFrame(data={'class': ['c1', 'c1', 'c2', 'c2'],
                              'lesson': ['l1', 'l2', 'l1', 'l2'],
                              'score': [90, 95, 92, 98],
                              'degree': [90, 91, 90, 91]})
    data.set_index(['class', 'lesson'], inplace=True)

    data_t = data.unstack(0)
    print(data_t)
    cs = [['class']]
    cs.append(['score', 'degree'])
    print(cs)

    dp=pd.pivot_table(data=data,index='lesson',columns='class')[['score','degree']]
    print(dp)
if __name__ == '__main__':
    #test()
    main("../test-data/san-ming/cleaned/AnswerList1540806254513_cleaned_本科毕业生_public_analysis_20181102235123.xlsx")
