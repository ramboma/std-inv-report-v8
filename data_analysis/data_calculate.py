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
            df_rate.insert(0, self._metric_col, where)
            df_combines.append(df_rate)

        # 拼接后排序
        df_combines = pd.concat(df_combines, sort=False)
        df_combines.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)

        # combine overal
        df_overal = formula_employe_rate(self._df)
        df_overal.insert(0, self._metric_col, CONFIG.TOTAL_COLUMN)
        df_combines=df_combines.append(df_overal)

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            self._styler.prettify(df_combines)
        print(df_combines)
        return df_combines


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
        df_ret = pd.concat([df_grp, df_overal], sort=False)
        df_ret.iloc[-1, 0:len(self._grp_cols)] = CONFIG.TOTAL_COLUMN
        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            self._styler.prettify(df_ret)
        print(df_ret)
        return df_ret


class OverallRateCalculator(DataCalculator):
    """总体答案占比 需要额外配置是否行转列，配置额外计算 eg 灵活就业率和离职率 name:[值]"""

    def __init__(self, df, target_col, metric_col, do_t=False, extra={}, styler=None):
        super().__init__(df, target_col, styler)
        self._metric_col = metric_col
        self._do_t=do_t
        self._extra=extra

    def calculate(self):
        # step1：筛选出指标中的值
        ls_metric = list(set(self._df[self._metric_col]))
        df_combines = []
        # step2：循环值进行计算
        for where in ls_metric:
            df_where = self._df[self._df[self._metric_col] == where]
            df_rate = formula_rate(df_where, self._tgt_col)
            if self._do_t:
                df_rate = formate_rate_t(df_rate)
            df_rate.insert(0, self._metric_col, where)
            df_combines.append(df_rate)
        # 拼接后排序
        df_combines = pd.concat(df_combines, sort=False)
        df_combines.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)

        # combine overal
        df_overal = formula_rate(self._df, self._tgt_col)
        if self._do_t:
            df_overal = formate_rate_t(df_overal)

        df_overal.insert(0, self._metric_col, CONFIG.TOTAL_COLUMN)
        df_combines=df_combines.append(df_overal)
        df_combines.fillna(0, inplace=True)

        if self._do_t and self._extra:
            for key in self._extra.keys():
                df_combines[key]=0
                for col in self._extra[key]:
                    if col in df_combines.columns:
                        df_combines.loc[:,key]=df_combines.loc[:,key]+df_combines.loc[:,col]

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            df_combines = self._styler.prettify(df_combines)
        return df_combines


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
        df_ret = pd.concat([df_grp, df_overal], sort=False)
        df_ret.iloc[-1, 0:len(self._grp_cols)] = CONFIG.TOTAL_COLUMN
        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            self._styler.prettify(df_ret)
        return df_ret

class OverallThreeCalculator():
    """三维总体答案占比 """
    def __init__(self, df, metric_col, metric_type, dict_extra={}, styler=None):
        self._df=df
        self._styler=styler
        self._metric_col = metric_col
        self._metric_type = metric_type
        self._dict_extra=dict_extra

    def calculate(self):
        # 各学历下的三维占比
        measure_name = parse_measure_name(self._metric_type)
        forcus_cols=[measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]]
        forcus_cols.append(self._metric_col)
        for key in self._dict_extra.keys():
            df_combines=[]
            for col in self._dict_extra[key]:
                df_five = OverallFiveCalculator(self._df, col, self._metric_col,
                                                self._metric_type, self._styler).calculate()
                df_three=df_five[forcus_cols]
                df_three.insert(0,key,col)
                df_combines.append(df_three)

            df_combines = pd.concat(df_combines, sort=False)
            df_t = df_combines.pivot_table(index=key,
                                        columns='_12',
                                        values=[measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]])
            df_t.fillna(0, inplace=True)
            df_t.reset_index(inplace=True)
            return df_t


class GrpThreeCalculator():
    """三维分组答案占比"""

    def __init__(self, df, grp_cols, metric_type, dict_extra={}, styler=None):
        self._df = df
        self._styler = styler
        self._grp_cols = grp_cols
        self._metric_type = metric_type
        self._dict_extra = dict_extra
        self

    def calculate(self):
        measure_name = parse_measure_name(self._metric_type)
        forcus_cols=[measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]]
        forcus_cols.extend(self._grp_cols)
        for key in self._dict_extra.keys():
            df_combines = []
            for col in self._dict_extra[key]:
                df_grp = GrpFiveCalculator(self._df, col, self._grp_cols,
                                           self._metric_type, self._styler).calculate()
                df_three = df_grp[forcus_cols]
                df_three.insert(0,key,col)
                df_combines.append(df_three)

            df_combines = pd.concat(df_combines, sort=False)

            df_t = df_combines.pivot_table(index=self._grp_cols,
                                        columns=key,
                                        values=[measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]])
            df_t.fillna(0, inplace=True)
            df_t.reset_index(inplace=True)
            return df_t


