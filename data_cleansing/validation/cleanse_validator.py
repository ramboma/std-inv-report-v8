#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cleanse_filter.py"""

__author__ = 'Gary.Z'

from data_cleansing.validation.abstract_validator import *

logger = get_logger(__name__)


class DataDimensionValidator(Validator):
    def __init__(self, expect_cols=231, expect_rows=3):
        super().__init__('data-dimension', 'data dimension checking: row >=3 and col >= 231')
        self._expect_cols = expect_cols
        self._expect_rows = expect_rows

    def do_validate(self, obj):
        """data dimension checking: row >=3 and col >= 231 """
        work_sheet = obj
        self._logger.info('validating data dimensions, cols: {}, rows: {}'.format(work_sheet.max_column, work_sheet.max_row))
        if work_sheet.max_column < self._expect_cols:
            raise Exception("column count must >= {}".format(self._expect_cols))
        if work_sheet.max_row < 3:
            raise Exception("row count must >= {}".format(self._expect_rows))
