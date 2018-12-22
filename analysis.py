#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""analysis.py"""

__author__ = 'Gary.Z'

import os
import click
import time

from data_cleansing.logging import *
from data_analysis.data_analyze import *

logger = get_logger(__name__)


@click.command()
# @click.argument('file', nargs=1)
@click.option('--input-file', '-i', required=True, help='Input file path')
@click.option('--output-folder', '-o', help='Output folder path')
@click.option('--config', '-c', help='Config file path')
def main(input_file, output_folder, config):
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
        filename = os.path.basename(input_file)
        name, ext = os.path.splitext(filename)

    tag = time.strftime('%Y%m%d%H%M%S', time.localtime())
    output_path = os.path.join(dirpath, '{}_analysis_{}'.format(name, tag))
    os.mkdir(output_path)

    if config is None or config == '':
        config = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'data_analysis/config.xlsx')

    # call report generator class here
    do_reports(input_file, output_path, config)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e, exc_info=True)
        # logger.error(e)
    finally:
        pass
