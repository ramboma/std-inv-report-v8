#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""employ_rate.py"""
'''就业率及就业状态 相关报表'''

__author__ = 'kuoren'

import pandas as pd
from data_cleansing.logging import *
from data_analysis.formulas import *
from data_analysis.reports.rep_common import *

logger = get_logger(__name__)


class EmpRateReport:
    def __init__(self, df_data):
        self.df_data = df_data

    def emp_rate(self):
        """总体就业率"""
        df_s = formula_employe_rate(self.df_data)
        return df_s

    def emp_rate_grp(self, grps):
        '''分组计算就业率'''
        df_grp = formula_employe_rate_grp(self.df_data, grps);
        return df_grp

    def emp_rate_by_metric(self, metric, has_summary=False):
        """根据某个指标进行就业率计算，如学历、性别"""
        # step1：筛选出指标中的值
        ls_metric = list(set(self.df_data[metric]))
        df_combines = []
        # step2：循环值进行计算
        for where in ls_metric:
            df_where = self.df_data[self.df_data[metric] == where]
            df_emp_rate = formula_employe_rate(df_where)
            df_emp_rate[metric] = where
            df_combines.append(df_emp_rate)
        if has_summary:
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
        df_emp_rate = formula_employe_rate(df_where)
        df_emp_rate[metric] = name
        df_combines = []
        df_combines.append(df_emp_rate)
        if has_summary:
            df_combines.append(self.emp_rate())
        # Concatenate everything into a single DataFrame
        df_combines = pd.concat(df_combines, ignore_index=True, sort=True)
        print(df_combines)
        return df_combines

    def emp_go(self):
        subject = 'A3'
        df_rate = formate_rate_t(formula_rate(self.df_data, subject))
        # 添加灵活就业率
        free = 0
        for metric in CONFIG.EMP_FREE_COLUMNS:
            free = free + df_rate[metric]
        df_rate.insert(-1, CONFIG.EMP_FREE, free)
        return df_rate

    def emp_go_by_metric(self, metric, has_summary=False):
        """根据某个指标进行就业去向统计，如学历、性别"""
        subject = 'A3'
        # step1：筛选出指标中的值
        ls_metric = list(set(self.df_data[metric]))
        df_combines = []
        # step2：循环值进行计算
        for where in ls_metric:
            df_where = self.df_data[self.df_data[metric] == where]
            df_rate = formate_rate_t(formula_rate(df_where, subject))
            free = 0
            for metric in CONFIG.EMP_FREE_COLUMNS:
                free = free + df_rate[metric]
            df_rate.insert(-1, CONFIG.EMP_FREE, free)
            df_rate[metric] = where
            df_combines.append(df_rate)
        if has_summary:
            df_combines.append(self.emp_go())
        # Concatenate everything into a single DataFrame
        df_combines = pd.concat(df_combines, ignore_index=True, sort=True)
        print(df_combines)
        return df_combines


class UnEmpReport:
    def __init__(self, df_data):
        self.df_data = df_data

    def unemployee(self):
        subject = "C1"
        df_rate = formula_rate(self.df_data, subject)
        return df_rate

    def unemployee_go(self):
        subject = "C2"
        df_rate = formula_rate(self.df_data, subject)
        return df_rate

    def unemployee_by_metric(self, metric, has_summary=False):
        subject = "C1"
        return comm_rate_by_metric(self.df_data,subject,do_t=False,has_summary=has_summary)


    def unemployee_go_by_metric(self, metric, has_summary=False):
        subject = "C2"
        return comm_rate_by_metric(self.df_data,subject,do_t=False,has_summary=has_summary)
