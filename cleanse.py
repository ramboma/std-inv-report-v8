#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""cleanse.py"""

__author__ = 'Gary.Z'

import os
import click

# from data_cleansing.config import *
from data_cleansing.utils import *


@clocking
def run_cleansing(st, keep_unsubmitted, v6_compatible, trace_mode):

    cleaner = DataCleanser(st)
    cleaner.set_trace_mode(trace_mode)

    cleaner.validate_data_dimensions()
    cleaner.remove_unnecessary_headers()
    cleaner.scan_reset_column_names()
    cleaner.reset_emplty_values_with_na()
    # clear_all_cells_bgcolor()

    # # Rule 1
    cleaner.remove_fake_records()
    # # Rule 2, 3
    if keep_unsubmitted:
        cleaner.remove_unqualified_records()
    else:
        cleaner.remove_unsubmitted_records()
    # Rule 4
    cleaner.rinse_irrelevant_answers(RINSE_RULE_IRRELEVANT_QUESTIONS, '4')
    # # Rule 5
    cleaner.rinse_nc_option_values()
    # # Rule 6
    cleaner.rinse_invalid_answers()
    # # Rule 7
    cleaner.rinse_unusual_salary_values()
    # Rule 8
    if v6_compatible:
        cleaner.rinse_irrelevant_answers(RINSE_RULE_IRRELEVANT_QUESTIONS_V6_COMPATIBLE, '8')
    return st


@click.command()
# @click.argument('file', nargs=1)
@click.option('--input-file', '-i', required=True, help='Input raw data file path')
@click.option('--output-file', '-o', help='Output clean file path')
@click.option('--keep-unsubmitted', '-k', is_flag=True, type=bool, help='Keep unsubmitted records')
@click.option('--v6-compatible', '-6', is_flag=True, type=bool, help='Rinse "自由职业" records to compatible with v6')
@click.option('--trace-mode', '-t', is_flag=True, type=bool, help='Trace mode will add additional comments for each rinsed cell')
def main(input_file, output_file, keep_unsubmitted, v6_compatible, trace_mode):
    """This script cleansing raw data into cleaned data."""

    if not os.path.exists(input_file):
        print('input file [{}] not exist, quit'.format(input_file))
        exit(0)

    if output_file is None:
        dirpath, filename = os.path.split(input_file)
        name, ext = os.path.splitext(filename)
        output_file = os.path.join(dirpath, '{}{}{}'.format(name, '_cleaned', ext))
    else:
        if os.path.isdir(output_file):
            dirpath = output_file
        else:
            dirpath, filename = os.path.split(output_file)
            name, ext = os.path.splitext(output_file)
            if ext != '.xlsx':
                print('output file extension must be .xlsx, quit')
                exit(0)
        if not os.path.exists(dirpath):
            print('output dir [{}] not exist, quit'.format(dirpath))
            exit(0)
        if os.path.isdir(output_file):
            filename = os.path.basename(input_file)
            name, ext = os.path.splitext(filename)
            output_file = os.path.join(dirpath, '{}{}{}'.format(name, '_cleaned', '.xlsx'))

    if keep_unsubmitted is None:
        keep_unsubmitted = False

    if trace_mode is None:
        trace_mode = False

    if trace_mode:
        print('** TRACING MODE ENABLED **')

    print('input file: {}'.format(input_file))
    print('output file: {}'.format(output_file))
    print('keep unsubmitted records: {}'.format(keep_unsubmitted))

    print('loading input file {}'.format(input_file))
    wb = xl.load_workbook(input_file)
    st = wb.worksheets[0]

    st = run_cleansing(st, keep_unsubmitted, v6_compatible, trace_mode)

    print('writing output file {}'.format(output_file))
    wb.save(output_file)


if __name__ == '__main__':
        main()
