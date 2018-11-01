#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rules_assembler.py"""

__author__ = 'Gary.Z'


# from data_cleansing.rule.validation_rule import *
# from data_cleansing.rule.preprocess_rule import *
from data_cleansing.rule.cleanse_rules import *


class RuleSetAssembler(object):
    def __init__(self):
        self._init_rule_full_dict()

    def _init_rule_full_dict(self):
        self.__rule_dict = {}
        for rule in self._build_rule_full_list():
            self.__rule_dict[rule.id] = rule

    @staticmethod
    def _build_rule_full_list():
        rule_list = [
            RuleRemoveTestRecords(),
            RuleRemoveRecordsWithoutA2Answer(),
            RuleRemoveRecordsWithoutSubmitTime(),
            RuleRinseIrrelevantAnswers('4', RINSE_RULE_IRRELEVANT_QUESTIONS),
            RuleRinseNcOptionValues(),
            RuleRinseInvalidAnswers(),
            RuleRinseUnusualSalaryValues(),
            RuleRinseIrrelevantAnswers('8', RINSE_RULE_IRRELEVANT_QUESTIONS_V6_COMPATIBLE)
        ]
        return rule_list

    def assemble(self, rule_ids):
        rule_list = []
        for rule_id in rule_ids:
            if rule_id not in self.__rule_dict:
                raise Exception('cannot identify rule id: {}'.format(rule_id))
            else:
                rule_list.append(self.__rule_dict[rule_id])
        return rule_list
