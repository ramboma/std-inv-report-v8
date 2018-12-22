#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""data_calculate.py"""
"""单个sheet计算类"""

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
        df_combines = df_combines.append(df_overal)

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
        return df_ret


class OverallRateCalculator(DataCalculator):
    """总体答案占比 需要额外配置是否行转列，配置额外计算 eg 灵活就业率和离职率 name:[值]"""

    def __init__(self, df, target_col, metric_col, do_t=False, extra={}, styler=None):
        super().__init__(df, target_col, styler)
        self._metric_col = metric_col
        self._do_t = do_t
        self._extra = extra

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
        df_combines = df_combines.append(df_overal)
        df_combines.fillna(0, inplace=True)

        if self._do_t and self._extra:
            for key in self._extra.keys():
                df_combines[key] = 0
                for col in self._extra[key]:
                    if col in df_combines.columns:
                        df_combines.loc[:, key] = df_combines.loc[:, key] + df_combines.loc[:, col]

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            df_combines = self._styler.prettify(df_combines)
        return df_combines


class GrpRateCalculator(DataCalculator):
    """分组答案占比"""

    def __init__(self, df, target_col, grp_cols, extra={}, styler=None, ):
        super().__init__(df, target_col, styler)
        self._grp_cols = list(grp_cols)
        self._extra = extra

    def calculate(self):
        df_grp = formula_rate_grp(self._df, self._tgt_col, self._grp_cols)
        # combine overal
        df_overal = formate_rate_t(formula_rate(self._df, self._tgt_col))
        # Concatenate everything into a single DataFrame
        df_ret = pd.concat([df_grp, df_overal], sort=False)
        df_ret.iloc[-1, 0:len(self._grp_cols)] = CONFIG.TOTAL_COLUMN
        # 结果集额外计算
        if self._extra:
            for key in self._extra:
                df_ret[key] = 0
                for col in self._extra[key]:
                    if col in df_ret.columns:
                        df_ret.loc[:, key] = df_ret.loc[:, key] + df_ret.loc[:, col]
        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            self._styler.prettify(df_ret)

        return df_ret


class OverallThreeCalculator():
    """三维总体答案占比 """

    def __init__(self, df, metric_col, metric_type, dict_extra={}, styler=None, dict_config={}):
        self._df = df
        self._styler = styler
        self._metric_col = metric_col
        self._metric_type = metric_type
        self._dict_extra = dict_extra
        self._dict_config = dict_config

    def calculate(self):
        # 各学历下的三维占比
        measure_name = parse_measure_name(self._metric_type)
        forcus_cols = [measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]]
        forcus_cols.append(self._metric_col)
        for key in self._dict_extra.keys():
            df_combines = []
            for col in self._dict_extra[key]:
                df_five = OverallFiveCalculator(self._df, col, self._metric_col,
                                                self._metric_type, self._styler).calculate()
                df_three = df_five[forcus_cols]
                df_three.insert(0, key, col)
                df_combines.append(df_three)

            df_combines = pd.concat(df_combines, sort=False)
            if self._dict_config:
                df_combines.loc[:, key] = df_combines.loc[:, key].map(self._dict_config)
            df_t = df_combines.pivot_table(index=key,
                                           columns='_12',
                                           values=[measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]])
            df_t.fillna(0, inplace=True)
            # df_t.reset_index(inplace=True)
            return df_t


