#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""rep_common.py"""
'''报表计算通用方法'''

__author__ = 'kuoren'

import pandas as pd
from data_analysis.formulas import *


def comm_rate(df_data, subject, do_t=False):
    df_rate = formula_rate(df_data, subject)
    if do_t:
        df_rate = formate_rate_t(df_rate)
    return df_rate


def comm_rate_by_metric(df_data, subject, metric, do_t=False, has_summary=False):
    """根据某个指标统计某题的占比，如学历、性别"""
    # step1：筛选出指标中的值
    ls_metric = list(set(df_data[metric]))
    df_combines = []
    # step2：循环值进行计算
    for where in ls_metric:
        df_where = df_data[df_data[metric] == where]
        df_rate = formula_rate(df_where, subject)
        if do_t:
            df_rate = formate_rate_t(df_rate)
        df_rate[metric] = where
        df_combines.append(df_rate)
    if has_summary:
        df_combines.append(comm_rate(df_data, subject, do_t))
    # Concatenate everything into a single DataFrame
    df_combines = pd.concat(df_combines, ignore_index=True, sort=True)
    print(df_combines)
    return df_combines
