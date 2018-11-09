#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""cleanse.py"""

__author__ = 'Gary.Z'

import click
import time
import shutil
# import portalocker
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from data_cleansing.cleanser_runner import *

logger = get_logger(__name__)


class InputFileMatchingEventHandler(FileSystemEventHandler):

    def __init__(self, batch_cleansing_handler, output_folder, degree, trace_mode, multi_thread):
        super().__init__()

        self.__batch_cleansing_handler = batch_cleansing_handler;
        self.__output_folder = output_folder
        self.__degree = degree
        self.__trace_mode = trace_mode
        self.__multi_thread = multi_thread

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
        # file_locked = True
        # wait_second = 1
        # count_down_max_times = 60
        # count_down = count_down_max_times
        # while file_locked and count_down > 0:
        #     try:
        #         with open(event.src_path, 'r') as f:
        #             portalocker.lock(f, portalocker.LOCK_EX)
        #             portalocker.unlock(f)
        #             file_locked = False
        #     except Exception as e:
        #         logger.debug(e)
        #         logger.info("waiting for file writing complete")
        #         time.sleep(wait_second)
        #     finally:
        #         count_down -= 1
        # if file_locked:
        #     raise Exception('file is locked by another process and exceeded waiting time limit: {} secs'.format(wait_second * count_down_max_times))
        filename = os.path.basename(event.src_path)
        name, ext = os.path.splitext(filename)
        if ext == '.xlsx':
            logger.info('input file {} detected'.format(event.src_path))
            self.__batch_cleansing_handler(event.src_path, self.__output_folder, self.__degree, self.__trace_mode, self.__multi_thread)
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


def try_move_file(src, dst, max_retry=20, retry_interval=3):
        success = False
        retry_count = max_retry
        while (not success) and retry_count > 0:
            try:
                shutil.move(src, dst)
                success = True
            except Exception as e:
                logger.debug(e)
                logger.info("waiting for file lock release")
                time.sleep(retry_interval)
            finally:
                retry_count -= 1
        if not success:
            raise Exception('file is locked by another process and exceeded waiting time limit: {} secs'.format(retry_interval * max_retry))


def batch_cleansing(input_file, output_folder, degree, trace_mode, multi_thread):
    filename = os.path.basename(input_file)
    name, ext = os.path.splitext(filename)

    backup_file = os.path.join(output_folder, filename)
    try_move_file(input_file, backup_file)
    input_file = backup_file

    dirpath = output_folder

    try:
        tag = time.strftime('%Y%m%d%H%M%S', time.localtime())

        setting_groups = []
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

    except Exception as e:
        logger.error(e, exc_info=True)
        with open(get_error_filename(dirpath, name), 'w') as f:
            f.write(e.__str__())
    finally:
        pass


@click.command()
# @click.argument('file', nargs=1)
@click.option('--input-folder', '-i', required=True, help='Input file path')
@click.option('--output-folder', '-o', required=False, help='Output folder path')
@click.option('--degree', '-d', help='Specify educational background, e.g. "本科毕业生"， "专科毕业生"')
@click.option('--trace-mode', '-t', is_flag=True, type=bool, help='Trace mode will add additional comments for each rinsed cell')
@click.option('--multi-thread', '-m', is_flag=True, type=bool, help='multi-thread mode, only make effect with -a')
def main(input_folder, output_folder, degree, trace_mode, multi_thread):
    """This script cleansing raw data into cleaned data."""

    if not os.path.exists(input_folder):
        logger.error('input path [{}] not exist, quit'.format(input_folder))
        exit(0)

    if not os.path.isdir(input_folder):
        logger.error('input path [{}] is not folder, quit'.format(input_folder))
        exit(0)

    if output_folder is None:
        output_folder = os.path.join(input_folder, 'cleaned')
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

    if not os.path.exists(output_folder):
        logger.error('output path [{}] not exist, quit'.format(output_folder))
        exit(0)

    if not os.path.isdir(output_folder):
        logger.error('output path [{}] is not folder, quit'.format(output_folder))
        exit(0)

    if trace_mode is None:
        trace_mode = False

    if multi_thread is None:
        multi_thread = False

    if trace_mode:
        logger.info('** TRACING MODE ENABLED **')

    logger.info('program is running in watching mode, watch path \'{}\', press Control-C to stop'.format(input_folder))
    event_handler = InputFileMatchingEventHandler(batch_cleansing, output_folder, degree, trace_mode, multi_thread)
    observer = Observer()
    observer.schedule(event_handler, input_folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info('program stopped')
        observer.stop()
    observer.join()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e, exc_info=True)
        # logger.error(e)
    finally:
        pass

