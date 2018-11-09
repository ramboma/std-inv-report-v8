#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""salary_cleanser.py"""

__author__ = 'Gary.Z'

import numpy as np

from data_cleansing.config import *


class SalaryValueCollector:
    def __init__(self):
        self.__value_list = []
        self.__np_value_list = None
        self.__lock_down = False

    def collect(self, value):
        if self.__lock_down:
            raise Exception('cannot operate on a lock-down instance')
        if value is not None and isinstance(value, int):
            self.__value_list.append(value)

    def get_lower_limit(self):
        return SALARY_FILTER_LOWER_LIMIT

    def get_higher_limit(self):
        if not self.__lock_down:
            raise Exception('cannot operate on a non-lock-down instance')
        top_n = round(self.__value_list.__len__() * SALARY_FILTER_TOP_RATIO)
        return self.__value_list[top_n]

    def lock_down(self):
        self.__lock_down = True
        self.__value_list.sort(reverse=True)
        self.__np_value_list = np.array(self.__value_list, dtype=np.int64)

    def get_mean(self):
        if not self.__lock_down:
            raise Exception('cannot operate on a non-lock-down instance')
        return self.__np_value_list.mean()

    def get_stdev(self):
        if not self.__lock_down:
            raise Exception('cannot operate on a non-lock-down instance')
        return self.__np_value_list.std()


