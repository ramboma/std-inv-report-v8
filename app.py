#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""app.py"""

__author__ = 'Gary.Z'

import click
from data_cleansing.utils import *

@clock
def run_cleansing(st, keep_unsubmitted):
    validate_data_dimensions(st)
    remove_unnecessary_headers(st)
    batch_reset_column_names(st)
    reset_emplty_values_with_na(st)

    # # Rule 1
    remove_fake_records(st)
    # # Rule 2, 3
    if keep_unsubmitted:
        remove_unqualified_records(st)
    else:
        remove_unsubmitted_records(st)
    # Rule 4
    rinse_irrelevant_answers(st)
    # # Rule 5
    rinse_nc_option_values(st)
    # # Rule 6
    rinse_invalid_answers(st)
    # # Rule 7
    rinse_unusual_salary_values(st)


@click.command()
# @click.argument('file', nargs=1)
@click.option('--input-file', '-i', required=True, help='Input raw data file path')
@click.option('--output-file', '-o', help='Output clean file path')
@click.option('--keep-unsubmitted', '-k', is_flag=True, type=bool, help='Whether keep unsubmitted records')
# @click.option('--test', '-t', type=bool, help='Only for test, DO NOT USE!!')
def main(input_file, output_file, keep_unsubmitted):
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

    print('input file: {}'.format(input_file))
    print('output file: {}'.format(output_file))
    print('keep unsubmitted records: {}'.format(keep_unsubmitted))

    # exit(0)

    print('loading input file {}'.format(input_file))
    wb = xl.load_workbook(input_file)
    st = wb.worksheets[0]

    run_cleansing(st, keep_unsubmitted)

    print('writing output file {}'.format(output_file))
    wb.save(output_file)


if __name__=='__main__':
        main()
