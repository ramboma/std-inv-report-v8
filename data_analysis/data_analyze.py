from data_analysis.data_extract import *
from data_analysis.data_calculate import *
from data_analysis.data_style import *
from data_analysis.result_write import *
from data_analysis.file_loader import *
from data_analysis.analyze_run import *


class DataAnalyzer(object):
    def __init__(self, df, dict_config=None):
        self._df = df
        self._dict_config = dict_config
        self._degree_col = '_12'
        pass

    def analyse(self):
        raise Exception('method not implement')



class OverallAnswerIndexDataAnalyzer(DataAnalyzer):
    """只包含总体，且以答案为索引"""

    def __init__(self, df, question_cols, dict_config=None):
        super().__init__(df, dict_config)
        self._question_cols = question_cols

    def analyse(self):
        # find out necessary data columns
        if self._dict_config is None:
            raise ("缺少配置文件，无法解析sheet name")
        de = DataExtractor(self._df, self._question_cols)
        df = de.extract_ref_cols()
        result = dict()
        style = AnswerIndexStyler()
        if isinstance(self._question_cols, list):
            for question_col in self._question_cols:
                sheet_name = self._dict_config[question_col]
                result[sheet_name] = OverallRateCalculator(df, question_col,
                                                           self._degree_col,
                                                           styler=style).calculate()
        else:
            raise ("当前只支持列表类型")
        return result


class ValueRateDataAnalyzer(DataAnalyzer):
    def __init__(self, df, question_col, dict_config=None):
        super().__init__(df, dict_config)
        self._question_col = question_col

    def analyse(self):
        if self._dict_config is None:
            raise ("缺少配置文件，无法解析sheet name")
        sheet_name = self._dict_config[self._question_col]
        # find out necessary data columns
        de = DataExtractor(self._df, self._question_col)
        df = de.extract_ref_cols()

        result = dict()
        # calculator 1
        style = DegreeIndexStyler()
        result["总体毕业生" + sheet_name] = OverallRateCalculator(df,
                                                             self._question_col,
                                                             self._degree_col,
                                                             styler=style).calculate()
        # 筛选出学历 如果为多学历需要计算总体
        ls_metric = list(set(df[self._degree_col]))
        if len(ls_metric) > 1:
            result["总体毕业生各学院" + sheet_name] = GrpRateCalculator(df, self._question_col,
                                                              [CONFIG.BASE_COLUMN[0]]).calculate()
            result["总体毕业生各专业" + sheet_name] = GrpRateCalculator(df, self._question_col,
                                                              [CONFIG.BASE_COLUMN[0],
                                                               CONFIG.BASE_COLUMN[1]]).calculate()

        for metric in ls_metric:
            df_filter = df[df[self._degree_col] == metric]
            result[metric + "各学院毕业去向"] = GrpRateCalculator(df_filter, self._question_col,
                                                         [CONFIG.BASE_COLUMN[0]]).calculate()
            result[metric + "各专业毕业去向"] = GrpRateCalculator(df_filter, self._question_col,
                                                         [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]]).calculate()
        return result


class FiveRateDataAnalyzer(DataAnalyzer):
    def __init__(self, df, question_col, metric_type, dict_config=None):
        super().__init__(df, dict_config)
        self._question_col = question_col
        self._metric_type = metric_type

    def analyse(self):
        if self._dict_config is None:
            raise ("缺少配置文件，无法解析sheet name")
        sheet_name = self._dict_config[self._question_col]
        # find out necessary data columns
        de = DataExtractor(self._df, self._question_col)
        df = de.extract_ref_cols()

        result = dict()
        # calculator 1
        result["总体毕业生" + sheet_name] = OverallFiveCalculator(df, self._question_col,
                                                             self._degree_col,
                                                             self._metric_type,
                                                             styler=None).calculate()
        # 筛选出学历 如果为多学历需要计算总体
        ls_metric = list(set(df[self._degree_col]))
        if len(ls_metric) > 1:
            result["总体毕业生各学院" + sheet_name] = GrpFiveCalculator(df, self._question_col,
                                                              [CONFIG.BASE_COLUMN[0]],
                                                              self._metric_type).calculate()
            result["总体毕业生各专业" + sheet_name] = GrpFiveCalculator(df, self._question_col,
                                                              [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]],
                                                              self._metric_type).calculate()

        for metric in ls_metric:
            df_filter = df[df[self._degree_col] == metric]
            result[metric + "各学院毕业去向"] = GrpFiveCalculator(df_filter, self._question_col,
                                                         [CONFIG.BASE_COLUMN[0]],
                                                         self._metric_type).calculate()
            result[metric + "各专业毕业去向"] = GrpFiveCalculator(df_filter, self._question_col,
                                                         [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]],
                                                         self._metric_type).calculate()
        return result