class GrpThreeCalculator():
    """三维分组答案占比"""

    def __init__(self, df, grp_cols, metric_type, dict_extra={},
                 styler=None, dict_config={}):
        self._df = df
        self._styler = styler
        self._grp_cols = grp_cols
        self._metric_type = metric_type
        self._dict_extra = dict_extra
        self._dict_config = dict_config

    def calculate(self):
        measure_name = parse_measure_name(self._metric_type)
        forcus_cols =list(self._grp_cols)
        forcus_cols.extend([measure_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]])
        for key in self._dict_extra.keys():
            df_combines = None
            for col in self._dict_extra[key]:
                df_grp = GrpFiveCalculator(self._df, col, self._grp_cols,
                                           self._metric_type, self._styler).calculate()
                df_three = df_grp[forcus_cols]
                col_name = self._dict_config[col]
                df_three.rename(columns={
                    measure_name: measure_name + '_' + col_name,
                    CONFIG.MEAN_COLUMN[-1]: CONFIG.MEAN_COLUMN[-1] + '_' + col_name,
                    CONFIG.MEAN_COLUMN[2]: CONFIG.MEAN_COLUMN[2] + '_' + col_name
                }, inplace=True)
                if df_combines is None:
                    df_combines = df_three
                else:
                    df_combines = pd.merge(df_combines, df_three,how='inner', on=self._grp_cols)

            df_combines[measure_name + '_总体' + key] = df_combines[[col for col in df_combines.columns
                                                                   if str(col).find(measure_name) >= 0]].apply(
                lambda x: x.mean(), axis=1)
            df_combines[CONFIG.MEAN_COLUMN[-1] + '_总体' + key] = df_combines[[col for col in df_combines.columns
                                                                             if str(col).find(
                    CONFIG.MEAN_COLUMN[-1]) >= 0]].apply(
                lambda x: x.mean(), axis=1)
            df_combines[CONFIG.MEAN_COLUMN[2] + '_总体' + key] = df_combines[[col for col in df_combines.columns
                                                                            if str(col).find(
                    CONFIG.MEAN_COLUMN[2]) >= 0]].apply(
                lambda x: x.max(), axis=1)

            if "任课教师评价" == key:
                df_private = df_combines[[col for col in df_combines.columns if str(col).find('专业') >= 0]]
                df_public = df_combines[[col for col in df_combines.columns if str(col).find('公共') >= 0]]

                df_combines[measure_name + '_专业总评价'] = df_private[[col for col in df_private.columns
                                                                   if str(col).find(measure_name) >= 0]].apply(
                    lambda x: x.mean(), axis=1)
                df_combines[CONFIG.MEAN_COLUMN[-1] + '_专业总评价'] = df_private[[col for col in df_private.columns
                                                                             if str(col).find(
                        CONFIG.MEAN_COLUMN[-1]) >= 0]].apply(
                    lambda x: x.mean(), axis=1)
                df_combines[CONFIG.MEAN_COLUMN[2] + '_专业总评价'] = df_private[[col for col in df_private.columns
                                                                            if str(col).find(
                        CONFIG.MEAN_COLUMN[2]) >= 0]].apply(
                    lambda x: x.max(), axis=1)
                df_combines[measure_name + '_公共总评价'] = df_public[[col for col in df_public.columns
                                                                  if str(col).find(measure_name) >= 0]].apply(
                    lambda x: x.mean(), axis=1)
                df_combines[CONFIG.MEAN_COLUMN[-1] + '_公共总评价'] = df_public[[col for col in df_public.columns
                                                                            if str(col).find(
                        CONFIG.MEAN_COLUMN[-1]) >= 0]].apply(
                    lambda x: x.mean(), axis=1)
                df_combines[CONFIG.MEAN_COLUMN[2] + '_公共总评价'] = df_public[[col for col in df_public.columns
                                                                           if str(col).find(
                        CONFIG.MEAN_COLUMN[2]) >= 0]].apply(
                    lambda x: x.max(), axis=1)

            df_combines.fillna(0, inplace=True)
            df_combines=df_combines.set_index(self._grp_cols)
            df_combines.columns = pd.MultiIndex.from_tuples([tuple(c.split('_')) for c in df_combines.columns])
            df_combines.reset_index(inplace=True)
            return df_combines


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
            if not df_rate.empty:
                df_combines.append(df_rate)
        # Concatenate everything into a single DataFrame
        df_combines = pd.concat(df_combines, sort=False)
        df_combines.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)

        # combine overal
        df_overal = formula_five_rate(self._df, self._tgt_col, self._metric_type)
        df_overal.insert(0, self._metric_col, CONFIG.TOTAL_COLUMN)
        df_combines = df_combines.append(df_overal)
        df_combines.fillna(0, inplace=True)

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            df_combines = self._styler.prettify(df_combines)
        return df_combines

    def multi_calculate(self, multi_cols, sheet_name, dict_config):
        if not isinstance(multi_cols, list):
            raise Exception('OverallFiveCalculator.multi_calculate '
                            '需要列表类型，multi_cols：{}'.format(multi_cols))
        df_combines = []
        # step2：循环值进行计算
        for col in multi_cols:
            df_rate = formula_five_rate(self._df, col, self._metric_type)
            df_rate.insert(0, sheet_name, col)
            df_combines.append(df_rate)
        # Concatenate everything into a single DataFrame
        df_combines = pd.concat(df_combines, sort=False)
        df_combines[sheet_name] = df_combines[sheet_name].map(dict_config)
        df_combines.fillna(0, inplace=True)

        multi_style = MultiOverallStyle()
        if "任课教师评价" == sheet_name:
            df_private = df_combines[df_combines[sheet_name].isin(['专业课教师教学态度', '专业课教师教学水平'])]
            df_publid = df_combines[df_combines[sheet_name].isin(['公共课教师教学态度', '公共课教师教学水平'])]

            df_private_s = formulas_overall(df_private, [sheet_name], 'max')
            df_private_s[sheet_name] = '专业总体'

            df_publid_s = formulas_overall(df_publid, [sheet_name], 'max')
            df_publid_s[sheet_name] = '公共总体'

            df_combine_s = formulas_overall(df_combines, sheet_name, 'max')
            df_combine_s[sheet_name] = '总体任课教师评价'
            df_combines = pd.concat([df_private, df_private_s, df_publid, df_publid_s, df_combine_s],
                                    ignore_index=True, sort=False)
        else:
            df_combines = multi_style.prettify(df_combines, sheet_name)

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
        df_combines = df_combines.append(df_overal)

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
        self._start = start
        self._period_num = period_num
        self._step = step

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
        df_combines = df_combines.append(df_overal)

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            df_combines = self._styler.prettify(df_combines)
        return df_combines


