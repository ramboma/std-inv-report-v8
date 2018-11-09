#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""filter_chain.py"""

__author__ = 'Gary.Z'

from data_cleansing.filter.abstract_filter import *
from data_cleansing.config import *

logger = get_logger(__name__)


class FilterChain:
    def __init__(self):
        self.__filters = []
        self.__index = 0
        # self.__interrupt = False

    # @property
    # def interrupt(self):
    #     return self.__interrupt
    #
    # @interrupt.setter
    # def interrupt(self, is_interrupt):
    #     self.__interrupt = is_interrupt
    #
    def add_filter(self, filter):
        logger.info('Add filter: {}'.format(filter.__str__()))
        self.__filters.append(filter)
        return self

    def do_filter(self, incoming, outgoing, q2c_mapping):
        # if self.__interrupt or self.__index >= self.__filters.__len__():
        if self.__index >= self.__filters.__len__():
            return
        filter = self.__filters[self.__index]
        self.__index += 1
        filter.do_filter(incoming, outgoing, self, q2c_mapping)

    def reset_state(self):
        self.__index = 0
        # self.__interrupt = False
