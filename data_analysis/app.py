#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'app.py'

__author__ = 'kuoren'

import read_excel_util as excelUtil
import answer_util as answerUtil

def main(file):
    data = excelUtil.read_excel(file)
    #a2_count=answerUtil.answer_count(data,"A2")
    #a2_dic=answerUtil.answer_val_count(data,"A2")
    #answerUtil.answer_grp_count(data,['_10','A2'],['_10'],'A2')
    #answerUtil.answer_grp_count(data,['_10','_14','A2'],['_10','_14'],'A2')
    #answerUtil.answer_of_subject_count(data,"A3","无法评价")

    period=list(range(2000, 4000, 500))
    print(period)
    #answerUtil.answer_grp_period(data, ['B6'], ['B6'], period)


if __name__=='__main__':
        main("../test-data/san-ming/cleaned/answer20181017_test.xlsx")