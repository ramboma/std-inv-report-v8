#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""employ_rate.py"""
'''就业率及就业状态 相关报表'''

__author__ = 'kuoren'

import pandas as pd
from data_cleansing.logging import *
from data_analysis.formulas import *

logger = get_logger(__name__)


class EmpRateReport:
    _fold = '就业率及就业状态'

    def __init__(self, df_data):
        self.df_data = df_data

    def emp_rate(self):
        """总体就业率"""
        df_s = formulas_employe_rate(self.df_data)
        return df_s

    def emp_rate_grp(self, grps):
        '''分组计算就业率'''
        df_grp=formulas_employe_rate_grp(self.df_data);
        return df_grp

    def emp_rate_by_metric(self, metric, has_summary=False):
        """根据某个指标进行就业率计算，如学历、性别"""
        # step1：筛选出指标中的值
        ls_metric = list(set(self.df_data[metric]))
        df_combines = []
        # step2：循环值进行计算
        for where in ls_metric:
            df_where = self.df_data[self.df_data[metric] == where]
            df_emp_rate = formulas_employe_rate(df_where)
            df_emp_rate[metric] = where
            df_combines.append(df_emp_rate)
        if (has_summary):
            df_combines.append(self.emp_rate())
        # Concatenate everything into a single DataFrame
        df_combines = pd.concat(df_combines, ignore_index=True, sort=True)
        print(df_combines)
        return df_combines

    def emp_rate_by_cond(self, dict_cond, has_summary=False):
        """
        根据条件计算就业率
        :param dict_cond: {key:conds} eg:{'_x':['教育']}
        :param has_summary:
        :return:
        """
        if not isinstance(dict_cond, dict):
            raise "条件参数格式错误，条件：{}".format(dict_cond)
        metric = dict_cond.keys[0]
        where = dict_cond.values[0]
        name = "和".join(where)
        df_where = self.df_data[self.df_data[metric].isin(where)]
        df_emp_rate = formulas_employe_rate(df_where)
        df_emp_rate[metric] = name
        df_combines = []
        df_combines.append(df_emp_rate)
        if (has_summary):
            df_combines.append(self.emp_rate())
        # Concatenate everything into a single DataFrame
        df_combines = pd.concat(df_combines, ignore_index=True, sort=True)
        print(df_combines)
        return df_combines


