#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""abstract_filter.py"""

__author__ = 'Gary.Z'

from data_cleansing.config import *

# logger = get_logger(__name__)


class Filter(object):
    def __init__(self, f_id, f_title, log_handler=None):
        self._id = f_id
        self._title = f_title
        self._counter = 0
        self._debug_info = []
        self._logger = get_logger('{}${}'.format(self.__class__.__name__, id(self)))
        if log_handler is not None:
            self._logger.addHandler(log_handler)

    @property
    def logger(self):
        return self._logger

    def get_debug_info(self):
        return self._debug_info

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def counter(self):
        return self._counter

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
        raise Exception('method not implement')

    def counter_report(self):
        self._logger.info('filter {} total filter count: {}'.format(self._id, self._counter))
        if self._debug_info.__len__() > 0:
            self._logger.debug(self._debug_info)

    def __str__(self):
        return 'filter {}: {}'.format(self._id, self._title)

    __repr__ = __str__
