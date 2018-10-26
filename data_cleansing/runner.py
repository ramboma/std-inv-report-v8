#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""runner.py"""

__author__ = 'Gary.Z'

from data_cleansing.utils import *


@clocking
def run_cleansing(input_file, output_file, keep_unsubmitted, v6_compatible, trace_mode):

    if keep_unsubmitted is None:
        keep_unsubmitted = False

    print('')
    print('############################## Cleansing start ##################################')
    print('input file: {}'.format(input_file))
    print('output file: {}'.format(output_file))
    print('keep un-submitted records: {}'.format(keep_unsubmitted))
    print('enable v6 compatible : {}'.format(v6_compatible))
    print('#################################################################################')
    print('')

    print('loading input file {}'.format(input_file))
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
    if keep_unsubmitted:
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
    if v6_compatible:
        cleaner.rinse_irrelevant_answers(RINSE_RULE_IRRELEVANT_QUESTIONS_V6_COMPATIBLE, '8')

    print('writing output file {}'.format(output_file))
    wb.save(output_file)

    print('')
    print('############################## Cleansing end ##################################')
    print('')

    return


