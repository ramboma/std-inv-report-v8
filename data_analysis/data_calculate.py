
import data_analysis.config as CONFIG
import data_analysis.formulas as formulas
import pandas as pd
from data_analysis.data_style import *


class DataCalculator(object):
    def __init__(self, df, target_col, styler=None):
        self._df = df
        self._tgt_col = target_col
        self._styler = styler
        pass

    def calculate(self):
        raise Exception('method not implement')


class OverallDataCalculator(DataCalculator):
    def __init__(self, df, target_col, styler=None):
        super().__init__(df, target_col, styler)

    def calculate(self):
        option = formulas.answer_rate(self._df, self._tgt_col)
        rate_t = formulas.rate_T(option)

        df_concat = pd.concat([rate_t, rate_t], sort=False)
        df_concat.insert(0, CONFIG.TOTAL_COLUMN, CONFIG.TOTAL_COLUMN)

        if isinstance(self._styler, AnalysisResultStyler):
            self._styler.prettify(df_concat)

        return df_concat


class CollegeDataCalculator(DataCalculator):
    def __init__(self, df, target_col, styler=None):
        super().__init__(df, target_col, styler)

    def calculate(self):
        pass


class MajorDataCalculator(DataCalculator):
    def __init__(self, df, target_col, styler=None):
        super().__init__(df, target_col, styler)

    def calculate(self):
        pass