class AnswerRateCalculator(DataCalculator):
    def __init__(self, df, target_col, styler=None):
        super().__init__(df, target_col, styler)

    def calculate(self):
        df_overal = formula_rate(self._df, self._tgt_col)
        return df_overal


class OtherProvinceRate(DataCalculator):
    """外省就业流向"""

    def __init__(self, df, target_col, province, metric_col, styler=None):
        super().__init__(df, target_col, styler)
        self._province = province
        self._metric_col = metric_col

    def calculate(self):
        # step1：筛选出指标中的值
        ls_metric = list(set(self._df[self._metric_col]))
        df_combines = []
        # step2：循环值进行计算
        for where in ls_metric:
            df_where = self._df[self._df[self._metric_col] == where]
            print(df_where)
            df_rate = self.other_province(df_where)
            df_rate.insert(0, self._metric_col, where)
            df_combines.append(df_rate)
        # Concatenate everything into a single DataFrame
        df_combines = pd.concat(df_combines, sort=False)
        df_combines.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)

        # combine overal
        df_overal = self.other_province(self._df)
        df_overal.insert(0, self._metric_col, CONFIG.TOTAL_COLUMN)
        df_combines = df_combines.append(df_overal)

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            df_combines = self._styler.prettify(df_combines)
        return df_combines

    def other_province(self, df):
        # 外地生源数据
        df_other_prov = df[df['A1-A'] != self._province]
        # 答题总人数
        not_birth_count = df_other_prov[self._tgt_col].count()
        print(not_birth_count)
        # 外地生源本地就业人数 省内就业
        not_birth_local_count = df_other_prov[df_other_prov[self._tgt_col] == self._province][self._tgt_col].count()
        not_birth_local_rate = (not_birth_local_count / not_birth_count).round(decimals=CONFIG.DECIMALS6)

        # 外地生源回生源地就业人数 回生源所在地就业
        not_birth_birth_count = df_other_prov[df_other_prov['A1-A'] == df_other_prov[self._tgt_col]][
            self._tgt_col].count()
        not_birth_birth_rate = (not_birth_birth_count / not_birth_count).round(decimals=CONFIG.DECIMALS6)

        df_rate = pd.DataFrame({'回生源所在地就业': [not_birth_birth_rate],
                                '其他省份就业': [1 - not_birth_local_rate - not_birth_birth_rate],
                                '省内就业': [not_birth_local_rate],
                                CONFIG.RATE_COLUMN[2]: not_birth_count})
        return df_rate


