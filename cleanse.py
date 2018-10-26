#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""cleanse.py"""

__author__ = 'Gary.Z'

import os
import click

from data_cleansing.runner import *


@click.command()
# @click.argument('file', nargs=1)
@click.option('--input-file', '-i', required=True, help='Input file path')
@click.option('--output-folder', '-o', help='Output folder path')
@click.option('--keep-unsubmitted', '-k', is_flag=True, type=bool, help='Keep unsubmitted records')
@click.option('--v6-compatible', '-6', is_flag=True, type=bool, help='Rinse "自由职业" records to compatible with v6')
@click.option('--all', '-a', is_flag=True, type=bool, help='To batch generate 3 cleaned data files, include for customer public/private & analysis public/private')
@click.option('--trace-mode', '-t', is_flag=True, type=bool, help='Trace mode will add additional comments for each rinsed cell')
def main(input_file, output_folder, keep_unsubmitted, v6_compatible, all, trace_mode):
    """This script cleansing raw data into cleaned data."""

    if not os.path.exists(input_file):
        print('input file [{}] not exist, quit'.format(input_file))
        exit(0)

    if output_folder is None:
        dirpath, filename = os.path.split(input_file)
        name, ext = os.path.splitext(filename)
    else:
        if not os.path.exists(output_folder):
            print('output path [{}] not exist, quit'.format(output_folder))
            exit(0)
        if not os.path.isdir(output_folder):
            print('output path [{}] is not dir, quit'.format(output_folder))
            exit(0)

        dirpath = output_folder
        ext = '.xlsx'
        filename = os.path.basename(input_file)
        name, ext = os.path.splitext(filename)

    output_file = os.path.join(dirpath, '{}{}{}'.format(name, '_cleaned', ext))
    output_file_customer_public = os.path.join(dirpath, '{}{}{}'.format(name, '_cleaned_customer_public', ext))
    output_file_customer_private = os.path.join(dirpath, '{}{}{}'.format(name, '_cleaned_customer_private', ext))
    output_file_analysis_public = os.path.join(dirpath, '{}{}{}'.format(name, '_cleaned_analysis_public', ext))
    output_file_analysis_private = os.path.join(dirpath, '{}{}{}'.format(name, '_cleaned_analysis_private', ext))

    if trace_mode is None:
        trace_mode = False

    if trace_mode:
        print('** TRACING MODE ENABLED **')

    if not all:
        run_cleansing(input_file, output_file, keep_unsubmitted, v6_compatible, trace_mode)
    else:
        run_cleansing(input_file, output_file_analysis_private, keep_unsubmitted=False, v6_compatible=True, trace_mode=trace_mode)
        run_cleansing(input_file, output_file_customer_private, keep_unsubmitted=False, v6_compatible=False, trace_mode=trace_mode)
        run_cleansing(input_file, output_file_analysis_public, keep_unsubmitted=True, v6_compatible=True, trace_mode=trace_mode)
        run_cleansing(input_file, output_file_customer_public, keep_unsubmitted=True, v6_compatible=False,  trace_mode=trace_mode)


if __name__ == '__main__':
        main()

