#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'answer_util.py'

__author__ = 'kuoren'
import pandas as pd

def answer_count(data,subject):
    '''
    统计某题回答总人数
    :param data: 数据源
    :param subject: 列名（题目ID）
    :return:
    '''
    total=pd.DataFrame(data)[subject].count()
    print("{} 答题总人数：{}".format(subject,total))
    return  total

def answer_val_count(data,subject):
    '''
    统计某题答案分布人数
    :param data: 数据源
    :param subject: 列名（题目ID）
    :return:
    '''
    subjects=pd.DataFrame(data)[subject]
    sub_value=subjects.value_counts()
    print(sub_value)
    return  sub_value

def answer_grp_count(data,arry_columns,array_groupby,subject):
    '''
    根据分组条件，统计某-题回答人数
    :param data: 数据源
    :param subject: 列名（题目ID）
    :return:
    '''
    grp=pd.DataFrame(data,columns=arry_columns)
    grp_count=grp.groupby(array_groupby)[subject].count()
    print(grp_count)
    return  grp_count

def answer_of_subject_count(data,subject,answer):
    '''
    统计某-题回答某个答案的人数
    :param data: 数据源
    :param subject: 列名（题目ID）
    :param answer: 答案
    :return:
    '''
    subj=pd.DataFrame(data)[subject]
    answer_count=subj[subj==answer].count()
    print("{}回答{}的人数：{}".format(subject,answer,answer_count))
    return  answer_count

def answer_grp_sum(data,arry_columns,array_groupby):
    '''
    根据分组条件，统计其他列之和
    :param data: 数据源
    :param arry_columns: 相关列
    :param array_groupby: 分组列
    :return:
    '''
    grp=pd.DataFrame(data)[arry_columns].groupby(array_groupby).sum()
    print(grp)
    return  grp

def answer_grp_period(data,arry_columns,array_groupby,array_periods):
    '''
    根据分组条件，统计其他列之和
    :param data: 数据源
    :param arry_columns: 相关列
    :param array_groupby: 分组列
    :return:
    '''
    grp=pd.DataFrame(data,columns=arry_columns)
    peroids=pd.cut(grp,array_periods)
    print(peroids)
    return  peroids


