#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""cleanse.py"""

__author__ = 'Gary.Z'

import os
import click
import time
# import sys
# import logging
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from data_cleansing.runner import *


class InputFileMatchingEventHandler(FileSystemEventHandler):

    def __init__(self, batch_cleansing_handler, output_folder, trace_mode):
        super().__init__()

        self.__batch_cleansing_handler = batch_cleansing_handler;
        self.__output_folder = output_folder
        self.__trace_mode = trace_mode

    def on_moved(self, event):
        # super(LoggingEventHandler, self).on_moved(event)
        #
        # what = 'directory' if event.is_directory else 'file'
        # logging.info("Moved %s: from %s to %s", what, event.src_path,
        #              event.dest_path)
        pass

    def on_created(self, event):
        # super(LoggingEventHandler, self).on_created(event)
        #
        # what = 'directory' if event.is_directory else 'file'
        # logging.info("Created %s: %s", what, event.src_path)
        filename = os.path.basename(event.src_path)
        name, ext = os.path.splitext(filename)
        if ext == '.xlsx':
            print('input file {} detected'.format(event.src_path))
            self.__batch_cleansing_handler(event.src_path, self.__output_folder, self.__trace_mode)
        pass

    def on_deleted(self, event):
        # super(LoggingEventHandler, self).on_deleted(event)
        #
        # what = 'directory' if event.is_directory else 'file'
        # logging.info("Deleted %s: %s", what, event.src_path)
        pass

    def on_modified(self, event):
        # super(LoggingEventHandler, self).on_modified(event)
        #
        # what = 'directory' if event.is_directory else 'file'
        # logging.info("Modified %s: %s", what, event.src_path)
        pass


def batch_cleansing(input_file, output_folder, trace_mode):
    filename = os.path.basename(input_file)
    name, ext = os.path.splitext(filename)

    backup_file = os.path.join(output_folder, filename)
    shutil.move(input_file, backup_file)

    output_file_customer_public = os.path.join(output_folder, '{}{}{}'.format(name, '_cleaned_customer_public', ext))
    output_file_customer_private = os.path.join(output_folder, '{}{}{}'.format(name, '_cleaned_customer_private', ext))
    output_file_analysis_public = os.path.join(output_folder, '{}{}{}'.format(name, '_cleaned_analysis_public', ext))
    output_file_analysis_private = os.path.join(output_folder, '{}{}{}'.format(name, '_cleaned_analysis_private', ext))

    run_cleansing(backup_file, output_file_analysis_private, keep_unsubmitted=False, v6_compatible=True, trace_mode=trace_mode)
    run_cleansing(backup_file, output_file_analysis_private, keep_unsubmitted=False, v6_compatible=True, trace_mode=trace_mode)
    run_cleansing(backup_file, output_file_customer_private, keep_unsubmitted=False, v6_compatible=False, trace_mode=trace_mode)
    run_cleansing(backup_file, output_file_analysis_public, keep_unsubmitted=True, v6_compatible=True, trace_mode=trace_mode)
    run_cleansing(backup_file, output_file_customer_public, keep_unsubmitted=True, v6_compatible=False, trace_mode=trace_mode)


@click.command()
# @click.argument('file', nargs=1)
@click.option('--input-folder', '-i', required=True, help='Input file path')
@click.option('--output-folder', '-o', required=False, help='Output folder path')
@click.option('--trace-mode', '-t', is_flag=True, type=bool, help='Trace mode will add additional comments for each rinsed cell')
def main(input_folder, output_folder, trace_mode):
    """This script cleansing raw data into cleaned data."""

    # logging.basicConfig(level=logging.INFO,
    #                     format='%(asctime)s - %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')

    if not os.path.exists(input_folder):
        print('input path [{}] not exist, quit'.format(input_folder))
        exit(0)

    if not os.path.isdir(input_folder):
        print('input path [{}] is not folder, quit'.format(input_folder))
        exit(0)

    if output_folder is None:
        output_folder = os.path.join(input_folder, 'cleaned')
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

    if not os.path.exists(output_folder):
        print('output path [{}] not exist, quit'.format(output_folder))
        exit(0)

    if not os.path.isdir(output_folder):
        print('output path [{}] is not folder, quit'.format(output_folder))
        exit(0)

    print('program is running in watching mode, watch path \'{}\', press Control-C to stop'.format(input_folder))
    event_handler = InputFileMatchingEventHandler(batch_cleansing, output_folder, trace_mode)
    observer = Observer()
    observer.schedule(event_handler, input_folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('program stopped')
        observer.stop()
    observer.join()


if __name__ == '__main__':
        main()

