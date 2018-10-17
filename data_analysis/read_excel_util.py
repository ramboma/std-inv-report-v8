#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'read_excel_util.py'

__author__ = 'kuoren'

import pandas as pd

def read_excel(filePath):
    '''
    Read excel
    :param filePath:
    :return:
    '''
    print("loading file...")
    xls=pd.ExcelFile(filePath)
    df=xls.parse()
    print(df)
    return df

if __name__=="__main__":
    read_excel("../test-data/san-ming/cleaned/answer20181016_174011234.xlsx")