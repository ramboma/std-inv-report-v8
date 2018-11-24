
from data_analysis.data_extract import *
from data_analysis.data_calculate import *
from data_analysis.data_style import *
from data_analysis.result_write import *


class DataAnalyzer(object):
    def __init__(self, df):
        self._df = df
        pass

    def analyse(self):
        raise Exception('method not implement')


class ValueRateDataAnalyzer(DataAnalyzer):
    def __init__(self, df, question_col):
        super().__init__(df)
        self._question_col = question_col

    def analyse(self):
        ls_metrics_cols = list(CONFIG.BASE_COLUMN)
        if self._question_col not in list(CONFIG.BASE_COLUMN):
            ls_metrics_cols.append(self._question_col)

        de = DataExtractor(self._df)
        df = de.extract_by_col_indexes(ls_metrics_cols)

        result = dict()
        result[CONFIG.TOTAL_COLUMN] = OverallDataCalculator(df, self._question_col, LookingAStyler()).calculate()
        result[CONFIG.GROUP_COLUMN[0]] = CollegeDataCalculator(df, self._question_col, LookingBStyler()).calculate()
        result[CONFIG.GROUP_COLUMN[1]] = MajorDataCalculator(df, self._question_col, LookingCStyler()).calculate()

        return result


class WorkOptionDataAnalyzer(ValueRateDataAnalyzer):
    def __init__(self, df):
        super().__init__(df, 'A3')


def test():
    # read excel as df
    df = object()
    woda = WorkOptionDataAnalyzer(df)
    result = woda.analyse()
    writer = AnalysisResultWriter('path to folder')
    writer.write_new_book('就业机会.xlsx', result)
    pass


if __name__ == '__main__':
    test()
