#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""logging.py"""

__author__ = 'Gary.Z'

import logging
from logging.handlers import TimedRotatingFileHandler

# formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')
# formatter = logging.Formatter('%(asctime)s %(name)s %(thread)d(%(threadName)s) %(levelname)s - %(message)s')
DEFAULT_LOG_FORMAT = '%(asctime)s %(name)s %(processName)s-%(process)d %(levelname)s - %(message)s'


def get_log_formatter(log_format=DEFAULT_LOG_FORMAT):
    return logging.Formatter(log_format)


def get_logger(name, file='runlog.txt', level=logging.DEBUG):

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = get_log_formatter()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = get_file_log_handler(file, level, formatter)
    logger.addHandler(file_handler)

    return logger


def get_file_log_handler(path, level=logging.INFO, log_formatter=get_log_formatter()):
    file_handler = logging.FileHandler(path, 'a', encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(log_formatter)
    return file_handler


def get_rotate_file_log_handler(path, level=logging.INFO, log_formatter=get_log_formatter()):
    file_handler = TimedRotatingFileHandler(path, when='M', interval=1, backupCount=7, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(log_formatter)
    return file_handler


# def get_process_log_file():
#     dirpath, filename = os.path.split(self._output_file)
#     name, ext = os.path.splitext(filename)
#     return os.path.join(dirpath, '{}_runlog.txt'.format(name))


