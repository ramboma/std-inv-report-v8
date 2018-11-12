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
MEASURE_NAME_MEET_V = '符合度'
MEASURE_NAME_IMPORTANT = '重要度'
MEASURE_NAME_PLEASED = '满足度'
MEASURE_NAME_HELP = '帮助度'
MEASURE_NAME_FEEL = '体验度'
MEASURE_NAME_NUM = '机会'

ANSWER_TYPE_RELATIVE = 'RELATIVE'
ANSWER_TYPE_SATISFY = 'SATISFY'
ANSWER_TYPE_MEET = 'MEET'
ANSWER_TYPE_MEET_V = 'MEET_V'
ANSWER_TYPE_IMPORTANT = 'IMPORTANT'
ANSWER_TYPE_PLEASED = 'PLEASED'
ANSWER_TYPE_HELP = 'HELP'
ANSWER_TYPE_FEEL = 'FEEL'
ANSWER_TYPE_NUM = 'NUM'


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
ANSWER_NORMAL_NUM = ['非常多', '比较多', '一般', '比较少', '非常少', '无法评价']
ANSWER_SCORE_DICT_NUM = {'非常多': 5, '比较多': 4, '一般': 3, '比较少': 2, '非常少': 1, '无法评价': 0}

ABILITY_SCORE = {'非常符合': 5, '有点符合': 4, '不一定': 3, '有点不符合': 2, '非常不符合': 1}
ABILITY_SCORE_REVERSE = {'非常符合': 1, '有点符合': 2, '不一定': 3, '有点不符合': 4, '非常不符合': 5}


ANSWER_RECOMMED = ['愿意', '不确定', '不愿意']

ABILITY_REVERSE = ['I2-2-2-4', 'I2-2-6-15', 'I2-2-7-20', 'I2-2-8-22', 'I2-2-13-33',
                   'I2-2-14-35', 'I2-2-16-41', 'I2-2-16-43',
                   'I2-2-17-47', 'I2-2-18-51', 'I2-2-19-53', 'I2-2-19-56', 'I2-2-20-59',
                   'I2-2-20-61', 'I2-2-20-63', 'I2-2-22-68']

COLUMN_NAME_GRP_COUNT = {'grp': '分组', 'subject': '答题总人数'}
COLUMN_NAME_GRP_VAL_COUNT = {'grp': '分组', 'subject': '答题总人数', 'cnt': '回答此答案人数'}

RATE_COLUMN = ('答案', '回答此答案人数', '答题总人数', '比例')
MEAN_COLUMN = ('答案', '回答此答案人数', '答题总人数', '比例', '度量', '均值')
EMPLOYEE_RATE_COLUMN = '就业率'
EMP_FREE = '灵活就业率'
EMP_FREE_COLUMNS = ['自主创业','自由职业']

ABILITY_COLUMN='能力水平'
DIMISSION='离职率'
DIMISSION_COLUMNS=['1次','2次','3次及以上']

COMBINE_RATE = '行业比率'
GROUP_COLUMN = ('学院', '专业', '分组')
COLLEGE_MAJOR = ('_10', '_14')
TOTAL_COLUMN = '总体'
AVG_SALARY='本校平均薪酬'
SPECIAL_WHERE = '条件'
B10_1_ANSWER = ['0次']
OPER_NOT = '非'

# 条件过滤的key值
DICT_KEY = ('column', 'cond', 'oper')