class OverallFiveCalculator(DataCalculator):
    """五维总体答案占比"""

    def __init__(self, df, target_col, metric_col, metric_type, styler=None):
        super().__init__(df, target_col, styler)
        self._metric_col = metric_col
        self._metric_type = metric_type

    def calculate(self):
        # step1：筛选出指标中的值
        ls_metric = list(set(self._df[self._metric_col]))
        df_combines = []
        # step2：循环值进行计算
        for where in ls_metric:
            df_where = self._df[self._df[self._metric_col] == where]
            df_rate = formula_five_rate(df_where, self._tgt_col, self._metric_type)
            df_rate.insert(0, self._metric_col, where)
            df_combines.append(df_rate)
        # Concatenate everything into a single DataFrame
        df_combines = pd.concat(df_combines, sort=False)
        df_combines.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)

        # combine overal
        df_overal = formula_five_rate(self._df, self._tgt_col, self._metric_type)
        df_overal.insert(0, self._metric_col, CONFIG.TOTAL_COLUMN)
        df_combines=df_combines.append(df_overal)
        df_combines.fillna(0, inplace=True)

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            df_combines = self._styler.prettify(df_combines)
        return df_combines


class GrpFiveCalculator(DataCalculator):
    """五维分组答案占比"""

    def __init__(self, df, target_col, grp_cols, metric_type, styler=None):
        super().__init__(df, target_col, styler)
        self._grp_cols = list(grp_cols)
        self._metric_type = metric_type

    def calculate(self):
        df_grp = formula_five_rate_grp(self._df, self._tgt_col, self._grp_cols, self._metric_type)
        # combine overal
        df_overal = formula_five_rate(self._df, self._tgt_col, self._metric_type)
        # Concatenate everything into a single DataFrame
        df_ret = pd.concat([df_grp, df_overal], sort=False)
        df_ret.iloc[-1, 0:len(self._grp_cols)] = CONFIG.TOTAL_COLUMN
        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            self._styler.prettify(df_ret)
        print(df_ret)
        return df_ret


class OverallIncomeCalculator(DataCalculator):
    """月均收入总体答案占比"""

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
            df_rate = formula_mean(df_where)
            df_rate.insert(0, self._metric_col, where)
            df_combines.append(df_rate)

        # Concatenate everything into a single DataFrame
        df_combines = pd.concat(df_combines, sort=False)
        df_combines.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)

        # combine overal
        df_overal = formula_mean(self._df)
        df_overal.insert(0, self._metric_col, CONFIG.TOTAL_COLUMN)
        df_combines=df_combines.append(df_overal)

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            df_ret = self._styler.prettify(df_combines)
        return df_ret

class GrpMeanCalculator(DataCalculator):
    """分组计算均值 eg 月均收入均值"""

    def __init__(self, df, target_col, grp_cols, styler=None):
        super().__init__(df, target_col, styler)
        self._grp_cols = list(grp_cols)

    def calculate(self):
        df_grp = formula_mean_grp(self._df, self._tgt_col, self._grp_cols)
        # combine overal
        df_overal = formula_mean(self._df, self._tgt_col)
        # Concatenate everything into a single DataFrame
        df_ret = pd.concat([df_grp, df_overal], sort=False)
        df_ret.iloc[-1, 0:len(self._grp_cols)] = CONFIG.TOTAL_COLUMN
        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            self._styler.prettify(df_ret)
        return df_ret

class AnswerPeriodCalculator(DataCalculator):
    """月均收入区间统计"""

    def __init__(self, df, target_col, metric_col, start, period_num, step, styler=None):
        super().__init__(df, target_col, styler)
        self._metric_col = metric_col
        self._start=start
        self._period_num=period_num
        self._step=step

    def calculate(self):
        # step1：筛选出指标中的值
        ls_metric = list(set(self._df[self._metric_col]))
        df_combines = []
        # step2：循环值进行计算
        for where in ls_metric:
            df_where = self._df[self._df[self._metric_col] == where]
            df_rate = formula_answer_period(df_where, self._tgt_col, self._start,
                                            self._period_num, self._step)
            df_rate.insert(0, self._metric_col, where)
            df_combines.append(df_rate)
        # Concatenate everything into a single DataFrame
        df_combines = pd.concat(df_combines, sort=False)
        df_combines.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)

        # combine overal
        df_overal = formula_answer_period(self._df, self._tgt_col, self._start,
                                         self._period_num, self._step)
        df_overal.insert(0, self._metric_col, CONFIG.TOTAL_COLUMN)
        df_combines=df_combines.append(df_overal)

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            df_ret = self._styler.prettify(df_combines)
        return df_ret