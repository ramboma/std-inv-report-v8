#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'utils.py'

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
    return  grp_count

def answer_of_subject_count_grp(data,arry_columns,array_groupby,subject,answer):
    '''
    根据分组条件，统计某-题回答某个答案的人数
    :param data: 数据源
    :param subject: 列名（题目ID）
    :param answer: 答案
    :return:
    '''
    subj=pd.DataFrame(data,columns=arry_columns)
    pd_answer=subj[subj[subject]==answer]
    grp_answer_count=pd_answer.groupby(array_groupby)[subject].count()
    return  grp_answer_count

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

def test():
    df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
                       'B': [5, 6, 7, 8, 9],
                       'C': ['a', 'b', 'c', 'd', 'e']})
    df['new']=df.index

    df.replace({'new':{0:100,4:400}},inplace=True)
    print(df)