class ProvinceRate(DataCalculator):
    """省内就业流向"""

    def __init__(self, df, target_col, province, metric_col, styler=None):
        super().__init__(df, target_col, styler)
        self._province = province
        self._metric_col = metric_col

    def calculate(self):
        # step1：筛选出指标中的值
        ls_metric = list(set(self._df[self._metric_col]))
        df_combines = []
        # step2：循环值进行计算
        for where in ls_metric:
            df_where = self._df[self._df[self._metric_col] == where]
            df_rate = self.province(df_where)
            df_rate.insert(0, self._metric_col, where)
            df_combines.append(df_rate)
        # Concatenate everything into a single DataFrame
        df_combines = pd.concat(df_combines, sort=False)
        df_combines.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)

        # combine overal
        df_overal = self.province(self._df)
        df_overal.insert(0, self._metric_col, CONFIG.TOTAL_COLUMN)
        df_combines = df_combines.append(df_overal)

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            df_combines = self._styler.prettify(df_combines)
        return df_combines

    def province(self, df):
        # 外地生源数据
        df_prov = df[df['A1-A'] == self._province]
        # 答题总人数
        birth_count = df_prov[self._tgt_col].count()
        # 生源地在本地就业人数
        birth_value_count = df_prov[df_prov[self._tgt_col] == self._province][self._tgt_col].count()
        # 生源地当地比
        birth_value_rate = (birth_value_count / birth_count).round(CONFIG.DECIMALS6)
        df_rate = pd.DataFrame({'省内就业': [birth_value_rate],
                                '省外就业': [1 - birth_value_rate],
                                CONFIG.RATE_COLUMN[2]: birth_count})
        return df_rate


class TopNCalculator(DataCalculator):
    """合并取top n"""

    def __init__(self, df, target_col, top=5, styler=None):
        super().__init__(df, target_col, styler)
        self._top = top

    def calculate(self):
        df_rate = formula_rate(self._df, self._tgt_col, self._top)
        df_combine = formate_row_combine(df_rate, combin_name=self._tgt_col)
        combine_name = CONFIG.DICT_SUBJECT[self._tgt_col]
        df_combine.rename(columns={self._tgt_col: combine_name,
                                   CONFIG.RATE_COLUMN[2]: combine_name + CONFIG.RATE_COLUMN[2]})
        print(df_combine)
        return df_combine


class GrpTopNCalculator(DataCalculator):
    """分组合并取top n"""

    def __init__(self, df, target_col, grp_cols, top=5, styler=None, has_overal=False):
        super().__init__(df, target_col, styler)
        self._grp_cols = grp_cols
        self._top = top
        self._has_overal = has_overal

    def calculate(self):
        df_grp_rate = formula_rate_grp_top(self._df, self._tgt_col, self._grp_cols, self._top)
        combine_name = CONFIG.DICT_SUBJECT[self._tgt_col]
        df_combine = formate_grp_row_combine(df_grp_rate, array_grps=self._grp_cols,
                                             combin_name=combine_name)
        if self._has_overal:
            df_overal = formula_rate(self._df, self._tgt_col, self._top)
            df_overal = formate_row_combine(df_overal, combin_name=combine_name)
            df_combine = pd.concat([df_combine, df_overal], sort=False)
            df_combine.iloc[-1, 0:len(self._grp_cols)] = CONFIG.TOTAL_COLUMN
        return df_combine


