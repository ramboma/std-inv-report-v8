#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""config.py"""

__author__ = 'Gary.Z'

import logging

EXCEL_INDEX_BASE = 1
HEADER_ROW_INDEX = 0 + EXCEL_INDEX_BASE

BASE_INFO_COLS_MIN = 23

MAJOR_FILTER_LIST = ('测试专业',)
NC_OPTION_FILTER_LIST = ('无法评价', '以上均不需要改进')
G1_OPTION_FILTER_LIST = ('国际组织', '军队')
SALARY_FILTER_LOWER_LIMIT = 1000
SALARY_FILTER_TOP_RATIO = 0.003

RINSE_RULE_KEY_QUESTION = 'question_id'
RINSE_RULE_KEY_ANSWER = 'answer'
RINSE_RULE_KEY_OPERATOR = 'operator'
RINSE_RULE_KEY_ACTION = 'rinse_ids'
RINSE_RULE_OPERATOR_IN = 'IN'
RINSE_RULE_OPERATOR_NOTIN = 'NOT_IN'
# definition of irrelevant question rinse rule
RINSE_RULE_IRRELEVANT_QUESTIONS = [
    # IF A2 not in (在国内工作, 自由职业) then rinse
    #   B1, B2, B3, B4, B5, B6, B7-1, B7-2, B7-3, B7-4, B8, B9-1, B9-2, B10-1, B10-2, D1, D2
    {RINSE_RULE_KEY_QUESTION: 'A2',
     RINSE_RULE_KEY_ANSWER: ('在国内工作', '自由职业'),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7-1', 'B7-2', 'B7-3', 'B7-4', 'B8',
                  'B9-1', 'B9-2', 'B10-1', 'B10-2', 'D1', 'D2']},
    # IF A2 = 自由职业 then rinse B1,B2,B3,B4, B10-1
    {RINSE_RULE_KEY_QUESTION: 'A2',
     RINSE_RULE_KEY_ANSWER: ('自由职业',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_IN,
     RINSE_RULE_KEY_ACTION: ['B1', 'B2', 'B3', 'B4', 'B10-1', 'B10-2']},
    # IF B9-1 not in (比较不相关, 很不相关) then rinse B9-2
    {RINSE_RULE_KEY_QUESTION: 'B9-1',
     RINSE_RULE_KEY_ANSWER: ('比较不相关', '很不相关'),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['B9-2']},
    # IF B10-1 = 0次 then rinse B10-2
    {RINSE_RULE_KEY_QUESTION: 'B10-1',
     RINSE_RULE_KEY_ANSWER: ('0次',),
     RINSE_RULE_KEY_OPERATOR: 'IN',
     RINSE_RULE_KEY_ACTION: ['B10-2']},
    # IF A2 != 未就业 then rinse C1, C2
    {RINSE_RULE_KEY_QUESTION: 'A2',
     RINSE_RULE_KEY_ANSWER: ('未就业',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['C1', 'C2']},
    # IF A2 != 在国内升学 then rinse E1,E2,E3,E4
    {RINSE_RULE_KEY_QUESTION: 'A2',
     RINSE_RULE_KEY_ANSWER: ('在国内求学',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['E1', 'E2', 'E3', 'E4']},
    # IF E3 not in (比较不相关, 很不相关) then rinse E4
    {RINSE_RULE_KEY_QUESTION: 'E3',
     RINSE_RULE_KEY_ANSWER: ('比较不相关', '很不相关'),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['E4']},
    # IF A2 != 出国/出境 then rinse F1, F2, F3, F4
    {RINSE_RULE_KEY_QUESTION: 'A2',
     RINSE_RULE_KEY_ANSWER: ('出国/出境',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['F1', 'F2', 'F3', 'F4']},
    # IF F1 != 求学 then rinse F2, F3
    {RINSE_RULE_KEY_QUESTION: 'F1',
     RINSE_RULE_KEY_ANSWER: ('求学',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['F2', 'F3']},
    # IF F3 not in (比较不相关, 很不相关) then rinse F4
    {RINSE_RULE_KEY_QUESTION: 'F3',
     RINSE_RULE_KEY_ANSWER: ('比较不相关', '很不相关'),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['F4']},
    # IF A2 != 自主创业 then rinse G1, G2, G3, G4, G5
    {RINSE_RULE_KEY_QUESTION: 'A2',
     RINSE_RULE_KEY_ANSWER: ('自主创业',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['G1', 'G2', 'G3', 'G4', 'G5']},
    # I2-1 rules, 22 rules in total
    {RINSE_RULE_KEY_QUESTION: 'I2-1-A',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-1-1', 'I2-2-1-2']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-B',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-2-3', 'I2-2-2-4']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-C',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-3-5', 'I2-2-3-6']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-D',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-4-7', 'I2-2-4-8']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-E',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-5-9', 'I2-2-5-10', 'I2-2-5-11', 'I2-2-5-12', 'I2-2-5-13']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-F',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-6-14', 'I2-2-6-15', 'I2-2-6-16', 'I2-2-6-17', 'I2-2-6-18']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-G',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-7-19', 'I2-2-7-20']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-H',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-8-21', 'I2-2-8-22']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-I',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-9-23', 'I2-2-9-24', 'I2-2-9-25']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-J',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-10-26', 'I2-2-10-27']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-K',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-11-28', 'I2-2-11-29']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-L',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-12-30', 'I2-2-12-31', 'I2-2-12-32']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-M',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-13-33', 'I2-2-13-34']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-N',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-14-35', 'I2-2-14-36']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-O',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-15-37', 'I2-2-15-38', 'I2-2-15-39']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-P',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-16-40', 'I2-2-16-41', 'I2-2-16-43', 'I2-2-16-43']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-Q',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-17-44', 'I2-2-17-45', 'I2-2-17-46', 'I2-2-17-47']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-R',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-18-48', 'I2-2-18-49', 'I2-2-18-50', 'I2-2-18-51']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-S',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-19-52', 'I2-2-19-53', 'I2-2-19-54', 'I2-2-19-55', 'I2-2-19-56', 'I2-2-19-57']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-T',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-20-58', 'I2-2-20-59', 'I2-2-20-60', 'I2-2-20-61', 'I2-2-20-62', 'I2-2-20-63']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-U',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-21-64', 'I2-2-21-65']},
    {RINSE_RULE_KEY_QUESTION: 'I2-1-V',
     RINSE_RULE_KEY_ANSWER: ('1',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_NOTIN,
     RINSE_RULE_KEY_ACTION: ['I2-2-22-66', 'I2-2-22-67', 'I2-2-22-68']},
]

RINSE_RULE_IRRELEVANT_QUESTIONS_V6_COMPATIBLE = [
    {RINSE_RULE_KEY_QUESTION: 'A2',
     RINSE_RULE_KEY_ANSWER: ('自由职业',),
     RINSE_RULE_KEY_OPERATOR: RINSE_RULE_OPERATOR_IN,
     RINSE_RULE_KEY_ACTION: ['B5', 'B6', 'B7-1', 'B7-2', 'B7-3', 'B7-4', 'B8', 'B9-1', 'B9-2']},
]


def get_logger(name):
    # formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s %(name)s %(thread)d(%(threadName)s) %(levelname)s - %(message)s')

    file_handler = logging.FileHandler('runlog.txt', mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


# definition of question code mapping to excel column index
# QUESTION_TO_EXCEL_COLUMN_MAP = {
#     'A1': ['X', 'Y'],
#     'A2': ['Z'],
#     'B1': ['AB'],
#     'B2': ['AC'],
#     'B3': ['AD', 'AE', 'AF'],
#     'B4': ['AG', 'AH', 'AI'],
#     'B5': ['AJ', 'AK', 'AI'],
#     'B6': ['AL'],
#     'B7-1': ['AM'],
#     'B7-2': ['AN'],
#     'B7-3': ['AO'],
#     'B7-4': ['AP'],
#     'B8': ['AQ'],
#     'B9-1': ['AR'],
#     'B9-2': ['AS'],
#     'B10-1': ['AT'],
#     'B10-2': ['AU'],
#     'C1': ['AV'],
#     'C2': ['AW'],
#     'D1': ['AX'],
#     'D2': ['AY'],
#     'E1': ['AZ'],
#     'E2': ['BA'],
#     'E3': ['BB'],
#     'E4': ['BC'],
#     'F1': ['BD'],
#     'F2': ['BE'],
#     'F3': ['BF'],
#     'F4': ['BG'],
#     'G1': ['BH', 'BI'],
#     'G2': ['BJ'],
#     'G3': ['BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ'],
#     'G4': ['BR', 'BS', 'BT', 'BU', 'BV', 'BW'],
#     'G5': ['BX', 'BY', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CE'],
#     'I2-1-A': ['EL'],
#     'I2-1-B': ['EM'],
#     'I2-1-C': ['EN'],
#     'I2-1-D': ['EO'],
#     'I2-1-E': ['EP'],
#     'I2-1-F': ['EQ'],
#     'I2-1-G': ['ER'],
#     'I2-1-H': ['ES'],
#     'I2-1-I': ['ET'],
#     'I2-1-J': ['EU'],
#     'I2-1-K': ['EV'],
#     'I2-1-L': ['EW'],
#     'I2-1-M': ['EX'],
#     'I2-1-N': ['EY'],
#     'I2-1-O': ['EZ'],
#     'I2-1-P': ['FA'],
#     'I2-1-Q': ['FB'],
#     'I2-1-R': ['FC'],
#     'I2-1-S': ['FD'],
#     'I2-1-T': ['FE'],
#     'I2-1-U': ['FF'],
#     'I2-1-V': ['FG'],
#
#     'I2-1-1': ['FH'],
#     'I2-1-2': ['FI'],
#
#     'I2-3-5': ['FJ'],
#     'I2-3-6': ['FK'],
#
#     'I2-4-7': ['FL'],
#     'I2-4-8': ['FM'],
#
#     'I2-6-14': ['FN'],
#     'I2-6-15': ['FO'],
#     'I2-6-16': ['FP'],
#     'I2-6-17': ['FQ'],
#     'I2-6-18': ['FR'],
#
#     'I2-2-3': ['FS'],
#     'I2-2-4': ['FT'],
#
#     'I2-5-9': ['FU'],
#     'I2-5-10': ['FV'],
#     'I2-5-11': ['FW'],
#     'I2-5-12': ['FX'],
#     'I2-5-13': ['FY'],
#
#     'I2-7-19': ['FZ'],
#     'I2-7-20': ['GA'],
#
#     'I2-8-21': ['GB'],
#     'I2-8-22': ['GC'],
#     'I2-9-23': ['GD'],
#     'I2-9-24': ['GE'],
#     'I2-9-25': ['GF'],
#     'I2-10-26': ['GG'],
#     'I2-10-27': ['GH'],
#     'I2-11-28': ['GI'],
#     'I2-11-29': ['GJ'],
#     'I2-12-30': ['GK'],
#     'I2-12-31': ['GL'],
#     'I2-12-32': ['GM'],
#     'I2-13-33': ['GN'],
#     'I2-13-34': ['GO'],
#     'I2-14-35': ['GP'],
#     'I2-14-36': ['GQ'],
#     'I2-15-37': ['GR'],
#     'I2-15-38': ['GS'],
#     'I2-15-39': ['GT'],
#     'I2-16-40': ['GU'],
#     'I2-16-41': ['GV'],
#     'I2-16-42': ['GW'],
#     'I2-16-43': ['GX'],
#     'I2-17-44': ['GY'],
#     'I2-17-45': ['GZ'],
#     'I2-17-46': ['HA'],
#     'I2-17-47': ['HB'],
#     'I2-18-48': ['HC'],
#     'I2-18-49': ['HD'],
#     'I2-18-50': ['HE'],
#     'I2-18-51': ['HF'],
#     'I2-19-52': ['HG'],
#     'I2-19-53': ['HH'],
#     'I2-19-54': ['HI'],
#     'I2-19-55': ['HJ'],
#     'I2-19-56': ['HK'],
#     'I2-19-57': ['HL'],
#     'I2-20-58': ['HM'],
#     'I2-20-59': ['HN'],
#     'I2-20-60': ['HO'],
#     'I2-20-61': ['HP'],
#     'I2-20-62': ['HQ'],
#     'I2-20-63': ['HR'],
#     'I2-21-64': ['HS'],
#     'I2-21-65': ['HT'],
#     'I2-22-66': ['HU'],
#     'I2-22-67': ['HV'],
#     'I2-22-68': ['HW'],
# }

