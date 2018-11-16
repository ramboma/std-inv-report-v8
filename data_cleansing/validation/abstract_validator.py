#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""abstract_filter.py"""

__author__ = 'Gary.Z'

from data_cleansing.config import *

logger = get_logger(__name__)


class Validator(object):
    def __init__(self, v_id, v_title, log_handler=None):
        self._id = v_id
        self._title = v_title
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

    def do_validate(self, obj):
        raise Exception('method not implement')

    def __str__(self):
        return 'validator {}: {}'.format(self._id, self._title)

    __repr__ = __str__