SPECIAL_COLUMN = ('性别', '民族', '类别')
DICT_SUBJECT = {'H4-A': '专业课教师教学态度', 'H4-B': '专业课教师教学水平', 'H4-C': '公共课教师教学态度',
                'H4-D': '公共课教师教学水平', 'H4-E': '教学总评价',
                'H4-F': '生涯规划/就业指导课', 'H4-G': '职业咨询与辅导', 'H4-H': '校园招聘会/宣讲会',
                'H4-I': '学校发布的招聘信息', 'H4-J': '就业帮扶与推荐', 'H4-K': '就业手续办理（户口档案迁移等)',
                'H4-L': '创业课程和讲座', 'H4-M': '创新创业大赛', 'H4-N': '创业模拟与实训',
                'H4-O': '创业指导服务（如信息咨询、管理运营等）',
                'H3-E': '创业场地', 'H3-F': '创业资金',
                'H3-A': '实验教学', 'H3-B': '实习实训',
                'H3-C': '社会实践', 'H3-D': '毕业论文（设计）',
                'H2-A': '课堂目标', 'H2-B': '课堂纪律',
                'H2-C': '师生互动', 'H2-D': '反馈效果', 'H2-E': '教学效果',
                'B5-B': '行业', 'B1': '单位类型', 'B3-A': '就业地区', 'B3-B': '就业城市',
                'B4-B': '就业职业','D2':'求职困难',

                }
SPECIAL_SUBJECT = {'B9-1': '专业', 'B7-1': '工作满意度', 'B7-2': '薪酬',
                   'B7-3': '职业发展前景', 'B7-4': '工作内容',
                   'B8': '职业期待'}

DICT_TITLE = {'B5-B': '就业行业分布', 'B1': '就业单位类型分布', 'B3-A': '就业地区', 'B3-B': '省内就业地区分布',
              'B4-B': '就业职业分布', 'B2': '就业单位规模分布',
              'C1': '一直未就业分布', 'C2': '未就业毕业生目前去向分布',
              'D2':'求职困难','D1':'求职成功途径',
              'A2':'毕业去向','B9-2':'从事低专业相关工作的原因分布','E2':'升学原因','E4':'跨专业升学原因',
              'F1':'留学比列','F4':'跨专业升学原因'}

JOB_SATISFY_SUBJECT = {'B7-1': '对工作总体的满意情况', 'B7-2': '对工作薪酬的满意情况',
                       'B7-3': '对职业发展前景的满意情况', 'B7-4': '对工作内容意的满意情况'}

MAJOR_QUALITY_SUBJECT = {'I1-1-A': '专业知识', 'I1-1-B': '专业能力', 'I1-2-A': '专业知识', 'I1-2-B': '专业能力'}

DICT_REP = {'非男': '女', '非汉族': '少数民族', '非福建省': '省外'}
SPECIAL_COLUMN = ('性别', '民族', '类别')
PROVINCE = '福建省'
# 条件过滤的key值
DICT_KEY = ('column', 'cond', 'oper')
OPER = ('eq', 'noteq','in')

GENDER = ('男', '女')
NATIONAL_COLUMN = ('汉族', '少数民族')
ORIGIN_COLUMN = ('省内生源', '省外生源')
INDUSTRY_COLUMN = ('省内就业', '省外就业')
EDUCATION_COLUMN = ('教育', '非教育')
MEDICAL_COLUMN = ('医疗卫生', '非医疗卫生')
HEALTH_COLUMN = ('卫生', '非卫生')
TEACHER_COLUMN = ('师范', '非师范')

SPECIAL_REL=['_3','_10', '_14','_16','A1-A','A2','B1', 'B3-A','B4-A', 'B4-B',
             'B5-A','B5-B','B6','B9-1',
             'B7-1','B7-2','B7-3','B7-4','B8','B10-1','H7','H8',
             'H2-A', 'H2-B', 'H2-C', 'H2-D', 'H2-E',
             'H3-A', 'H3-B', 'H3-C', 'H3-D',
             'H4-A', 'H4-B', 'H4-C', 'H4-D', 'H4-E',]

REPORT_FOLDER = "../test-data/san-ming/report/"
SOURCE_FOLDER = "../test-data/san-ming/cleaned/"
CONFIG_FILE='subject_content.xlsx'
ERROR_PARAMS = "参数错误"

DECIMALS6 = 6
DECIMALS2 = 2
