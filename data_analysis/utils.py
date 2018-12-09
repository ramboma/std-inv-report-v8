#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'utils.py'

__author__ = 'kuoren'
import pandas as pd
import data_analysis.config as CONFIG


def answer_count(data, subject):
    '''
    统计某题回答总人数
    :param data: 数据源
    :param subject: 列名（题目ID）
    :return:
    '''
    total = pd.DataFrame(data)[subject].count()
    return total


def answer_val_count(data, subject):
    '''
    统计某题答案分布人数
    :param data: 数据源
    :param subject: 列名（题目ID）
    :return:
    '''
    subjects = pd.DataFrame(data)[subject]
    sub_value = subjects.value_counts()
    return sub_value


def answer_grp_count(data, array_columns, array_groupby):
    '''
    根据分组条件，统计某-题回答人数
    :param data: 数据源
    :param array_groupby
    :return:
    '''
    grp = pd.DataFrame(data, columns=array_columns)
    if len(array_columns) == len(array_groupby):
        grp['cnt'] = 1
    grp_count = grp.groupby(array_groupby, as_index=False).count()
    return grp_count


def answer_of_subject_count_grp(data, arry_columns, array_groupby, subject, answer):
    '''
    根据分组条件，统计某-题回答某个答案的人数
    :param data: 数据源
    :param subject: 列名（题目ID）
    :param answer: 答案
    :return:
    '''
    subj = pd.DataFrame(data, columns=arry_columns)
    pd_answer = subj[subj[subject] == answer]
    grp_answer_count = pd_answer.groupby(array_groupby, as_index=False).count()
    return grp_answer_count


def answer_of_subject_count(data, subject, answer):
    '''
    统计某-题回答某个答案的人数
    :param data: 数据源
    :param subject: 列名（题目ID）
    :param answer: 答案
    :return:
    '''
    if data.empty:
        return 0
    count = data[data[subject] == answer][subject].count()
    return count


def answer_grp_sum(data, arry_columns, array_groupby):
    '''
    根据分组条件，统计其他列之和
    :param data: 数据源
    :param arry_columns: 相关列
    :param array_groupby: 分组列
    :return:
    '''
    grp = pd.DataFrame(data)[arry_columns].groupby(array_groupby, as_index=False).sum()
    return grp


def answer_grp_period(data, arry_columns, array_groupby, array_periods):
    '''
    根据分组条件，统计其他列之和
    :param data: 数据源
    :param arry_columns: 相关列
    :param array_groupby: 分组列
    :return:
    '''
    grp = pd.DataFrame(data, columns=arry_columns)
    peroids = pd.cut(grp, array_periods)
    return peroids


def answer_sum(data, subject):
    '''
    统计某题求和
    :param data: 数据源
    :param subject: 列名（题目ID）
    :return:
    '''
    sum = pd.DataFrame(data)[subject].sum()
    return sum


def multi_columns(data, subject, max_times=0):
    '''多选题的选项列'''
    multi_column = []
    for col in data.columns:
        if subject in str(col):
            multi_column.append(col)

    if max_times:
        multi_column = multi_column[0:max_times]

    return multi_column


def multi_answer_count(data, subject):
    '''多选题 答题人数统计'''
    multi_column = multi_columns(data, subject)
    df_answer = data.loc[:,multi_column]
    df_answer.dropna(how='all', inplace=True)
    df_answer.fillna(0, inplace=True)
    answer_count = df_answer.loc[:,multi_column[0]].count()
    return answer_count



