#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""logging.py"""

__author__ = 'Gary.Z'

import logging


def get_logger(name, file='runlog.txt'):
    # formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')
    # formatter = logging.Formatter('%(asctime)s %(name)s %(thread)d(%(threadName)s) %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s %(name)s %(process)d(%(processName)s) %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(file, mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