class MultiRateCalculator(DataCalculator):
    def __init__(self, df, target_col, metric_col, styler=None, dict_config=None):
        super().__init__(df, target_col, styler)
        self._metric_col = metric_col
        self._dict_config = dict_config

    def calculate(self):

        # step1 答题总人数
        answer_count = multi_answer_count(self._df, self._tgt_col)
        # step2 结果集
        multi_column = multi_columns(self._df, self._tgt_col)
        df_relative = self._df[multi_column]
        key = []
        result = []
        for col in df_relative.columns:
            key.append(col)
            result.append(df_relative[col].count())
        df_result = pd.DataFrame({CONFIG.RATE_COLUMN[0]: key,
                                  CONFIG.RATE_COLUMN[1]: result})
        df_result[CONFIG.RATE_COLUMN[2]] = answer_count
        df_result[CONFIG.RATE_COLUMN[-1]] = (df_result[CONFIG.RATE_COLUMN[1]] / df_result[CONFIG.RATE_COLUMN[2]]).round(
            decimals=CONFIG.DECIMALS6)
        df_result.fillna(0, inplace=True)
        df_result.sort_values([CONFIG.RATE_COLUMN[-1]], ascending=[0], inplace=True)
        df_result.loc[:, CONFIG.RATE_COLUMN[0]] = df_result.loc[:, CONFIG.RATE_COLUMN[0]].map(self._dict_config)

        print(df_result)
        return df_result

    def degree_cal(self):
        # step1：筛选出指标中的值
        ls_metric = list(set(self._df[self._metric_col]))
        df_combines = []
        # step2：循环值进行计算
        for where in ls_metric:
            df_where = self._df[self._df[self._metric_col] == where]
            df_rate = MultiRateCalculator(df_where, self._tgt_col, self._metric_col,
                                          dict_config=self._dict_config).calculate()
            df_rate.insert(0, self._metric_col, where)
            df_combines.append(df_rate)
        # Concatenate everything into a single DataFrame
        df_combines = pd.concat(df_combines, sort=False)
        df_combines.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)

        # combine overal
        df_overal = MultiRateCalculator(self._df, self._tgt_col, self._metric_col,
                                        dict_config=self._dict_config).calculate()
        df_overal.insert(0, self._metric_col, CONFIG.TOTAL_COLUMN)
        df_combines = df_combines.append(df_overal)
        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            df_combines = self._styler.prettify(df_combines)
        return df_combines


class EmpFeatureCalculator(DataCalculator):
    """
    多纬度，多条件查询，结果列拼接展示，其中多条件目前只支持in；
    eg [[教育],[此列非教育的集合],[此列全部]]，则_col:[教育]

    """

    def __init__(self, df, target_col, combine_cols, dict_where, styler=None, dict_config=None):
        super().__init__(df, target_col, styler)
        self._dict_config = dict_config
        self._combine_cols = combine_cols
        self._dict_where = dict_where

    def calculate(self):
        if not isinstance(self._dict_where, dict):
            raise Exception("EmpFeatureCalculator.calculate 不支持的查询条件，where={}".format(self._dict_where))
        df_combine = []
        for where_col in self._dict_where:
            where = list(self._dict_where[where_col])
            df_where = self._df[self._df[self._tgt_col].isin(where)]
            if df_where.empty:
                continue
            df_init = pd.DataFrame()
            for col in self._combine_cols:
                df_top = TopNCalculator(df_where, col, top=5).calculate()
                print(df_top.columns)
                df_init = pd.concat([df_init, df_top], sort=False, axis=1)
            if self._tgt_col in df_init.columns:
                df_init.insert(0, self._tgt_col + '条件', where_col)
            else:
                df_init.insert(0, self._tgt_col, where_col)
            df_combine.append(df_init)
            print(df_combine)

        df_combines = pd.concat(df_combine, sort=False)
        return df_combines


