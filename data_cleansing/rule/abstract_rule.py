#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""abstract_rule.py"""

__author__ = 'Gary.Z'


class CleanseRule(object):
    def __init__(self, id, title):
        self.__id = id
        self.__title = title

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    def apply(self, work_sheet, question_column_mapping):
        raise Exception('method not implement')

    def __str__(self):
        return 'rule {}: {}'.format(self.__id, self.__title)

    __repr__ = __str__
