#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""runner.py"""

__author__ = 'Gary.Z'

import os

from data_cleansing.data_cleanser import *
from data_cleansing.rule.rules_assembler import *

logger = get_logger(__name__)


@clocking
def run_cleansing(input_file, output_file, sheet_tag, degree=False, with_rule_2_2=False, with_rule_7=False, trace_mode=False):

    logger.info('')
    logger.info('############################## Cleansing start ##################################')
    logger.info('input file: \'{}\''.format(input_file))
    logger.info('output file: \'{}\''.format(output_file))
    logger.info('with rule 2.2: {}'.format(with_rule_2_2))
    logger.info('with rule 8: {}'.format(with_rule_7))
    logger.info('trace mode: {}'.format(trace_mode))
    logger.info('#################################################################################')
    logger.info('')

    logger.info('loading input file \'{}\''.format(input_file))
    wb = xl.load_workbook(input_file)
    st = wb.worksheets[0]

    cleanser = DataCleanser(st)
    cleanser.trace_mode = trace_mode

    cleanser.validate_data_dimensions()
    cleanser.remove_unnecessary_headers()
    cleanser.reset_column_names()
    cleanser.reset_emplty_values_with_na()

    if degree is not None:
        cleanser.filter_records_with_degree(degree)

    rule_set_assembler = RuleSetAssembler()
    rule_ids = ['1', '2.1']
    if with_rule_2_2:
        rule_ids.append('2.2')
    rule_ids.extend(['3', '4', '5', '6'])
    if with_rule_7:
        rule_ids.append('7')
    rule_set = rule_set_assembler.assemble(rule_ids)

    cleanser.apply_rule_set(rule_set)
    cleanser.validate_data_dimensions()

    cleanser.set_sheet_name('cleaned_{}'.format(sheet_tag))

    logger.info('writing output file {}'.format(output_file))
    wb.save(output_file)

    logger.info('')
    logger.info('############################## Cleansing end ##################################')
    logger.info('')

    return


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

