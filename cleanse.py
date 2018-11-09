#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""cleanse.py"""

__author__ = 'Gary.Z'

import time
import click

from data_cleansing.cleanser_runner import *

logger = get_logger(__name__)


@click.command()
# @click.argument('file', nargs=1)
@click.option('--input-file', '-i', required=True, help='Input file path')
@click.option('--output-folder', '-o', help='Output folder path')
@click.option('--analysis', '-s', is_flag=True, type=bool, help='For analysis, if no: for customer')
@click.option('--internal', '-l', is_flag=True, type=bool, help='For internal, if no: for public')
@click.option('--all', '-a', is_flag=True, type=bool, help='To batch generate 3 cleaned data files, include for customer public/private & analysis public/private')
@click.option('--degree', '-d', default=None, help='Specify educational background, e.g. "本科毕业生"， "专科毕业生"')
@click.option('--trace-mode', '-t', is_flag=True, type=bool, help='Trace mode will add additional comments for each rinsed cell')
@click.option('--multi-thread', '-m', is_flag=True, type=bool, help='multi-thread mode, only make effect with -a')
def main(input_file, output_folder, analysis, internal, all, degree, trace_mode, multi_thread):
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

    if multi_thread is None:
        multi_thread = False

    tag = time.strftime('%Y%m%d%H%M%S', time.localtime())

    setting_groups = []
    if not all:
        setting_groups.append(
            {'internal': internal, 'analysis': analysis, 'output_file': get_output_filename(dirpath, name, ext, internal, analysis, tag, degree)}
        )
    else:
        setting_groups.extend([
            # internal, analysis
            {'internal': True, 'analysis': True, 'output_file': get_output_filename(dirpath, name, ext, True, True, tag, degree)},
            # internal, customer
            {'internal': True, 'analysis': False, 'output_file': get_output_filename(dirpath, name, ext, True, False, tag, degree)},
            # public, analysis
            {'internal': False, 'analysis': True, 'output_file': get_output_filename(dirpath, name, ext, False, True, tag, degree)},
            # public, customer
            {'internal': False, 'analysis': False, 'output_file': get_output_filename(dirpath, name, ext, False, False, tag, degree)},
        ])

    if multi_thread:
        run_multi_thread(input_file, degree, tag, setting_groups, trace_mode)
    else:
        run_single_thread(input_file, degree, tag, setting_groups, trace_mode)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e, exc_info=True)
        # logger.error(e)
    finally:
        pass
