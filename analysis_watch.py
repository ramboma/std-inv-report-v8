#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""cleanse.py"""

__author__ = 'Gary.Z'

import click
import time
import shutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from data_analysis.data_analyze import *

logger = get_logger(__name__)


class InputFileMatchingEventHandler(FileSystemEventHandler):

    def __init__(self, batch_cleansing_handler, output_folder, config):
        super().__init__()

        self._batch_cleansing_handler = batch_cleansing_handler
        self._output_folder = output_folder
        self._config = config

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
            logger.info('input file {} detected'.format(event.src_path))
            self._batch_cleansing_handler(event.src_path, self._output_folder, self._config)
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


def get_error_filename(dirpath, name):
    return os.path.join(dirpath, '{}_error.txt'.format(name))


def run_generate_reports(input_file, output_folder, config):
    filename = os.path.basename(input_file)
    name, ext = os.path.splitext(filename)

    backup_file = os.path.join(output_folder, filename)
    try_move_file(input_file, backup_file)
    input_file = backup_file

    dirpath = output_folder

    try:
        tag = time.strftime('%Y%m%d%H%M%S', time.localtime())
        output_path = os.path.join(dirpath, '{}_analysis_{}'.format(name, tag))
        os.mkdir(output_path)

        # call report generator class here
        do_reports(input_file, output_path, config)

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
@click.option('--config', '-c', help='Config file path')
def main(input_folder, output_folder, config):
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

    if config is None or config == '':
        config = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'data_analysis/config.xlsx')

    logger.info('program is running in watching mode, watch path \'{}\', press Control-C to stop'.format(input_folder))

    event_handler = InputFileMatchingEventHandler(run_generate_reports, output_folder, config)
    observer = Observer()
    observer.schedule(event_handler, input_folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info('program stopped')
        observer.stop()
    except Exception as e:
        logger.error(e)
        observer.stop()
    finally:
        observer.join()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e, exc_info=True)
        # logger.error(e)
    finally:
        pass

