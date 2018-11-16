#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""filter_chain.py"""

__author__ = 'Gary.Z'

from data_cleansing.filter.abstract_filter import *
from data_cleansing.config import *

# logger = get_logger(__name__)


class FilterChain:
    def __init__(self, log_handler=None):
        self._filters = []
        self._index = 0
        self._logger = get_logger('{}${}'.format(self.__class__.__name__, id(self)))
        if log_handler is not None:
            self._logger.addHandler(log_handler)

    @property
    def logger(self):
        return self._logger

    def add_filter(self, filter):
        self._logger.info('Add filter: {}'.format(filter.__str__()))
        self._filters.append(filter)
        return self

    def do_filter(self, incoming, outgoing, q2c_mapping):
        # if self.__interrupt or self.__index >= self.__filters.__len__():
        if self._index >= self._filters.__len__():
            return
        filter = self._filters[self._index]
        self._index += 1
        filter.do_filter(incoming, outgoing, self, q2c_mapping)

    def reset_state(self):
        self._index = 0
        # self.__interrupt = False

    def counter_report(self):
        for filter in self._filters:
            filter.counter_report()