class EmpCompetitiveCalculator(DataCalculator):
    """就业竞争力合并"""

    def __init__(self, df, target_col, dict_where, styler=None, dict_config=None):
        super().__init__(df, target_col, styler)
        self._dict_config = dict_config
        self._dict_where = dict_where

    def calculate(self):
        if not isinstance(self._dict_where, dict):
            raise Exception("EmpFeatureCalculator.calculate 不支持的查询条件，where={}".format(self._dict_where))
        df_combine = []
        for where_col in self._dict_where:
            where = list(self._dict_where[where_col])
            df_where = self._df[self._df[self._tgt_col].isin(where)]
            df_init = pd.DataFrame()
            # 就业率
            df_emp_rate = formula_employe_rate(df_where)
            df_emp_rate.rename(columns={CONFIG.RATE_COLUMN[2]: '就业率' + CONFIG.RATE_COLUMN[2]}, inplace=True)
            df_init = pd.concat([df_init, df_emp_rate], sort=False, axis=1)
            # 薪酬
            df_mean = formula_mean(df_where, 'B6')
            df_mean.rename(columns={CONFIG.MEAN_COLUMN[-1]: '薪酬' + CONFIG.MEAN_COLUMN[-1],
                                    CONFIG.MEAN_COLUMN[2]: '薪酬' + CONFIG.MEAN_COLUMN[2]}, inplace=True)
            df_init = pd.concat([df_init, df_mean], sort=False, axis=1)
            df_join = pd.DataFrame()
            combine_cols = ['B9-1', 'B7-1', 'B7-2', 'B7-3', 'B7-4', 'B8']
            for col in combine_cols:
                metric_type = CONFIG.SPECIAL_SUBJECT_TYPE[col]
                metric_name = parse_measure_name(metric_type)
                df_t = formula_five_rate(df_where, col, metric_type)
                df_t = df_t.loc[:, [metric_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]]]
                df_t.drop_duplicates(inplace=True)
                df_t.rename(columns={
                    metric_name: CONFIG.SPECIAL_SUBJECT[col],
                    CONFIG.MEAN_COLUMN[-1]: CONFIG.SPECIAL_SUBJECT[col] + CONFIG.MEAN_COLUMN[-1],
                    CONFIG.MEAN_COLUMN[2]: CONFIG.SPECIAL_SUBJECT[col] + CONFIG.MEAN_COLUMN[2]
                }, inplace=True)

                df_join = pd.concat([df_join, df_t], sort=False, axis=1)
            # 离职率
            df_demission = formate_rate_t(formula_rate(df_where, 'B10-1'))
            df_demission["离职率"] = 0
            for col in CONFIG.DIMISSION_COLUMNS:
                if col in df_demission.columns:
                    df_demission.loc[:, "离职率"] = df_demission.loc[:, "离职率"] + df_demission.loc[:, col]
            df_demission = df_demission.loc[:, ["离职率", CONFIG.RATE_COLUMN[2]]]
            df_demission.rename(columns={CONFIG.RATE_COLUMN[2]: "离职率" + CONFIG.RATE_COLUMN[2]}, inplace=True)
            df_join = pd.concat([df_join, df_demission], axis=1, sort=False)
            df_init.insert(0, self._tgt_col, where_col)
            df_join.insert(0, self._tgt_col, where_col)
            df_init = pd.merge(df_init, df_join, on=self._tgt_col, how='left')
            df_combine.append(df_init)
        df_combines = pd.concat(df_combine, sort=False)
        return df_combines


class EmpCompetitiveGrpCalculator(DataCalculator):
    """就业竞争力合并"""

    def __init__(self, df, grp_cols, styler=None, dict_config=None):
        super().__init__(df, None, styler)
        self._dict_config = dict_config
        self._grp_cols = grp_cols

    def calculate(self):
        # 就业率
        df_emp_rate = GrpEmpRate(self._df, None, self._grp_cols).calculate()
        df_emp_rate.rename(columns={CONFIG.RATE_COLUMN[2]: '就业率' + CONFIG.RATE_COLUMN[2]}, inplace=True)
        # 薪酬
        df_mean = GrpMeanCalculator(self._df, 'B6', self._grp_cols).calculate()
        df_mean.rename(columns={CONFIG.MEAN_COLUMN[-1]: '薪酬' + CONFIG.MEAN_COLUMN[-1],
                                CONFIG.MEAN_COLUMN[2]: '薪酬' + CONFIG.MEAN_COLUMN[2]}, inplace=True)
        df_combine = pd.merge(df_emp_rate, df_mean, how='left', on=self._grp_cols)

        combine_cols = ['B9-1', 'B7-1', 'B7-2', 'B7-3', 'B7-4', 'B8']
        for col in combine_cols:
            metric_type = CONFIG.SPECIAL_SUBJECT_TYPE[col]
            metric_name = parse_measure_name(metric_type)
            df_t = GrpFiveCalculator(self._df, col, self._grp_cols, metric_type).calculate()
            sub_cols = [metric_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]]
            sub_cols.extend(self._grp_cols)
            df_t = df_t.loc[:, sub_cols]
            df_t.drop_duplicates(inplace=True)
            df_t.rename(columns={
                metric_name: CONFIG.SPECIAL_SUBJECT[col],
                CONFIG.MEAN_COLUMN[-1]: CONFIG.SPECIAL_SUBJECT[col] + CONFIG.MEAN_COLUMN[-1],
                CONFIG.MEAN_COLUMN[2]: CONFIG.SPECIAL_SUBJECT[col] + CONFIG.MEAN_COLUMN[2]
            }, inplace=True)

            df_combine = pd.merge(df_combine, df_t, how='left', on=self._grp_cols)
        # 离职率
        df_demission = GrpRateCalculator(self._df, 'B10-1', self._grp_cols,
                                         {"离职率": ["1次", "2次", "3次及以上"]}).calculate()
        sub_cols = ["离职率", CONFIG.RATE_COLUMN[2]]
        sub_cols.extend(self._grp_cols)
        df_demission = df_demission[sub_cols]
        df_demission.rename(columns={CONFIG.RATE_COLUMN[2]: "离职率" + CONFIG.RATE_COLUMN[2]}, inplace=True)
        df_combine = pd.merge(df_combine, df_demission, how='left', on=self._grp_cols)

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            df_combine = self._styler.prettify(df_combine, self._grp_cols)

        return df_combine


