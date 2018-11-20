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
@click.option('--batch', '-b', is_flag=True, type=bool, help='To batch generate 3 cleaned data files, include for customer public/private & analysis public/private')
@click.option('--degree', '-d', default=None, help='Specify educational background, e.g. "本科毕业生"， "专科毕业生"')
@click.option('--stream-mode', '-sm', is_flag=True, type=bool, help='Use stream mode to process data, or by default in memory')
@click.option('--concurrent-mode', '-cm', is_flag=True, type=bool, help='Use multi-process to process data, or by default in serial')
@click.option('--chinese-naming', '-cn', is_flag=True, type=bool, help='Use chinese naming file name')
@click.option('--trace-mode', '-t', is_flag=True, type=bool, help='Trace mode will add additional comments for each rinsed cell')
def main(input_file, output_folder, analysis, internal, batch, degree, stream_mode, concurrent_mode, chinese_naming, trace_mode):
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

    if stream_mode is None:
        stream_mode = False

    if concurrent_mode is None:
        concurrent_mode = False

    if chinese_naming is None:
        chinese_naming = False

    tag = time.strftime('%Y%m%d%H%M%S', time.localtime())

    setting_groups = []
    if not batch:
        setting_groups.append(
            {
                'input_file': input_file,
                'output_file': get_output_filename(dirpath, name, ext, internal, analysis, tag, degree, chinese_naming),
                'internal': internal, 'analysis': analysis,
                'tag': tag, 'trace_mode': trace_mode, 'degree': degree,
             }
        )
        # run_serial(setting_groups, stream_mode)
    else:
        setting_groups.extend([
            # internal, analysis
            {
                'input_file': input_file,
                'output_file': get_output_filename(dirpath, name, ext, True, True, tag, degree, chinese_naming),
                'internal': True, 'analysis': True,
                'tag': tag, 'trace_mode': trace_mode, 'degree': degree,
            },
            # internal, customer
            {
                'input_file': input_file,
                'output_file': get_output_filename(dirpath, name, ext, True, False, tag, degree, chinese_naming),
                'internal': True, 'analysis': False,
                'tag': tag, 'trace_mode': trace_mode, 'degree': degree,
            },
            # public, analysis
            {
                'input_file': input_file,
                'output_file': get_output_filename(dirpath, name, ext, False, True, tag, degree, chinese_naming),
                'internal': False, 'analysis': True,
                'tag': tag, 'trace_mode': trace_mode, 'degree': degree,
            },
            # public, customer
            {
                'input_file': input_file,
                'output_file': get_output_filename(dirpath, name, ext, False, False, tag, degree, chinese_naming),
                'internal': False, 'analysis': False,
                'tag': tag, 'trace_mode': trace_mode, 'degree': degree,
            },
        ])
    if concurrent_mode:
        run_concurrent(setting_groups, stream_mode)
    else:
        run_serial(setting_groups, stream_mode)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e, exc_info=True)
        # logger.error(e)
    finally:
        pass