class EmpRateAndEmpStatus(DataAnalyzer):
    """就业率和就业状态"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, dict_config)
        self._question_col = 'A2'

    def analyse(self):
        de = DataExtractor(self._df, [self._question_col, self._degree_col])
        df = de.extract_ref_cols()

        result = dict()
        # 总体就业率
        result['总体就业率'] = OveralEmpRate(df, self._question_col, self._degree_col).calculate()

        result["总体毕业去向"] = OverallRateCalculator(df, self._question_col, self._degree_col, ).calculate()

        # 筛选出学历 如果为多学历需要计算总体
        ls_metric = list(set(df[self._degree_col]))
        if len(ls_metric) > 1:
            result["总体毕业生各学院就业率"] = GrpEmpRate(df, self._question_col, [CONFIG.BASE_COLUMN[0]]).calculate()
            result["总体毕业生各专业就业率"] = GrpEmpRate(df, self._question_col,
                                             [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]]).calculate()
            result["总体毕业生各学院毕业去向"] = GrpRateCalculator(df, self._question_col, [CONFIG.BASE_COLUMN[0]]).calculate()
            result["总体毕业生各专业毕业去向"] = GrpRateCalculator(df, self._question_col,
                                                     [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]]).calculate()

        for metric in ls_metric:
            df_filter = df[df[self._degree_col] == metric]
            result[metric + "各学院就业率"] = GrpEmpRate(df_filter, self._question_col, [CONFIG.BASE_COLUMN[0]]).calculate()
            result[metric + "各专业就业率"] = GrpEmpRate(df_filter, self._question_col,
                                                 [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]]).calculate()
            result[metric + "各学院毕业去向"] = GrpRateCalculator(df_filter, self._question_col,
                                                         [CONFIG.BASE_COLUMN[0]]).calculate()
            result[metric + "各专业毕业去向"] = GrpRateCalculator(df_filter, self._question_col,
                                                         [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]]).calculate()
        return result


class WorkOptionDataAnalyzer(ValueRateDataAnalyzer):
    """就业机会"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'A3', dict_config)


class NonEmployeeDataAnalyzer(OverallAnswerIndexDataAnalyzer):
    """未就业报告"""

    def __init__(self, df, dic_config=None):
        super().__init__(df, ['C1', 'C2'], dic_config)


############# 就业竞争力 start
class WorkStabilityAnalyzer(ValueRateDataAnalyzer):
    """工作稳定性"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'B10-1', dict_config)
    # TODO 追加离职率计算


class JobMeetAnalyzer(FiveRateDataAnalyzer):
    """职业期待吻合度"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'B8', CONFIG.ANSWER_TYPE_MEET, dict_config)


class JobSatisfyAnalyzer(FiveRateDataAnalyzer):
    """就业满意度"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'B7-1', CONFIG.JOB_SATISFY_SUBJECT, dict_config)
    # TODO 对工作各方面满意情况，三维拼接


class MajorRelativeAnalyzer(FiveRateDataAnalyzer):
    """专业相关度"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'B9-1', CONFIG.ANSWER_TYPE_RELATIVE, dict_config)
    # TODO B9-2


########### 就业竞争力 end


class EvelutionH4_EAnalyzer(FiveRateDataAnalyzer):
    '''母校任课教师总体报告'''

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'H4-E', CONFIG.ANSWER_TYPE_SATISFY, dict_config)


class EvelutionAcademicAnalyzer(FiveRateDataAnalyzer):
    '''母校的学风认可度评价'''

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'J5-5', CONFIG.ANSWER_TYPE_FEEL, dict_config)


class EvelutionH4_TAnalyzer(FiveRateDataAnalyzer):
    """教育教学报告"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'H4-T', CONFIG.ANSWER_TYPE_SATISFY, dict_config)


class EvelutionH4_SAnalyzer(FiveRateDataAnalyzer):
    '''实践教学报告'''

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'H4-S', CONFIG.ANSWER_TYPE_SATISFY, dict_config)


class EvelutionH4_RAnalyzer(FiveRateDataAnalyzer):
    '''社团活动报告'''

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'H4-R', CONFIG.ANSWER_TYPE_SATISFY, dict_config)


class EvelutionH4_PAnalyzer(FiveRateDataAnalyzer):
    '''母校学生管理报告'''

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'H4-P', CONFIG.ANSWER_TYPE_SATISFY, dict_config)
    # TODO H5


def test():
    # read excel as df
    file_loader = ExcelLoader("../test-data/san-ming/cleaned/cleaned.xlsx")
    df = file_loader.load_data
    config_loader = ExcelLoader("config.xlsx")
    dic_config = config_loader.dict_data

    # init a result writer
    writer = AnalysisResultWriter(CONFIG.REPORT_FOLDER)
    runner = AnalyzeRunner(writer)

    # Assemble all analyzers need to be run
    analyzer_collection = dict()

    analyzer_collection['实践教学的评价'] = EvelutionH4_SAnalyzer(df, dic_config)

    runner.run_batch(analyzer_collection)

    pass


if __name__ == '__main__':
    test()
