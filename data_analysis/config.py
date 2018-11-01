#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'config.py'

__author__ = 'kuoren'

BASE_COLUMN = ('_10', '_14', 'A2')

A2_ANSWER = ['在国内工作', '自主创业', '自由职业', '在国内求学', '出国/出境', '未就业']
EXCEPTED_ANSWER = '无法评价'

MEASURE_NAME_RELATIVE = '相关度'
MEASURE_NAME_SATISFY = '满意度'
MEASURE_NAME_MEET = '符合度'
MEASURE_NAME_MEET_V = '非常符合度'
MEASURE_NAME_IMPORTANT = '重要度'
MEASURE_NAME_PLEASED = '满足度'
MEASURE_NAME_HELP = '帮助度'
MEASURE_NAME_FEEL= '体验度'



ANSWER_TYPE_RELATIVE = 'RELATIVE'
ANSWER_TYPE_SATISFY = 'SATISFY'
ANSWER_TYPE_MEET = 'MEET'
ANSWER_TYPE_MEET_V = 'MEET_V'
ANSWER_TYPE_IMPORTANT='IMPORTANT'
ANSWER_TYPE_PLEASED='PLEASED'
ANSWER_TYPE_HELP='HELP'
ANSWER_TYPE_FEEL='FEEL'


ANSWER_NORMAL_MEET_V = ['非常符合', '比较符合', '一般', '比较不符合', '非常不符合', '无法评价']
ANSWER_SCORE_DICT_MEET_V = {'非常符合': 5, '比较符合': 4, '一般': 3, '比较不符合': 2, '非常不符合': 1, '无法评价': 0}
ANSWER_NORMAL_MEET = ['很符合', '比较符合', '一般', '比较不符合', '很不符合', '无法评价']
ANSWER_SCORE_DICT_MEET = {'很符合': 5, '比较符合': 4, '一般': 3, '比较不符合': 2, '很不符合': 1, '无法评价': 0}

ANSWER_NORMAL_RELATIVE = ['很相关', '比较相关', '一般', '比较不相关', '很不相关', '无法评价']
ANSWER_SCORE_DICT_RELATIVE = {'很相关': 5, '比较相关': 4, '一般': 3, '比较不相关': 2, '很不相关': 1, '无法评价': 0}

ANSWER_NORMAL_SATISFY = ['很满意', '比较满意', '一般', '比较不满意', '很不满意', '无法评价']
ANSWER_SCORE_DICT_SATISFY = {'很满意': 5, '比较满意': 4, '一般': 3, '比较不满意': 2, '很不满意': 1, '无法评价': 0}

ANSWER_NORMAL_IMPORTANT = ['很重要', '比较重要', '一般', '不太重要', '很不重要', '无法评价']
ANSWER_SCORE_DICT_IMPORTANT = {'很重要': 5, '比较重要': 4, '一般': 3, '不太重要': 2, '很不重要': 1, '无法评价': 0}

ANSWER_NORMAL_PLEASED = ['完全满足', '大部分满足', '基本满足', '大部分没满足', '完全没满足', '无法评价']
ANSWER_SCORE_DICT_PLEASED = {'完全满足': 5, '大部分满足': 4, '基本满足': 3, '大部分没满足': 2, '完全没满足': 1, '无法评价': 0}

ANSWER_NORMAL_HELP = ['很大帮助', '较大帮助', '有些帮助', '没什么帮助', '完全没帮助', '无法评价']
ANSWER_SCORE_DICT_HELP = {'很大帮助': 5, '较大帮助': 4, '有些帮助': 3, '没什么帮助': 2, '完全没帮助': 1, '无法评价': 0}
ANSWER_NORMAL_FEEL = ['很好', '比较好', '一般', '比较差', '很差', '无法评价']
ANSWER_SCORE_DICT_FEEL = {'很好': 5, '比较好': 4, '一般': 3, '比较差': 2, '很差': 1, '无法评价': 0}


ANSWER_NORMAL_1 = ['很符合', '比较符合', '一般', '比较不符合', '很不符合', '无法评价']
ANSWER_SCORE_DICT_1 = {'很符合': 5, '比较符合': 4, '一般': 3, '比较不符合': 2, '很不符合': 1, '无法评价': 0}
ANSWER_NORMAL_2 = ['很相关', '比较相关', '一般', '比较不相关', '很不相关', '无法评价']
ANSWER_SCORE_DICT_2 = {'很相关': 5, '比较相关': 4, '一般': 3, '比较不相关': 2, '很不相关': 1, '无法评价': 0}
ANSWER_NORMAL_3 = ['很满意', '比较满意', '一般', '比较不满意', '很不满意', '无法评价']
ANSWER_SCORE_DICT_3 = {'很满意': 5, '比较满意': 4, '一般': 3, '比较不满意': 2, '很不满意': 1, '无法评价': 0}

ABILITY_SCORE = {'非常符合': 5, '有点符合': 4, '不一定': 3, '有点不符合': 2, '非常不符合': 1}
ABILITY_SCORE_REVERSE = {'非常符合': 1, '有点符合': 2, '不一定': 3, '有点不符合': 4, '非常不符合': 5}

ABILITY_REVERSE = ['I2-2-4', 'I2-6-15', 'I2-7-20', 'I2-8-22', 'I2-13-33', 'I2-14-35', 'I2-16-41', 'I2-16-43',
                   'I2-17-47', 'I2-18-51', 'I2-19-53', 'I2-19-56', 'I2-20-59', 'I2-20-61', 'I2-20-63', 'I2-22-68']

COLUMN_NAME_GRP_COUNT = {'grp': '分组', 'subject': '答题总人数'}
COLUMN_NAME_GRP_VAL_COUNT = {'grp': '分组', 'subject': '答题总人数', 'cnt': '回答此答案人数'}

RATE_COLUMN = ('答案', '回答此答案人数', '答题总人数', '比例')
MEAN_COLUMN = ('答案', '回答此答案人数', '答题总人数', '比例','度量','均值')
EMPLOYEE_RATE_COLUMN='就业率'
EMP_FREE_RATE_COLUMN='灵活就业率'
COMBINE_RATE='行业比率'
GROUP_COLUMN=('学院','专业','分组')

B10_1_ANSWER = ['0次']

# 条件过滤的key值
DICT_KEY=('column','cond')


COLLEGE_MAJOR=('_10', '_14')
TOTAL_COLUMN='总体'
GENDER=('男','女')
NATIONAL_COLUMN=('汉族','少数民族')
ORIGIN_COLUMN=('省内生源','省外生源')
INDUSTRY_COLUMN=('省内就业','省外就业')
EDUCATION_COLUMN=('教育','非教育')
MEDICAL_COLUMN=('医药卫生','非医疗卫生')
HEALTH_COLUMN=('卫生','非卫生')




ERROR_PARAMS="参数错误"
