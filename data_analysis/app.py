#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'cleanse.py'

__author__ = 'kuoren'

import data_analysis.read_excel_util as excelUtil
import data_analysis.utils as answerUtil
import data_analysis.reporter as report


def main(file):
    answerUtil.test()


    data = excelUtil.read_excel(file)
    # a2_count=answerUtil.answer_count(data,"A2")
    # a2_dic=answerUtil.answer_val_count(data,"A2")
    # answerUtil.answer_grp_count(data,['_10','A2'],['_10'],'A2')
    # answerUtil.answer_grp_count(data,['_10','_14','A2'],['_10','_14'],'A2')
    # answerUtil.answer_of_subject_count(data,"A3","无法评价")

    #period = list(range(2000, 4000, 500))
    #print(period)
    #report.employability_college(data)
    report.employability_major(data)
    # answerUtil.answer_grp_period(data, ['B6'], ['B6'], period)


if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/answer20181017_test.xlsx")
