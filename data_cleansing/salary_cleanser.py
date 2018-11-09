#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""salary_cleanser.py"""

__author__ = 'Gary.Z'

import numpy as np

from data_cleansing.config import *

logger = get_logger(__name__)


class SalaryValueCollector:
    def __init__(self):
        self.__value_list = []
        # self.__np_value_list = None
        self.__top_n = 0
        self.__lock_down = False
        self.__mean = 0
        self.__stdev = 0
        self.__stdev_4 = 0

    def collect(self, value):
        if self.__lock_down:
            raise Exception('cannot operate on a lock-down instance')
        if value is not None:
            if isinstance(value, int):
                self.__value_list.append(value)
            else:
                raise Exception("{} is not number".format(value))

    def get_lower_limit(self):
        return SALARY_FILTER_LOWER_LIMIT

    def get_higher_limit(self):
        if not self.__lock_down:
            raise Exception('cannot operate on a non-lock-down instance')
        return self.__value_list[self.__top_n - 1]

    def get_top_n(self):
        return self.__top_n

    def lock_down(self):
        self.__lock_down = True
        self.__top_n = round(self.__value_list.__len__() * SALARY_FILTER_TOP_RATIO)

        if self.__top_n < 1:
            raise Exception('Unexpected top n < 1')

        new_list = []
        self.__value_list.sort(reverse=True)
        for value in self.__value_list:
            if value < self.get_lower_limit() or value >= self.get_higher_limit():
                continue
            new_list.append(value)
        np_value_list = np.array(new_list, dtype=np.int64)
        self.__mean = np_value_list.mean()
        self.__stdev = np_value_list.std()
        self.__stdev_4 = self.__stdev * 4

    def get_mean(self):
        if not self.__lock_down:
            raise Exception('cannot operate on a non-lock-down instance')
        return self.__mean

    def get_stdev(self):
        if not self.__lock_down:
            raise Exception('cannot operate on a non-lock-down instance')
        return self.__stdev

    def get_stdev_4(self):
        if not self.__lock_down:
            raise Exception('cannot operate on a non-lock-down instance')
        return self.__stdev_4

    def report(self):
        logger.info('salary collector result:')
        logger.info('>> total: {}'.format(self.__value_list.__len__()))
        logger.info('>> lower limit: {}'.format(self.get_lower_limit()))
        logger.info('>> top N: {}'.format(self.get_top_n()))
        logger.info('>> higher limit: {}'.format(self.get_higher_limit()))
        logger.info('>> mean: {}'.format(self.get_mean()))
        logger.info('>> stdev: {}'.format(self.get_stdev()))
        logger.info('>> stdev*4: {}'.format(self.get_stdev_4()))

    def __str__(self):
        return 'salary collector result: total: {}, lower limit: {}, top N: {}, higher limit: {}, mean: {}, stdev: {}, stdev*4: {}'\
            .format(self.__value_list.__len__(), self.get_lower_limit(), self.get_top_n(), self.get_higher_limit(), self.get_mean(), self.get_stdev(), self.get_stdev_4())

    __repr__ = __str__
