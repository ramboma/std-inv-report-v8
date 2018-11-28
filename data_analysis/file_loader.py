#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'file_loader.py'

__author__ = 'kuoren'

import pandas as pd
from data_cleansing.logging import *

logger = get_logger(__name__)


class ExcelLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    @property
    def load_data(self):
        logger.info('loading file {}'.format(self.file_path))
        xls = pd.ExcelFile(self.file_path)
        data = xls.parse()
        if data.empty:
            logger.info('loading empty file ')
            return None
        else:
            logger.info('loading file success')
            return data

    @property
    def dict_data(self):
        xls = pd.ExcelFile(self.file_path)
        data = xls.parse()
        if data.empty:
            logger.info('loading empty file ')
            return None
        else:
            config_dict = {row['subject']: row['content'] for index, row in data.iterrows()}
            logger.info('loading config file success: {}', config_dict)
            return config_dict
