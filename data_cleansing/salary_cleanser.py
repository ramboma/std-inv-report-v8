#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""salary_cleanser.py"""

__author__ = 'Gary.Z'

import sys
import numpy as np

from data_cleansing.config import *

# logger = get_logger(__name__)


class SalaryValueCollector:
    def __init__(self, log_handler=None):
        self._value_list = []
        # self.__np_value_list = None
        # self._top_n = 0
        self._lock_down = False
        self._mean = 0
        self._stdev = 0
        self._stdev_4 = 0
        self._logger = get_logger('{}${}'.format(self.__class__.__name__, id(self)))
        if log_handler is not None:
            self._logger.addHandler(log_handler)

    @property
    def logger(self):
        return self._logger

    def collect(self, value):
        if self._lock_down:
            raise Exception('cannot operate on a lock-down instance')
        if value is not None:
            if isinstance(value, int):
                self._value_list.append(value)
            else:
                raise Exception("{} is not number".format(value))

    def get_lower_limit(self):
        return SALARY_FILTER_LOWER_LIMIT

    def get_higher_limit(self):
        if not self._lock_down:
            raise Exception('cannot operate on a non-lock-down instance')
        # if self._top_n > 0:
        #     return self._value_list[self._top_n - 1]
        # else:
        #     return sys.maxsize
        return SALARY_FILTER_HIGHER_LIMIT

    # def get_top_n(self):
    #     return self._top_n

    def lock_down(self):
        self._lock_down = True
        # self._top_n = round(self._value_list.__len__() * SALARY_FILTER_TOP_RATIO)
        #
        # if self._top_n < 1:
        #     # raise Exception('Unexpected top n < 1')
        #     self._logger.warn('Unexpected top n({}) < 1'.format(self._top_n))

        new_list = []
        self._value_list.sort(reverse=True)
        for value in self._value_list:
            if value < self.get_lower_limit() or value >= self.get_higher_limit():
                continue
            new_list.append(value)
        np_value_list = np.array(new_list, dtype=np.int64)
        self._mean = np_value_list.mean()
        self._stdev = np_value_list.std()
        self._stdev_4 = self._stdev * 4

    def get_mean(self):
        if not self._lock_down:
            raise Exception('cannot operate on a non-lock-down instance')
        return self._mean

    def get_stdev(self):
        if not self._lock_down:
            raise Exception('cannot operate on a non-lock-down instance')
        return self._stdev

    def get_stdev_4(self):
        if not self._lock_down:
            raise Exception('cannot operate on a non-lock-down instance')
        return self._stdev_4

    def report(self):
        self._logger.info('salary collector result:')
        self._logger.info('>> total: {}'.format(self._value_list.__len__()))
        self._logger.info('>> lower limit: {}'.format(self.get_lower_limit()))
        # self._logger.info('>> top N: {}'.format(self.get_top_n()))
        self._logger.info('>> higher limit: {}'.format(self.get_higher_limit()))
        self._logger.info('>> mean: {}'.format(self.get_mean()))
        self._logger.info('>> stdev: {}'.format(self.get_stdev()))
        self._logger.info('>> stdev*4: {}'.format(self.get_stdev_4()))

    def __str__(self):
        # return 'salary collector result: total: {}, lower limit: {}, top N: {}, higher limit: {}, mean: {}, stdev: {}, stdev*4: {}'\
        #     .format(self._value_list.__len__(), self.get_lower_limit(), self.get_top_n(), self.get_higher_limit(), self.get_mean(), self.get_stdev(), self.get_stdev_4())
        return 'salary collector result: total: {}, lower limit: {}, higher limit: {}, mean: {}, stdev: {}, stdev*4: {}'\
            .format(self._value_list.__len__(), self.get_lower_limit(), self.get_higher_limit(), self.get_mean(), self.get_stdev(), self.get_stdev_4())

    __repr__ = __str__
