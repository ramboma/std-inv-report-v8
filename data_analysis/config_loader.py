#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'config_loader.py'

__author__ = 'kuoren'

import data_analysis.read_excel_util as excelUtil
from data_cleansing.logging import *

logger = get_logger(__name__)


class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path

    @property
    def config_dict(self):
        logger.info('loading config file {}'.format(self.config_path))
        data = excelUtil.read_excel(self.config_path)
        if data.empty:
            logger.info('loading config file fails: empty')
            return None
        else:
            config_dict = {row['subject']: row['content'] for index, row in data.iterrows()}
            logger.info('loading config file success: {}',config_dict)
            return config_dict
