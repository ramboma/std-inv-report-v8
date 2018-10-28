#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""cleanse.py"""

__author__ = 'Gary.Z'

import os
import click

from data_cleansing.runner import *

logger = get_logger(__name__)


@click.command()
# @click.argument('file', nargs=1)
@click.option('--input-file', '-i', required=True, help='Input file path')
@click.option('--output-folder', '-o', help='Output folder path')
@click.option('--customer', '-c', is_flag=True, type=bool, help='for customer, if no: for analysis')
@click.option('--external', '-e', is_flag=True, type=bool, help='for external, if no: for internal')
@click.option('--all', '-a', is_flag=True, type=bool, help='To batch generate 3 cleaned data files, include for customer public/private & analysis public/private')
@click.option('--trace-mode', '-t', is_flag=True, type=bool, help='Trace mode will add additional comments for each rinsed cell')
def main(input_file, output_folder, customer, external, all, trace_mode):
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

    output_file = os.path.join(dirpath, '{}{}{}'.format(name, '_cleaned', ext))
    output_file_customer_public = os.path.join(dirpath, '{}{}{}'.format(name, '_cleaned_customer_public', ext))
    output_file_customer_internal = os.path.join(dirpath, '{}{}{}'.format(name, '_cleaned_customer_private', ext))
    output_file_analysis_public = os.path.join(dirpath, '{}{}{}'.format(name, '_cleaned_analysis_public', ext))
    output_file_analysis_internal = os.path.join(dirpath, '{}{}{}'.format(name, '_cleaned_analysis_private', ext))

    if customer is None:
        customer = False
    if external is None:
        external = False

    if trace_mode is None:
        trace_mode = False

    if trace_mode:
        logger.info('** TRACING MODE ENABLED **')

    if not all:
        run_cleansing(input_file, output_file, with_rule_2_2=not external, with_rule_8=not customer, trace_mode=trace_mode)
    else:
        run_cleansing(input_file, output_file_analysis_internal, with_rule_2_2=False, with_rule_8=True, trace_mode=trace_mode)
        run_cleansing(input_file, output_file_customer_internal, with_rule_2_2=False, with_rule_8=False, trace_mode=trace_mode)
        run_cleansing(input_file, output_file_analysis_public, with_rule_2_2=True, with_rule_8=True, trace_mode=trace_mode)
        run_cleansing(input_file, output_file_customer_public, with_rule_2_2=True, with_rule_8=False, trace_mode=trace_mode)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e, exc_info=True)
    finally:
        pass
