#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""abstract_filter.py"""

__author__ = 'Gary.Z'


class Filter(object):
    def __init__(self, id, title):
        self._id = id
        self._title = title

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    def do_filter(self, incoming, outgoing, chain, q2c_mapping):
            raise Exception('method not implement')

    def __str__(self):
        return 'filter {}: {}'.format(self._id, self._title)

    __repr__ = __str__