class FiveConditionCalculator(DataCalculator):
    """五维条件查询"""

    def __init__(self, df, target_col, dict_where, multi_cols, metric_type, sheet_name, styler=None, dict_config=None):
        super().__init__(df, target_col, styler)
        self._dict_config = dict_config
        self._dict_where = dict_where
        self._metric_type = metric_type
        self._multi_cols = multi_cols
        self._sheet_name = sheet_name

    def calculate(self):
        if not isinstance(self._dict_where, dict):
            raise Exception("EmpFeatureCalculator.calculate 不支持的查询条件，where={}".format(self._dict_where))
        df_combine = []
        for where_col in self._dict_where:
            where = list(self._dict_where[where_col])
            df_where = self._df[self._df[self._tgt_col].isin(where)]
            df_five = OverallFiveCalculator(df_where, None, None,
                                            self._metric_type, self._styler).multi_calculate(self._multi_cols,
                                                                                             self._sheet_name,
                                                                                             self._dict_config)
            df_five.insert(0, self._tgt_col, where_col)
            df_combine.append(df_five)
        df_combines = pd.concat(df_combine, sort=False)

        return df_combines


class SchoolEvelutionCalcutor(DataCalculator):
    """学校总体评价"""

    def __init__(self, df, target_col, dict_where, styler=None, dict_config=None):
        super().__init__(df, target_col, styler)
        self._dict_config = dict_config
        self._dict_where = dict_where

    def calculate(self):
        if not isinstance(self._dict_where, dict):
            raise Exception("EmpFeatureCalculator.calculate 不支持的查询条件，where={}".format(self._dict_where))
        df_combine = []

        metric_name = parse_measure_name(CONFIG.ANSWER_TYPE_SATISFY)
        for where_col in self._dict_where:
            where = list(self._dict_where[where_col])
            df_where = self._df[self._df[self._tgt_col].isin(where)]
            # 母校满意度
            df_t = formula_five_rate(df_where, 'H7', CONFIG.ANSWER_TYPE_SATISFY)
            df_t = df_t.loc[:, [metric_name, CONFIG.MEAN_COLUMN[-1], CONFIG.MEAN_COLUMN[2]]]
            df_t.drop_duplicates(inplace=True)
            df_t.rename(columns={metric_name: "母校" + metric_name,
                                 CONFIG.MEAN_COLUMN[-1]: "母校满意度" + CONFIG.MEAN_COLUMN[-1],
                                 CONFIG.RATE_COLUMN[2]: "母校满意度" + CONFIG.RATE_COLUMN[2]}, inplace=True)

            # 母校推荐度
            df_recommend = formate_rate_t(formula_rate(df_where, 'H8'))
            df_recommend = df_recommend.loc[:, [CONFIG.ANSWER_RECOMMED[0], CONFIG.RATE_COLUMN[2]]]
            df_recommend.rename(columns={CONFIG.ANSWER_RECOMMED[0]: "母校推荐度",
                                         CONFIG.RATE_COLUMN[2]: "母校推荐度" + CONFIG.RATE_COLUMN[2]}, inplace=True)
            df_init = pd.concat([df_t, df_recommend], axis=1, sort=False)

            df_init.insert(0, self._tgt_col, where_col)
            df_combine.append(df_init)
        df_combines = pd.concat(df_combine, sort=False)
        return df_combines


class AbilityDistribution(DataCalculator):
    def __init__(self, df, target_col, dict_config, styler=None):
        super().__init__(df, target_col, styler)
        self._dict_config = dict_config

    def calculate(self):
        df_ability = ability_distribution(self._df, self._tgt_col)
        df_ability.loc[:, CONFIG.RATE_COLUMN[0]] = df_ability.loc[:, CONFIG.RATE_COLUMN[0]].map(self._dict_config)
        df_ability.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)

        return df_ability


