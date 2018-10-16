#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'utils.py'

__author__ = 'Gary.Z'

import pandas as pd

def load_xlsx_file(path):
    df = pd.read_excel(path)
    return df



def test():
    print('test not implement')

if __name__=='__main__':
    test()