import pandas as pd
import data_analysis.config as CONFIG
from data_analysis.formulas import *
from data_analysis.data_style import *


class DataCalculator(object):
    def __init__(self, df, target_col, styler=None):
        self._df = df
        self._tgt_col = target_col
        self._styler = styler
        pass

    def calculate(self):
        raise Exception('method not implement')


class OveralEmpRate(DataCalculator):
    """总体就业率"""

    def __init__(self, df, target_col, metric_col, styler=None):
        super().__init__(df, target_col, styler)
        self._metric_col = metric_col

    def calculate(self):
        # step1：筛选出指标中的值
        ls_metric = list(set(self._df[self._metric_col]))
        df_combines = []
        # step2：循环值进行计算
        for where in ls_metric:
            df_where = self._df[self._df[self._metric_col] == where]
            df_rate = formula_employe_rate(df_where)
            df_rate[self._metric_col] = where
            df_combines.append(df_rate)

        # combine overal
        df_overal = formula_employe_rate(self._df)
        df_overal[self._metric_col] = CONFIG.TOTAL_COLUMN
        df_combines.append(df_overal)

        # Concatenate everything into a single DataFrame
        df_ret = pd.concat(df_combines, ignore_index=True, sort=True)

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            self._styler.prettify(df_ret)
        print(df_ret)
        return df_ret


class GrpEmpRate(DataCalculator):
    """分组就业率"""

    def __init__(self, df, target_col, grp_cols, styler=None):
        super().__init__(df, target_col, styler)
        self._grp_cols = list(grp_cols)

    def calculate(self):
        df_grp = formula_employe_rate_grp(self._df, self._grp_cols)
        # combine overal
        df_overal = formula_employe_rate(self._df)
        # Concatenate everything into a single DataFrame
        df_ret = pd.concat([df_grp, df_overal], ignore_index=True, sort=True)
        df_ret.iloc[-1, 0:len(self._grp_cols)] = CONFIG.TOTAL_COLUMN
        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            self._styler.prettify(df_ret)
        print(df_ret)
        return df_ret


class OverallRateCalculator(DataCalculator):
    """总体答案占比"""

    def __init__(self, df, target_col, metric_col, styler=None):
        super().__init__(df, target_col, styler)
        self._metric_col = metric_col

    def calculate(self):
        # step1：筛选出指标中的值
        ls_metric = list(set(self._df[self._metric_col]))
        df_combines = []
        # step2：循环值进行计算
        for where in ls_metric:
            df_where = self._df[self._df[self._metric_col] == where]
            df_rate = formula_rate(df_where, self._tgt_col)
            df_rate[self._metric_col] = where
            df_combines.append(df_rate)

        # combine overal
        df_overal = formula_rate(self._df, self._tgt_col)
        df_overal[self._metric_col] = CONFIG.TOTAL_COLUMN
        df_combines.append(df_overal)

        # Concatenate everything into a single DataFrame
        df_ret = pd.concat(df_combines, ignore_index=True, sort=True)

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            self._styler.prettify(df_ret)
        print(df_ret)
        return df_ret


class GrpRateCalculator(DataCalculator):
    """分组答案占比"""

    def __init__(self, df, target_col, grp_cols, styler=None):
        super().__init__(df, target_col, styler)
        self._grp_cols = list(grp_cols)

    def calculate(self):
        df_grp = formula_rate_grp(self._df, self._tgt_col, self._grp_cols)
        # combine overal
        df_overal = formate_rate_t(formula_rate(self._df, self._tgt_col))
        # Concatenate everything into a single DataFrame
        df_ret = pd.concat([df_grp, df_overal], ignore_index=True, sort=True)
        df_ret.iloc[-1, 0:len(self._grp_cols)] = CONFIG.TOTAL_COLUMN
        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            self._styler.prettify(df_ret)
        print(df_ret)
        return df_ret
