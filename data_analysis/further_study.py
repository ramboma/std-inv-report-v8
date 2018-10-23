#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'further_study.py'

__author__ = 'kuoren'

import pandas as pd
import data_analysis.utils as answerUtil
import data_analysis.read_excel_util as excelUtil
import data_analysis.config as config


def study_abroad_report(data, filePath):
    a2_count = answerUtil.answer_count(data, 'A2')
    study_value = answer_value_rate(data, 'E2')
    study_value['答A2题总人数'] = a2_count
    study_value.drop(config.VALUE_RATE_COLUMN[2:4], axis='columns', inplace=True)
    study_value[config.VALUE_RATE_COLUMN[-1]] = (
                study_value[config.VALUE_RATE_COLUMN[1]] / study_value['答A2题总人数'] * 100).round(decimals=2)
    excelUtil.writeExcel(study_value, filePath, '留学比列')

    study_satisfy = answer_five_rate(data, 'F2', 2)
    excelUtil.writeExcel(study_satisfy, filePath, '留学录取结果满意度')

    study_relative = answer_five_rate(data, 'F3', 1)
    excelUtil.writeExcel(study_relative, filePath, '留学专业一致性')

    change_study_reason = answer_value_rate(data, 'F4')
    excelUtil.writeExcel(change_study_reason, filePath, '跨专业升学原因')


def further_report(data, filePath):
    further_rate = answer_rate(data, 'A2', config.A2_ANSWER[3])
    excelUtil.writeExcel(further_rate, filePath, '总体国内升学比例')

    further_reason = answer_value_rate(data, 'E2')
    excelUtil.writeExcel(further_reason, filePath, '升学原因')

    further_satisfy = answer_five_rate(data, 'E1', 2)
    excelUtil.writeExcel(further_satisfy, filePath, '升学录取结果满意度')

    further_relative = answer_five_rate(data, 'E3', 1)
    excelUtil.writeExcel(further_relative, filePath, '升学专业相关度')

    change_reason = answer_value_rate(data, 'E4')
    excelUtil.writeExcel(change_reason, filePath, '跨专业升学原因')


def work_stability_report(data, filePath):
    change_times = answer_value_rate(data, 'B10-1')
    no_changes = change_times[change_times[config.VALUE_RATE_COLUMN[0]].isin([config.B10_1_ANSWER[0]])][[config.VALUE_RATE_COLUMN[-1]]]
    no_changes.fillna(0,inplace=True)
    change_times['离职率'] = 100-no_changes
    excelUtil.writeExcel(change_times, filePath, '总体离职情况分布')

    college_changes=answer_college_value_rate(data,'B10-1')
    college_no_change=college_changes[college_changes['答案'].isin([config.B10_1_ANSWER[0]])][['学院','比例']]
    college_no_change['离职率']=100-college_no_change['比例']
    college_no_change.drop('比例', axis='columns', inplace=True)
    college_changes_left=pd.merge(college_changes,college_no_change,
                                  how='left',
                                  on='学院')
    excelUtil.writeExcel(college_changes_left, filePath, '各学院离职情况')

    major_changes = answer_major_value_rate(data, 'B10-1')
    major_no_change = major_changes[major_changes['答案'].isin([config.B10_1_ANSWER[0]])][['学院','专业','比例']]
    major_no_change['离职率'] = 100 - major_no_change['比例']
    major_no_change.drop('比例', axis='columns', inplace=True)
    major_changes_left = pd.merge(major_changes, major_no_change,
                                    how='left',
                                    on=['学院','专业'])
    excelUtil.writeExcel(major_changes_left, filePath, '各专业离职情况')

    change_reason=answer_value_rate(data,'B10-2')
    excelUtil.writeExcel(change_reason, filePath, '更换工作原因')


def work_option_report(data, filePath):
    option = answer_value_rate(data, 'A3')
    no_option = option[option['答案'].isin([config.EXCEPTED_ANSWER])][[config.VALUE_RATE_COLUMN[1]]]
    no_option.fillna(0, inplace=True)
    option['有效人数']=option[config.VALUE_RATE_COLUMN[2]]-no_option[config.VALUE_RATE_COLUMN[1]]

    option[config.VALUE_RATE_COLUMN[-1]]=(option[config.VALUE_RATE_COLUMN[1]]/option['有效人数']*100).round(decimals=2)
    excelUtil.writeExcel(option, filePath, '总体就业机会')

    college_changes=answer_college_value_rate(data,'A3')
    college_no_change=college_changes[college_changes['答案'].isin([config.EXCEPTED_ANSWER])][['学院',config.VALUE_RATE_COLUMN[1]]]

    pd_left=pd.merge(college_changes,college_no_change,
                     how='left',
                     on='学院',
                     )
    pd_left.fillna(0,inplace=True)

    pd_left[config.VALUE_RATE_COLUMN[-1]]= (pd_left[config.VALUE_RATE_COLUMN[1]+'_x']/(pd_left[config.VALUE_RATE_COLUMN[2]]-pd_left[config.VALUE_RATE_COLUMN[1]+'_y'])*100).round(decimals=2)
    excelUtil.writeExcel(pd_left, filePath, '各学院就业机会')

    major_changes = answer_major_value_rate(data, 'A3')
    major_no_change = major_changes[major_changes['答案'].isin([config.EXCEPTED_ANSWER])][['学院','专业',config.VALUE_RATE_COLUMN[1]]]
    pd_left_major=pd.merge(major_changes,major_no_change,how='left',on=['学院','专业'])
    pd_left_major.fillna(0,inplace=True)
    pd_left_major[config.VALUE_RATE_COLUMN[-1]]= (pd_left_major[config.VALUE_RATE_COLUMN[1]+'_x']/(pd_left_major[config.VALUE_RATE_COLUMN[2]]-pd_left_major[config.VALUE_RATE_COLUMN[1]+'_y'])*100).round(decimals=2)

    excelUtil.writeExcel(pd_left_major, filePath, '各专业就业机会')



