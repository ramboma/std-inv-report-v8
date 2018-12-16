#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'data_calculate.py'

__author__ = 'kuoren'

class DataCalculator(object):
    def __init__(self, df, target_col, styler=None):
        self._df = df
        self._tgt_col = target_col
        self._styler = styler
        pass

    def calculate(self):
        raise Exception('method not implement')

