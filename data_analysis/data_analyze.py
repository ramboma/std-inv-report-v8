from data_analysis.data_extract import *
from data_analysis.data_calculate import *
from data_analysis.data_style import *
from data_analysis.result_write import *
from data_analysis.file_loader import *
from data_analysis.analyze_run import *


class DataAnalyzer(object):
    def __init__(self, df):
        self._df = df
        self._degree_col = '_12'
        pass

    def analyse(self):
        raise Exception('method not implement')


class ValueRateDataAnalyzer(DataAnalyzer):
    def __init__(self, df, question_col):
        super().__init__(df)
        self._question_col = question_col

    def analyse(self):
        # find out necessary data columns
        de = DataExtractor(self._df, [self._question_col, self._degree_col])
        df = de.extract_ref_cols()

        result = dict()
        # calculator 1
        result[CONFIG.TOTAL_COLUMN] = OverallRateCalculator(df,
                                                            self._question_col,
                                                            self._degree_col,
                                                            styler=OverallProvotStyler).calculate()

        # calculator 2
        result[CONFIG.GROUP_COLUMN[0]] = GrpRateCalculator(df, self._question_col,
                                                           [CONFIG.BASE_COLUMN[0]]).calculate()
        # calculator 3
        result[CONFIG.GROUP_COLUMN[1]] = GrpRateCalculator(df, self._question_col,
                                                           [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]]).calculate()

        return result


class WorkOptionDataAnalyzer(ValueRateDataAnalyzer):
    def __init__(self, df):
        super().__init__(df, 'A3', '_12')


class NonEmployeeDataAnalyzer(ValueRateDataAnalyzer):
    def __init__(self, df):
        super().__init__(df, 'C1')
        raise Exception('method not implement')


class EmpRateAndEmpStatus(DataAnalyzer):
    """就业率和就业状态"""

    def __init__(self, df):
        super().__init__(df)
        self._question_col = 'A2'

    def analyse(self):
        de = DataExtractor(self._df, [self._question_col, self._])
        df = de.extract_ref_cols()

        result = dict()
        # 总体就业率
        dict["总体就业率"] = OveralEmpRate(df, self._question_col, self._degree_col).calculate()

        dict["总体毕业去向"] = OverallRateCalculator(df, self._question_col).calculate()

        # 筛选出学历 如果为多学历需要计算总体
        ls_metric = list(set(df[self._degree_col]))
        if len(ls_metric)>1:
            dict["总体毕业生各学院就业率"] = GrpEmpRate(df, self._question_col, [CONFIG.BASE_COLUMN[0]]).calculate()
            dict["总体毕业生各专业就业率"] = GrpEmpRate(df, self._question_col,
                                             [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]]).calculate()
            dict["总体毕业生各学院毕业去向"] = GrpRateCalculator(df, self._question_col, [CONFIG.BASE_COLUMN[0]]).calculate()
            dict["总体毕业生各专业毕业去向"] = GrpRateCalculator(df, self._question_col,
                                                     [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]]).calculate()

        for metric in ls_metric:
            df_filter = df[df[self._degree_col] == metric]
            dict[metric + "各学院就业率"] = GrpEmpRate(df_filter, self._question_col, [CONFIG.BASE_COLUMN[0]]).calculate()
            dict[metric + "各专业就业率"] = GrpEmpRate(df_filter, self._question_col,
                                                 [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]]).calculate()
            dict[metric + "各学院毕业去向"] = GrpRateCalculator(df_filter, self._question_col,
                                                         [CONFIG.BASE_COLUMN[0]]).calculate()
            dict[metric + "各专业毕业去向"] = GrpRateCalculator(df_filter, self._question_col,
                                                         [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]]).calculate()

def test():
    # read excel as df
    file_loader = ExcelLoader("../test-data/san-ming/cleaned/cleaned.xlsx")
    df = file_loader.load_data
    # init a result writer
    writer = AnalysisResultWriter(CONFIG.REPORT_FOLDER)
    runner = AnalyzeRunner(writer)

    # Assemble all analyzers need to be run
    analyzer_collection = dict()
    # analyze 1
    analyzer_collection['就业机会'] = WorkOptionDataAnalyzer(df)
    # analyze 2
    # analyzer_collection['未就业分析'] = NonEmployeeDataAnalyzer(df)
    # ... analyze N

    runner.run_batch(analyzer_collection)

    pass


if __name__ == '__main__':
    test()
