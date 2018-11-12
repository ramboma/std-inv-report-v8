#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'cleaned_loader.py'

__author__ = 'kuoren'

import data_analysis.read_excel_util as excelUtil
from data_cleansing.logging import *

logger = get_logger(__name__)


class CleanedLoader:
    def __init__(self, cleaned_path):
        self.cleaned_path = cleaned_path

    @property
    def cleaned_data(self):
        logger.info('loading cleaned file {}'.format(self.cleaned_path))
        data = excelUtil.read_excel(self.cleaned_path)
        if data.empty:
            logger.info('loading cleaned file fails: empty')
            return None
        else:
            logger.info('loading cleaned file success')
            return data
