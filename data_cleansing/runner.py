#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""runner.py"""

__author__ = 'Gary.Z'

import os
# import threading

from data_cleansing.data_cleanser import *
from data_cleansing.rule.rules_assembler import *

logger = get_logger(__name__)


# class CleansingBackgroundExecutor(threading.Thread):
#     def __init__(self, input_file, output_file, thread_name=None):
#         threading.Thread.__init__(self)
#         self.setDaemon(True)
#         if thread_name is not None:
#             self.setName(thread_name)
class CleansingBackgroundExecutor:
    def __init__(self, input_file, output_file):
        self.__input_file = input_file
        self.__output_file = output_file
        self.__degree_filter = None
        self.__with_rule_2_2 = False
        self.__with_rule_7 = False
        self.__sheet_tag = None
        self.__trace_mode = False

    @property
    def with_rule_2_2(self):
        return self.__with_rule_2_2

    @with_rule_2_2.setter
    def with_rule_2_2(self, with_rule_2_2):
        self.__with_rule_2_2 = with_rule_2_2

    @property
    def with_rule_7(self):
        return self.__with_rule_7

    @with_rule_7.setter
    def with_rule_7(self, with_rule_7):
        self.__with_rule_7 = with_rule_7

    @property
    def trace_mode(self):
        return self.__trace_mode

    @trace_mode.setter
    def trace_mode(self, trace_mode):
        self.__trace_mode = trace_mode

    @property
    def degree_filter(self):
        return self.__degree_filter

    @degree_filter.setter
    def degree_filter(self, degree_filter):
        self.__degree_filter = degree_filter

    @property
    def sheet_tag(self):
        return self.__sheet_tag

    @sheet_tag.setter
    def sheet_tag(self, sheet_tag):
        self.__sheet_tag = sheet_tag

    @clocking
    def run(self):
        logger.info('')
        logger.info('############################## Cleansing start ##################################')
        logger.info('input file: \'{}\''.format(self.__input_file))
        logger.info('output file: \'{}\''.format(self.__output_file))
        if self.__degree_filter is not None:
            logger.info('with degree filter: {}'.format(self.degree_filter))
        logger.info('with rule 2.2: {}'.format(self.__with_rule_2_2))
        logger.info('with rule 8: {}'.format(self.__with_rule_7))
        logger.info('trace mode: {}'.format(self.__trace_mode))
        logger.info('#################################################################################')
        logger.info('')

        logger.info('loading input file \'{}\''.format(self.__input_file))
        wb = xl.load_workbook(self.__input_file)
        st = wb.worksheets[0]

        cleanser = DataCleanser(st)
        cleanser.trace_mode = self.__trace_mode

        cleanser.validate_data_dimensions()
        cleanser.remove_unnecessary_headers()
        cleanser.reset_column_names()
        cleanser.reset_emplty_values_with_na()

        if self.__degree_filter is not None:
            cleanser.filter_records_with_degree(self.__degree_filter)

        rule_set_assembler = RuleSetAssembler()
        rule_ids = ['1', '2.1']
        if self.__with_rule_2_2:
            rule_ids.append('2.2')
        rule_ids.extend(['3', '4', '5', '6'])
        if self.__with_rule_7:
            rule_ids.append('7')
        rule_set = rule_set_assembler.assemble(rule_ids)

        cleanser.apply_rule_set(rule_set)
        cleanser.validate_data_dimensions()

        if self.__sheet_tag is not None:
            cleanser.set_sheet_name('cleaned_{}'.format(self.__sheet_tag))
        else:
            cleanser.set_sheet_name('cleaned')

        logger.info('writing output file {}'.format(self.__output_file))
        wb.save(self.__output_file)

        logger.info('')
        logger.info('############################## Cleansing end ##################################')
        logger.info('')

        return


@clocking
def run(input_file, degree, tag, setting_groups, trace_mode):
    for setting in setting_groups:
        # thread_name = get_thread_name(setting['internal'], setting['analysis'])
        executor = CleansingBackgroundExecutor(input_file, setting['output_file'])
        if degree is not None:
            executor.degree_filter = degree
        executor.with_rule_2_2 = setting['internal']
        executor.with_rule_7 = setting['analysis']
        executor.sheet_tag = tag
        executor.trace_mode = trace_mode
        executor.run()


# @clocking
# def run_cleansing(input_file, output_file, degree=False, with_rule_2_2=False, with_rule_7=False, sheet_tag=None, trace_mode=False):
#
#     logger.info('')
#     logger.info('############################## Cleansing start ##################################')
#     logger.info('input file: \'{}\''.format(input_file))
#     logger.info('output file: \'{}\''.format(output_file))
#     logger.info('with rule 2.2: {}'.format(with_rule_2_2))
#     logger.info('with rule 8: {}'.format(with_rule_7))
#     logger.info('trace mode: {}'.format(trace_mode))
#     logger.info('#################################################################################')
#     logger.info('')
#
#     logger.info('loading input file \'{}\''.format(input_file))
#     wb = xl.load_workbook(input_file)
#     st = wb.worksheets[0]
#
#     cleanser = DataCleanser(st)
#     cleanser.trace_mode = trace_mode
#
#     cleanser.validate_data_dimensions()
#     cleanser.remove_unnecessary_headers()
#     cleanser.reset_column_names()
#     cleanser.reset_emplty_values_with_na()
#
#     if degree is not None and isinstance(degree, str):
#         cleanser.filter_records_with_degree(degree)
#
#     rule_set_assembler = RuleSetAssembler()
#     rule_ids = ['1', '2.1']
#     if with_rule_2_2:
#         rule_ids.append('2.2')
#     rule_ids.extend(['3', '4', '5', '6'])
#     if with_rule_7:
#         rule_ids.append('7')
#     rule_set = rule_set_assembler.assemble(rule_ids)
#
#     cleanser.apply_rule_set(rule_set)
#     cleanser.validate_data_dimensions()
#
#     if sheet_tag is not None:
#         cleanser.set_sheet_name('cleaned_{}'.format(sheet_tag))
#     else:
#         cleanser.set_sheet_name('cleaned')
#
#     logger.info('writing output file {}'.format(output_file))
#     wb.save(output_file)
#
#     logger.info('')
#     logger.info('############################## Cleansing end ##################################')
#     logger.info('')
#
#     return


def get_output_filename(dirpath, name, ext,  internal, analysis, tag, degree=None):
    if internal:
        target = 'internal'
    else:
        target = 'public'
    if analysis:
        scope = 'analysis'
    else:
        scope = 'customer'

    if degree is None:
        return os.path.join(dirpath, '{}_cleaned_{}_{}_{}{}'.format(name, target, scope, tag, ext))
    else:
        return os.path.join(dirpath, '{}_cleaned_{}_{}_{}_{}{}'.format(name, degree, target, scope, tag, ext))


def get_thread_name(internal, analysis):
    if internal:
        target = 'internal'
    else:
        target = 'public'
    if analysis:
        scope = 'analysis'
    else:
        scope = 'customer'

    return os.path.join('{}-{}'.format(target, scope))

