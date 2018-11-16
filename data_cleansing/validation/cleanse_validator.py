#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cleanse_filter.py"""

__author__ = 'Gary.Z'

import re

from data_cleansing.validation.abstract_validator import *

# logger = get_logger(__name__)


class DataDimensionValidator(Validator):
    def __init__(self, expect_cols=231, expect_rows=3, log_handler=None):
        super().__init__('data-dimension', 'data dimension checking: row >=3 and col >= 231', log_handler)
        self._expect_cols = expect_cols
        self._expect_rows = expect_rows

    def do_validate(self, obj):
        """data dimension checking: row >=3 and col >= 231 """
        cols = obj[0]
        rows = obj[1]
        self._logger.info('validating data dimensions, cols: {}, rows: {}'.format(cols, rows))
        if cols <= 1 and rows <= 1:
            raise Exception('only 1 cell detected, consider not supported excel file format, version must be >= Excel 2010')
        if cols < self._expect_cols:
            raise Exception("column count must >= {}".format(self._expect_cols))
        if rows < 3:
            raise Exception("row count must >= {}".format(self._expect_rows))


class QuestionIdHeaderValidator(Validator):
    def __init__(self, id_pattern=r'(?P<prefix>([A-Z0-9]+)(-[0-9]+)*)(-[A-Z]+)?', log_handler=None):
        super().__init__('question-id-header', 'check if question ids in header', log_handler)
        self._id_pattern = id_pattern

    def do_validate(self, obj):
        values = obj
        for value in values:
            if value is None or value == '':
                continue
            matches = re.match(self._id_pattern, value)
            if matches is None:
                raise Exception('invalid question id: {}, consider missing question id header'.format(value))
