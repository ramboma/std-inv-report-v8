#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""cleanse.py"""

__author__ = 'Gary.Z'

import time
import click

from data_cleansing.runner import *

logger = get_logger(__name__)


@click.command()
# @click.argument('file', nargs=1)
@click.option('--input-file', '-i', required=True, help='Input file path')
@click.option('--output-folder', '-o', help='Output folder path')
@click.option('--analysis', '-s', is_flag=True, type=bool, help='for analysis, if no: for customer')
@click.option('--internal', '-l', is_flag=True, type=bool, help='for internal, if no: for public')
@click.option('--all', '-a', is_flag=True, type=bool, help='To batch generate 3 cleaned data files, include for customer public/private & analysis public/private')
@click.option('--trace-mode', '-t', is_flag=True, type=bool, help='Trace mode will add additional comments for each rinsed cell')
def main(input_file, output_folder, analysis, internal, all, trace_mode):
    """This script cleansing raw data into cleaned data."""

    if not os.path.exists(input_file):
        logger.error('input file [{}] not exist, quit'.format(input_file))
        exit(0)

    if output_folder is None:
        dirpath, filename = os.path.split(input_file)
        name, ext = os.path.splitext(filename)
    else:
        if not os.path.exists(output_folder):
            logger.error('output path [{}] not exist, quit'.format(output_folder))
            exit(0)
        if not os.path.isdir(output_folder):
            logger.error('output path [{}] is not dir, quit'.format(output_folder))
            exit(0)

        dirpath = output_folder
        ext = '.xlsx'
        filename = os.path.basename(input_file)
        name, ext = os.path.splitext(filename)

    if analysis is None:
        analysis = False
    if internal is None:
        internal = False

    if trace_mode is None:
        trace_mode = False

    tag = time.strftime('%Y%m%d%H%M%S', time.localtime())

    if not all:
        output_file = get_output_filename(dirpath, name, ext, internal, analysis, tag)
        run_cleansing(input_file, output_file, sheet_tag=tag, with_rule_2_2=internal, with_rule_8=analysis, trace_mode=trace_mode)
    else:
        # internal, analysis
        output_file = get_output_filename(dirpath, name, ext, internal=True, analysis=True, tag=tag)
        run_cleansing(input_file, output_file, sheet_tag=tag, with_rule_2_2=True, with_rule_8=True, trace_mode=trace_mode)
        # internal, customer
        output_file = get_output_filename(dirpath, name, ext, internal=True, analysis=False, tag=tag)
        run_cleansing(input_file, output_file, sheet_tag=tag, with_rule_2_2=True, with_rule_8=False, trace_mode=trace_mode)
        # public, analysis
        output_file = get_output_filename(dirpath, name, ext, internal=False, analysis=True, tag=tag)
        run_cleansing(input_file, output_file, sheet_tag=tag, with_rule_2_2=False, with_rule_8=True, trace_mode=trace_mode)
        # public, customer
        output_file = get_output_filename(dirpath, name, ext, internal=False, analysis=False, tag=tag)
        run_cleansing(input_file, output_file, sheet_tag=tag, with_rule_2_2=False, with_rule_8=False, trace_mode=trace_mode)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e, exc_info=True)
    finally:
        pass
