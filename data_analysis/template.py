'template.py'

__author__ = 'kuoren'

import pandas as pd
import numpy as np
import data_analysis.utils as answerUtil
import data_analysis.read_excel_util as excelUtil
import data_analysis.config as CONFIG
import data_analysis.formulas as formulas

def tdl_value_rate(df_data,subject,file_path):
    '''总体模板1：各个值的占比，参考 就业行业分布-总体就业行业分布'''
    sheet_name = CONFIG.DICT_TITLE[subject]
    df_value_rate = formulas.answer_rate(df_data, subject)
    # 总人数降序
    df_value_rate.sort_values(CONFIG.RATE_COLUMN[-1], ascending=0, inplace=True)
    excelUtil.writeExcel(df_value_rate, file_path, CONFIG.TOTAL_COLUMN + sheet_name)

    return

def tdl_college_combine(df_data,subject,file_path,top=5):
    '''学院：参考 就业行业分布-各学院就业行业分布'''
    sheet_name = CONFIG.DICT_TITLE[subject]
    sheet_name='各{}{}'.format(CONFIG.GROUP_COLUMN[0],sheet_name)
    column_name=CONFIG.DICT_SUBJECT[subject]
    # 总人数、比例降序,top 5
    college_value = formulas.answer_college_value_rate(df_data, subject,
                                                       array_order=[CONFIG.RATE_COLUMN[2],CONFIG.RATE_COLUMN[-1]],
                                                       array_asc=[0, 0],
                                                       top=top)
    df_combine = formulas.college_row_combine(college_value, combin_name=column_name)
    excelUtil.writeExcel(df_combine, file_path, sheet_name)
    return


def tdl_major_combine(df_data, subject, file_path,top=5):
    sheet_name = CONFIG.DICT_TITLE[subject]
    sheet_name = '各{}{}'.format(CONFIG.GROUP_COLUMN[1], sheet_name)
    column_name = CONFIG.DICT_SUBJECT[subject]
    # 总人数、比例降序,top 5
    major_value = formulas.answer_major_value_rate(df_data, subject,
                                                   array_order=[CONFIG.RATE_COLUMN[2], CONFIG.RATE_COLUMN[-1]],
                                                   array_asc=[0, 0],top=top)
    df_combine = formulas.major_row_combine(major_value, combin_name=column_name)
    excelUtil.writeExcel(df_combine, file_path, sheet_name)
    return

def tdl_value_rate_t(df_data,subject,file_path):
    '''总体模板2：各个值的占比,行转列，追加总体。参考 就业行业分布-总体就业行业分布'''
    sheet_name = CONFIG.DICT_TITLE[subject]

    df_value_rate = formulas.answer_rate(df_data, subject)
    df_t = formulas.rate_T(df_value_rate)
    df_concat = pd.concat([df_t, df_t], sort=False)
    df_concat.insert(0, CONFIG.TOTAL_COLUMN, CONFIG.TOTAL_COLUMN)
    excelUtil.writeExcel(df_concat, file_path, CONFIG.TOTAL_COLUMN +sheet_name)
    return