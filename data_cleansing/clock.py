#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""clock.py"""

__author__ = 'Gary.Z'

import timeit


def clocking(func):
    def clocked(*args):
        t0 = timeit.default_timer()
        result = func(*args)
        elapsed = timeit.default_timer() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        # print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        print('=> [%0.2fs]' % elapsed)
        return result
    return clocked


