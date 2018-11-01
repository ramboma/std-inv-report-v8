#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""clock.py"""

__author__ = 'Gary.Z'

import timeit

from data_cleansing.config import *

logger = get_logger(__name__)


def clocking(func):
    def clocked(*args, **kw):
        t0 = timeit.default_timer()
        result = func(*args, **kw)
        elapsed = timeit.default_timer() - t0
        # name = func.__name__
        # arg_str = ', '.join(repr(arg) for arg in args)
        # print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        logger.info('=> time cost: [%0.2fs]' % elapsed)
        return result
    return clocked


