#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'utils.py'

__author__ = 'kuoren'
import pandas as pd
import data_analysis.config as CONFIG

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

def answer_grp_count(data, array_columns, array_groupby):
    '''
    根据分组条件，统计某-题回答人数
    :param data: 数据源
    :param array_groupby
    :return:
    '''
    grp = pd.DataFrame(data, columns=array_columns)
    if len(array_columns)==len(array_groupby):
        grp['cnt']=1
    grp_count = grp.groupby(array_groupby, as_index=False).count()
    return grp_count

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
    grp_answer_count=pd_answer.groupby(array_groupby, as_index=False).count()
    return  grp_answer_count

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
    count = data[data[subject]==answer][subject].count()
    return count

def answer_grp_sum(data,arry_columns,array_groupby):
    '''
    根据分组条件，统计其他列之和
    :param data: 数据源
    :param arry_columns: 相关列
    :param array_groupby: 分组列
    :return:
    '''
    grp=pd.DataFrame(data)[arry_columns].groupby(array_groupby, as_index=False).sum()
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

def answer_sum(data, subject):
    '''
    统计某题求和
    :param data: 数据源
    :param subject: 列名（题目ID）
    :return:
    '''
    sum = pd.DataFrame(data)[subject].sum()
    return sum

def test():
    df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
                       'B': [5, 6, 5, 8, 9],
                       'C': ['a', 'b', 'c', 'a', 'b']})
    df['new']=df.index

    df.replace({'new':{0:100,4:400}},inplace=True)
    print(df)
    pd_s=pd.DataFrame(df,columns=['C','B'])
    grouped=df.groupby(['C','B'], as_index=False).count()
    print(grouped)

def multi_columns(data, subject,max_times=0):
    '''多选题的选项列'''
    multi_column = []
    for col in data.columns:
        if subject in str(col):
            multi_column.append(col)

    if max_times:
        multi_column=multi_column[0:max_times]

    return multi_column


def multi_answer_count(data, subject):
    '''多选题 答题人数统计'''
    multi_column = multi_columns(data, subject)
    df_answer = data[multi_column]
    # resolve SettingWithCopyWarning problem
    df_copy = df_answer.copy()
    df_copy.dropna(how='all', inplace=True)
    df_copy.fillna(0, inplace=True)
    answer_count = df_copy[multi_column[0]].count()
    return answer_count

def multi_answer_distribution(data, subject):
    '''多选题 每个选项人数统计'''
    # step1 答题总人数
    answer_count = multi_answer_count(data, subject)
    # step2 结果集
    multi_column = multi_columns(data, subject)
    df_answer = data[multi_column]
    key = []
    result = []
    for col in df_answer.columns:
        key.append(col)
        result.append(df_answer[col].count())
    df_result = pd.DataFrame({'答案': key, '回答此答案人数': result})
    df_result['答题总人数'] = answer_count
    df_result['比例'] = (df_result['回答此答案人数'] / df_result['答题总人数']*100).round(decimals=2)
    # df_result['比例']=df_result['比例'].map(lambda x:'%.2f' % x) 格式化后无法参与计算
    return df_result


def ability_dis(data,subject):
    return 
def ability_item_distribution(data, subject):
    '''能力题 答题人数，能力水平分析'''
    # step1 答题总人数 N2
    answer_count = multi_answer_count(data, subject)

    multi_column = multi_columns(data, subject)
    # 单项能力水平题目数量N1
    item_size=multi_column.count()
    #结果集
    df_answer = data[multi_column]
    df_answer.dropna(how='all', inplace=True)

    df_answer['sum']=0
    for col in multi_column:
        # 反向分
        if col in CONFIG.ABILITY_REVERSE:
            df_answer[col + '_score'] = df_answer[col].map(CONFIG.ABILITY_SCORE_REVERSE)
        else:
            df_answer[col + '_score'] = df_answer[col].map(CONFIG.ABILITY_SCORE)
        df_answer['sum']=df_answer['sum']+df_answer[col + '_score']

    # 单个学生能力
    df_answer['ability']=df_answer['sum']/item_size
    ability=(df_answer['ability'].sum()/answer_count).round(2)

    df_result = pd.DataFrame({'答案': subject, '回答此答案人数': answer_count,'能力':ability})
    return df_result


def parse_ability_score(column_name):
    '''解析能力分值'''
    if column_name in CONFIG.ABILITY_REVERSE:
        return CONFIG.ABILITY_SCORE_REVERSE
    else:
        return CONFIG.ABILITY_SCORE