def answer_five_rate(data, subject, answerType):
    '''某一题五维占比'''
    # step1：各个答案占比
    pd_five_rate = answer_value_rate(data, subject)
    pd_five_rate.drop('比例', axis='columns', inplace=True)
    invalid_count = answerUtil.answer_of_subject_count(data, subject, config.EXCEPTED_ANSWER)
    pd_five_rate['比例'] = (pd_five_rate['回答此答案人数'] / (pd_five_rate['答题总人数'] - invalid_count) * 100).round(decimals=2)

    # step2: 相关度/满意度
    if answerType == 0:
        pd_relative = pd_five_rate[pd_five_rate['答案'].isin(config.ANSWER_NORMAL_1[0:3])]['比例'].sum()
        relativeName = '符合度'
    elif answerType == 1:
        pd_relative = pd_five_rate[pd_five_rate['答案'].isin(config.ANSWER_NORMAL_2[0:3])]['比例'].sum()
        relativeName = '相关度'
    elif answerType == 2:
        pd_relative = pd_five_rate[pd_five_rate['答案'].isin(config.ANSWER_NORMAL_3[0:3])]['比例'].sum()
        relativeName = '满意度'
    pd_five_rate[relativeName] = pd_relative

    pd_five_rate['val_score'] = pd_five_rate['答案']

    if answerType == 0:
        pd_five_rate.replace({'val_score': config.ANSWER_SCORE_DICT_1}, inplace=True)
    elif answerType == 1:
        pd_five_rate.replace({'val_score': config.ANSWER_SCORE_DICT_2}, inplace=True)
    elif answerType == 2:
        pd_five_rate.replace({'val_score': config.ANSWER_SCORE_DICT_3}, inplace=True)

    pd_five_rate['val_score'] = pd_five_rate['回答此答案人数'] * pd_five_rate['val_score']
    alpha_x = pd_five_rate['val_score'].sum()
    pd_five_rate['均值'] = (alpha_x / (pd_five_rate['答题总人数'] - invalid_count)).round(decimals=2)
    pd_five_rate.drop('val_score', axis='columns', inplace=True)
    return pd_five_rate


def answer_rate(data, subject, answer):
    '''某一题某个答案总体占比'''
    count = answerUtil.answer_count(data, subject);
    answer_count = answerUtil.answer_of_subject_count(data, subject, answer)
    rate = (answer_count / count * 100).round(decimals=2)
    title = "回答'{}'人数".format(answer)
    df = pd.DataFrame({title: [answer_count],
                       '答题总人数': [count],
                       '比例': [rate]})
    return df


def answer_value_rate(data, subject):
    '''各答案占比'''
    count = answerUtil.answer_count(data, subject);
    pd_value_count = answerUtil.answer_val_count(data, subject)
    pd_result = pd.DataFrame({'答案': pd_value_count.index,
                              '回答此答案人数': pd_value_count.values})
    pd_result['答题总人数'] = count
    pd_result['比例'] = (pd_result['回答此答案人数'] / pd_result['答题总人数'] * 100).round(decimals=2)
    return pd_result

def answer_college_value_rate(data,subject):
    pd_count=answerUtil.answer_grp_count(data,[config.BASE_COLUMN[0],subject],[config.BASE_COLUMN[0]])
    pd_value_count=answerUtil.answer_grp_count(data,[config.BASE_COLUMN[0],subject],[config.BASE_COLUMN[0],subject])

    pd_left=pd.merge(pd_value_count,pd_count,on=config.BASE_COLUMN[0],how='left',suffixes=('_x','_y'))
    pd_left.columns=['学院','答案','回答此答案人数','答题总人数']
    pd_left['比例'] = (pd_left['回答此答案人数'] / pd_left['答题总人数'] * 100).round(decimals=2)

    return pd_left


def answer_major_value_rate(data, subject):
    pd_count = answerUtil.answer_grp_count(data,
                                           [config.BASE_COLUMN[0],config.BASE_COLUMN[1], subject],
                                           [config.BASE_COLUMN[0],config.BASE_COLUMN[1]])
    pd_value_count = answerUtil.answer_grp_count(data,
                                                 [config.BASE_COLUMN[0],config.BASE_COLUMN[1], subject],
                                                 [config.BASE_COLUMN[0],config.BASE_COLUMN[1], subject])
    pd_left = pd.merge(pd_value_count, pd_count,
                       on=[config.BASE_COLUMN[0],config.BASE_COLUMN[1]],
                       how='left', suffixes=('_x', '_y'))
    pd_left.columns = ['学院','专业', '答案', '回答此答案人数', '答题总人数']
    pd_left['比例'] = (pd_left['回答此答案人数'] / pd_left['答题总人数'] * 100).round(decimals=2)

    return pd_left

