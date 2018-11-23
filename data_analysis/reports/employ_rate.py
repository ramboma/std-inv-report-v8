#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""employ_rate.py"""
'''就业率及就业状态 相关报表'''

__author__ = 'kuoren'

import os
import pandas as pd
from data_cleansing.logging import *
import data_analysis.formulas as frm
logger = get_logger(__name__)


class EmpRateReport:
    _fold = '就业率及就业状态'

    def __init__(self, output_fold, df_data, subjects):
        self.output_fold=output_fold
        self.df_data = df_data
        self.subject = subjects

    @property
    def report_dir(self):
        dir_path=os.path.join(self.output_fold,self._fold)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        return dir_path

    def emp_rate(self):
        '''总体就业率'''
        df_s= frm.formulas_employe_rate(self.df_data)
        return df_s

    def emp_rate_degree(self, has_summary=False):
        ls_degree=list(set(self.df_data['_12']))
        degrees=[]
        for degree in ls_degree:
            df_where=self.df_data[self.df_data['_12']==degree]
            df_emp_rate=frm.formulas_employe_rate(df_where)
            df_emp_rate['degree']=degree
            degrees.append(df_emp_rate)
        if(has_summary):
            degrees.append(self.emp_rate())
        # Concatenate everything into a single DataFrame
        degrees = pd.concat(degrees, ignore_index=True,sort=True)
        print(degrees)