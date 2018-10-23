#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'cleanse.py'

__author__ = 'kuoren'

import data_analysis.read_excel_util as excelUtil
import data_analysis.utils as answerUtil
import data_analysis.reporter as report
import data_analysis.further_study as further


def main(file):

    data = excelUtil.read_excel(file)
    # a2_count=answerUtil.answer_count(data,"A2")
    # a2_dic=answerUtil.answer_val_count(data,"A2")
    # answerUtil.answer_grp_count(data,['_10','A2'],['_10'],'A2')
    # answerUtil.answer_grp_count(data,['_10','_14','A2'],['_10','_14'],'A2')
    # answerUtil.answer_of_subject_count(data,"A3","无法评价")

    #period = list(range(2000, 4000, 500))
    #print(period)

    further.further_report(data, report.REPORT_FOLDER + '国内升学.xlsx')
    further.study_abroad_report(data, report.REPORT_FOLDER + '出国境留学.xlsx')
    further.work_stability_report(data,report.REPORT_FOLDER + '工作稳定性.xlsx')
    further.work_option_report(data,report.REPORT_FOLDER + '就业机会.xlsx')
    # answerUtil.answer_grp_period(data, ['B6'], ['B6'], period)


if __name__ == '__main__':
    main("../test-data/san-ming/cleaned/answer1022_new.xlsx")
