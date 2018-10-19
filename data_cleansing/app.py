#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'app.py'

__author__ = 'Gary.Z'

import click
import utils as u


@click.command()
@click.argument('FILE', nargs=1)
@click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name', help='The person to greet.')
def main(file):
    """This script cleansing raw data into cleaned data."""
    print('reading')
    df = u.load_xlsx_file(file)


if __name__=='__main__':
        main()
