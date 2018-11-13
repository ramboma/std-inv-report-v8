#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'reports_generator.py'

__author__ = 'kuoren'

from data_analysis.report import *


class ReportGenerator:
    def __init__(self, input_file, output_fold, config_file):
        self.input_file = input_file
        self.output_fold = output_fold
        self.config_file = config_file
    
    def generate(self):
        '''v1'''
        rep = Reporter(self.input_file, self.output_fold, self.config_file)
        rep.do_report()


def generate_reports(input_file, output_folder,config_file):
    reporter = ReportGenerator(input_file, output_folder, config_file)
    reporter.generate()