class StudyCalculator(DataCalculator):
    """求学比列"""

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
            count = df_where['A2'].count()
            df_rate[CONFIG.RATE_COLUMN[2]] = count
            df_rate[CONFIG.RATE_COLUMN[-1]] = (df_rate[CONFIG.RATE_COLUMN[1]] / df_rate[CONFIG.RATE_COLUMN[2]]).round(
                decimals=CONFIG.DECIMALS6)
            df_rate = formate_rate_t(df_rate)
            if not df_rate.empty:
                df_rate.insert(0, self._metric_col, where)
                df_combines.append(df_rate)
        # 拼接后排序
        df_combines = pd.concat(df_combines, sort=False)
        df_combines.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)

        # combine overal
        df_overal = formula_rate(self._df, self._tgt_col)
        count = self._df['A2'].count()
        df_overal[CONFIG.RATE_COLUMN[2]] = count
        df_overal[CONFIG.RATE_COLUMN[-1]] = (df_overal[CONFIG.RATE_COLUMN[1]] / df_overal[CONFIG.RATE_COLUMN[2]]).round(
            decimals=CONFIG.DECIMALS6)
        df_overal = formate_rate_t(df_overal)

        df_overal.insert(0, self._metric_col, CONFIG.TOTAL_COLUMN)
        df_combines = df_combines.append(df_overal)
        df_combines.fillna(0, inplace=True)

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            df_combines = self._styler.prettify(df_combines)
        return df_combines


class SelfEmpCalculator(DataCalculator):
    """自主创业比列"""

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
            df_self = df_rate[df_rate[CONFIG.RATE_COLUMN[0]] == CONFIG.A2_ANSWER[1]]
            if df_self.empty:
                df_self = pd.DataFrame({CONFIG.RATE_COLUMN[0]: [CONFIG.A2_ANSWER[1]],
                                        CONFIG.RATE_COLUMN[1]: [0],
                                        CONFIG.RATE_COLUMN[-1]: [0]
                                        })
                df_self[CONFIG.RATE_COLUMN[2]] = df_rate[CONFIG.RATE_COLUMN[2]].head(1)

            df_self.insert(0, self._metric_col, where)
            df_combines.append(df_self)
        # 拼接后排序
        df_combines = pd.concat(df_combines, sort=False)
        df_combines.sort_values(CONFIG.RATE_COLUMN[2], ascending=0, inplace=True)

        # combine overal
        df_overal = formula_rate(self._df, self._tgt_col)
        df_overal = df_overal[df_overal[CONFIG.RATE_COLUMN[0]] == CONFIG.A2_ANSWER[1]]
        df_overal.insert(0, self._metric_col, CONFIG.TOTAL_COLUMN)
        df_combines = df_combines.append(df_overal)
        df_combines.fillna(0, inplace=True)

        # if styler object be set, apply style
        if isinstance(self._styler, AnalysisResultStyler):
            df_combines = self._styler.prettify(df_combines)
        return df_combines


class ObjectiveSizeCalculator(DataCalculator):
    """客观数据规模占比"""

    def __init__(self, df, target_col, styler=None):
        super().__init__(df, target_col, styler)

    def calculate(self):
        df_overal = formula_rate(self._df, self._tgt_col)
        print(df_overal)
        df_s = pd.DataFrame({
            CONFIG.RATE_COLUMN[0]: [CONFIG.TOTAL_COLUMN],
            CONFIG.RATE_COLUMN[1]: [df_overal[CONFIG.RATE_COLUMN[1]].sum()],
            CONFIG.RATE_COLUMN[-1]: [df_overal[CONFIG.RATE_COLUMN[-1]].sum()],
        })
        df_combines = pd.concat([df_overal, df_s], sort=False)

        if isinstance(self._styler, AnalysisResultStyler):
            df_combines = self._styler.prettify(df_combines, CONFIG.RATE_COLUMN[0])
        return df_combines


class ObjectiveGrpSizeCalculator(DataCalculator):
    """客观数据规模占比"""

    def __init__(self, df, target_col, grp_cols, styler=None):
        super().__init__(df, target_col, styler)
        self._grp_cols = grp_cols

    def calculate(self):
        df_overal = formula_grp_rate(self._df, self._tgt_col, self._grp_cols)

        return df_overal
