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
    further.evelution_H4_R_report(data, CONFIG.REPORT_FOLDER + '社团活动.xlsx')
    further.evelution_academic_report(data, CONFIG.REPORT_FOLDER + '母校学风认可度.xlsx')
    further.evelution_H4_T_report(data, CONFIG.REPORT_FOLDER + '教育教学总体评价.xlsx')
    further.evelution_H4_S_report(data, CONFIG.REPORT_FOLDER + '实践教学的评价.xlsx')
    further.evelution_H4_E_report(data, CONFIG.REPORT_FOLDER + '任课教师.xlsx')

def test():
    data = pd.DataFrame({'class': ['c1', 'c2', 'c3', 'c4'],
                              'lesson': ['l1', 'l2', 'l1', 'l2'],
                              'score': [90, 95, 92, 98],
                              'degree': [90, 91, 90, 91]})
    data2=pd.DataFrame({'subject':['c1','c2','c3','c4'],
                        'content':['C1','C2','C3','C4']
    })

    s=data.loc[:,'score'].sum()
    print('{},avg:{}'.format(s,s/4))
    ds=data.describe()
    ds=ds[ds.index=='mean']
    ds=pd.concat([data,ds],sort=False)

    print(ds)
    data2.set_index('subject',inplace=True)
    data.loc[:, 'class']=data.loc[:,'class'].map({'c1':'C1'})
    print(data)

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
