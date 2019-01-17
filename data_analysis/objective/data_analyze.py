#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""data_analyze.py"""
"""客观数据报表生成类"""

__author__ = 'kuoren'

from data_analysis.result_write import *
from data_analysis.file_loader import *
import data_analysis.config as CONFIG
from data_analysis.analyze_run import *
from data_analysis.data_calculate import *


class DataAnalyzer(object):
    def __init__(self, df, dict_config=None):
        self._df = df
        self._dict_config = dict_config
        self._degree_col = '_12'
        pass

    def analyse(self):
        raise Exception('method not implement')


def common_grp_anaysis(df, question_col, class_name, sheet_name, dic_grp={}):
    """学院、专业通用部分"""
    degree_col = "学历合并"
    result = dict()

    # 筛选出学历 如果为多学历需要计算总体
    ls_metric = list(set(df[degree_col]))
    if len(ls_metric) > 1:
        if dic_grp:
            for key in dic_grp:
                result["总体毕业生" + key + sheet_name] = class_name(df, question_col,
                                                                list(dic_grp[key])).calculate()
        else:
            result["总体毕业生各学院" + sheet_name] = class_name(df,
                                                         question_col,
                                                         ['学院']).calculate()
            result["总体毕业生各专业" + sheet_name] = class_name(df, question_col,
                                                         ['学院', '专业']).calculate()

    for metric in ls_metric:
        df_filter = df[df[degree_col] == metric]
        if not df_filter.empty:
            if dic_grp:
                for key in dic_grp:
                    result[metric + key + sheet_name] = class_name(df_filter, question_col,
                                                                   list(dic_grp[key])).calculate()
            else:
                result[metric + "各学院" + sheet_name] = class_name(df_filter, question_col,
                                                                 ['学院']).calculate()
                result[metric + "各专业" + sheet_name] = class_name(df_filter, question_col,
                                                                 ['学院', '专业']).calculate()
    return result


class SizeAndStructureAnalyzer(DataAnalyzer):
    """毕业生规模和结构"""

    def __init__(self, df, dict_config):
        super().__init__(df, dict_config)
        self._question_cols = '学历合并'

    def analyse(self):
        rel_cols = CONFIG.OBJECTIVE_BASE
        de = DataExtractor(self._df, self._question_cols)
        df = de.extract_objective_cols(rel_cols)

        result = dict()
        style = ObjectiveOrderStyler()
        result['总体规模'] = ObjectiveSizeCalculator(df,
                                                 self._question_cols,
                                                 styler=style).calculate()
        result.update(common_grp_anaysis(df, self._question_cols, ObjectiveGrpSizeCalculator, '结构'))
        return result


class EmpRateAnalyzer(object):
    """就业率"""

    def __init__(self, df, dict_config):
        super().__init__(df, dict_config)

    def analyse(self):
        pass


class SignedRateAnalyzer(object):
    """签约率"""

    def __init__(self, df, dict_config):
        super().__init__(df, dict_config)

    def analyse(self):
        pass


class EmpRegionAnalyzer(object):
    """就业地区分布"""

    def __init__(self, df, dict_config):
        super().__init__(df, dict_config)

    def analyse(self):
        pass


class EmpIndustryAnalyzer(object):
    """就业行业分布"""

    def __init__(self, df, dict_config):
        super().__init__(df, dict_config)

    def analyse(self):
        pass


class EmpCareerAnalyzer(object):
    """就业职业分布"""

    def __init__(self, df, dict_config):
        super().__init__(df, dict_config)

    def analyse(self):
        pass


class EmpUnitAnalyzer(object):
    """就业职业分布"""

    def __init__(self, df, dict_config):
        super().__init__(df, dict_config)

    def analyse(self):
        pass


def test():
    # read excel as df
    file_loader = ExcelLoader("../../test-data/san-ming/cleaned/objective.xlsx")
    df = file_loader.load_data
    config_loader = ExcelLoader("../config.xlsx")
    dic_config = config_loader.dict_data

    # init a result writer
    writer = AnalysisResultWriter(CONFIG.OBJECTIVE_REPORT_FOLDER)
    runner = AnalyzeRunner(writer)

    # Assemble all analyzers need to be run
    analyzer_collection = dict()
    analyzer_collection['1-毕业生规模和结构'] = SizeAndStructureAnalyzer(df, dic_config)
    # analyzer_collection['2-就业率'] = EmpRateAnalyzer(df, dic_config)
    # analyzer_collection['3-签约率'] = SignedRateAnalyzer(df, dic_config)
    # analyzer_collection['4-就业地区分布'] = EmpRegionAnalyzer(df, dic_config)
    # analyzer_collection['5-就业行业分布'] = EmpIndustryAnalyzer(df, dic_config)
    # analyzer_collection['6-就业职业分布'] = EmpCareerAnalyzer(df, dic_config)
    # analyzer_collection['7-就业单位分布'] = EmpUnitAnalyzer(df, dic_config)

    # analyzer_collection['8-不同性别就业基本情况'] = MajorQualityAnalyzer(df, dic_config)
    # analyzer_collection['9-不同困难生就业基本情况'] = BasicQualityAnalyzer(df, dic_config)
    # analyzer_collection['10-不同师范生就业基本情况'] = MajorQualityAnalyzer(df, dic_config)
    # analyzer_collection['11-不同政治面貌就业基本情况'] = BasicQualityAnalyzer(df, dic_config)
    # analyzer_collection['12-不同民族就业基本情况'] = MajorQualityAnalyzer(df, dic_config)
    # analyzer_collection['13-省内、省外生源就业基本情况'] = BasicQualityAnalyzer(df, dic_config)
    # analyzer_collection['14-不同招生途径就业基本情况'] = MajorQualityAnalyzer(df, dic_config)
    # analyzer_collection['15-京津冀就业群体-单位行业'] = BasicQualityAnalyzer(df, dic_config)
    # analyzer_collection['16-京津冀就业群体-单位性质'] = BasicQualityAnalyzer(df, dic_config)

    runner.run_batch(analyzer_collection)

    pass


if __name__ == '__main__':
    test()
