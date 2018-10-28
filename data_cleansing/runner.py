#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""runner.py"""

__author__ = 'Gary.Z'

from data_cleansing.utils import *

logger = get_logger(__name__)


@clocking
def run_cleansing(input_file, output_file, with_rule_2_2, with_rule_8, trace_mode):

    logger.info('')
    logger.info('############################## Cleansing start ##################################')
    logger.info('input file: {}'.format(input_file))
    logger.info('output file: {}'.format(output_file))
    logger.info('remove un-submitted records: {}'.format(with_rule_2_2))
    logger.info('rinse by rule 7: {}'.format(with_rule_8))
    logger.info('#################################################################################')
    logger.info('')

    logger.info('loading input file {}'.format(input_file))
    wb = xl.load_workbook(input_file)
    st = wb.worksheets[0]

    cleaner = DataCleanser(st)
    cleaner.set_trace_mode(trace_mode)

    cleaner.validate_data_dimensions()
    cleaner.remove_unnecessary_headers()
    cleaner.scan_reset_column_names()
    cleaner.reset_emplty_values_with_na()
    # clear_all_cells_bgcolor()

    # Rule 1
    cleaner.remove_fake_records()
    # Rule 2.1
    cleaner.remove_unqualified_records()
    if with_rule_2_2:
        # Rule 2.2
        cleaner.remove_unsubmitted_records()
    # Rule 4
    cleaner.rinse_irrelevant_answers(RINSE_RULE_IRRELEVANT_QUESTIONS, '4')
    # Rule 5
    cleaner.rinse_nc_option_values()
    # Rule 6
    cleaner.rinse_invalid_answers()
    # Rule 7
    cleaner.rinse_unusual_salary_values()
    # Rule 8
    if with_rule_8:
        cleaner.rinse_irrelevant_answers(RINSE_RULE_IRRELEVANT_QUESTIONS_V6_COMPATIBLE, '8')

    logger.info('writing output file {}'.format(output_file))
    wb.save(output_file)

    logger.info('')
    logger.info('############################## Cleansing end ##################################')
    logger.info('')

    return


