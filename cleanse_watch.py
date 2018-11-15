#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""cleanse.py"""

__author__ = 'Gary.Z'

import click
import time
import shutil
# import portalocker
import multiprocessing
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from data_cleansing.cleanser_runner import *

logger = get_logger(__name__)


class InputFileMatchingEventHandler(FileSystemEventHandler):

    def __init__(self, batch_cleansing_handler, output_folder, degree=None, stream_mode=False, concurrent_mode=False, pool=None, trace_mode=False):
        super().__init__()

        self._batch_cleansing_handler = batch_cleansing_handler
        self._output_folder = output_folder
        self._degree = degree
        self._trace_mode = trace_mode
        self._stream_mode = stream_mode
        self._concurrent_mode = concurrent_mode
        self._pool = pool

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
            self._batch_cleansing_handler(event.src_path, self._output_folder, self._degree,
                                          self._stream_mode, self._concurrent_mode, self._pool, self._trace_mode)
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


def batch_cleansing(input_file, output_folder, degree=None, stream_mode=False, concurrent_mode=False, pool=None, trace_mode=False):
    filename = os.path.basename(input_file)
    name, ext = os.path.splitext(filename)

    tag = time.strftime('%Y%m%d%H%M%S', time.localtime())
    output_folder = get_output_folder(output_folder, name, tag, degree)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    backup_file = os.path.join(output_folder, filename)
    try_move_file(input_file, backup_file)
    input_file = backup_file

    dirpath = output_folder

    try:
        setting_groups = []
        setting_groups.extend([
            # internal, analysis
            {
                'input_file': input_file,
                'output_file': get_output_filename(dirpath, name, ext, True, True, tag, degree),
                'internal': True, 'analysis': True,
                'tag': tag, 'trace_mode': trace_mode, 'degree': degree,
            },
            # internal, customer
            {
                'input_file': input_file,
                'output_file': get_output_filename(dirpath, name, ext, True, False, tag, degree),
                'internal': True, 'analysis': False,
                'tag': tag, 'trace_mode': trace_mode, 'degree': degree,
            },
            # public, analysis
            {
                'input_file': input_file,
                'output_file': get_output_filename(dirpath, name, ext, False, True, tag, degree),
                'internal': False, 'analysis': True,
                'tag': tag, 'trace_mode': trace_mode, 'degree': degree,
            },
            # public, customer
            {
                'input_file': input_file,
                'output_file': get_output_filename(dirpath, name, ext, False, False, tag, degree),
                'internal': False, 'analysis': False,
                'tag': tag, 'trace_mode': trace_mode, 'degree': degree,
            },
        ])
        if concurrent_mode:
            run_concurrent(setting_groups, stream_mode, pool)
        else:
            run_serial(setting_groups, stream_mode)

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
@click.option('--stream-mode', '-sm', is_flag=True, type=bool, help='Use stream mode to process data, or by default in memory')
@click.option('--concurrent-mode', '-cm', is_flag=True, type=bool, help='Use multi-process to process data, or by default in serial')
def main(input_folder, output_folder, degree, stream_mode, concurrent_mode, trace_mode):
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

    if stream_mode is None:
        stream_mode = False

    if concurrent_mode is None:
        concurrent_mode = False

    logger.info('program is running in watching mode, watch path \'{}\', press Control-C to stop'.format(input_folder))

    pool = None
    if concurrent_mode:
        logger.info('init process pool ... ')
        max_count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(max_count)
        logger.info('{} processes initialed'.format(max_count))

    event_handler = InputFileMatchingEventHandler(batch_cleansing, output_folder, degree, stream_mode, concurrent_mode, pool, trace_mode)
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
        pool.close()
        pool.join()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e, exc_info=True)
        # logger.error(e)
    finally:
        pass

