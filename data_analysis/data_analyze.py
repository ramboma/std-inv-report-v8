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


def common_grp_anaysis(df, question_col, class_name, sheet_name, dic_grp={}):
    degree_col = "_12"
    result = dict()

    # 筛选出学历 如果为多学历需要计算总体
    ls_metric = list(set(df[degree_col]))
    if len(ls_metric) > 1:
        if dic_grp:
            for key in dic_grp:
                result["总体毕业生" + key + sheet_name] = class_name(df, question_col,
                                                                list(dic_grp[key])).calculate()
        else:
            result["总体毕业生各学院" + sheet_name] = class_name(df, question_col,
                                                         [CONFIG.BASE_COLUMN[0]]).calculate()
            result["总体毕业生各专业" + sheet_name] = class_name(df, question_col,
                                                         [CONFIG.BASE_COLUMN[0],
                                                          CONFIG.BASE_COLUMN[1]]).calculate()

    for metric in ls_metric:
        df_filter = df[df[degree_col] == metric]
        if not df_filter.empty:
            if dic_grp:
                for key in dic_grp:
                    result[metric + key + sheet_name] = class_name(df_filter, question_col,
                                                                   list(dic_grp[key])).calculate()
            else:
                result[metric + "各学院" + sheet_name] = class_name(df_filter, question_col,
                                                                 [CONFIG.BASE_COLUMN[0]]).calculate()
                result[metric + "各专业" + sheet_name] = class_name(df_filter, question_col,
                                                                 [CONFIG.BASE_COLUMN[0],
                                                                  CONFIG.BASE_COLUMN[1]]).calculate()
    return result


class ValueRateDataAnalyzer(DataAnalyzer):
    """答案占比，行专利 包含 总体、各学历的学院、专业 答案占比"""
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
        result["总体毕业生" + sheet_name] = OverallRateCalculator(df,
                                                             self._question_col,
                                                             self._degree_col,
                                                             do_t=True).calculate()
        # 筛选出学历 如果为多学历需要计算总体
        df_grp = common_grp_anaysis(df, self._question_col, GrpRateCalculator, sheet_name)
        result.update(df_grp)
        return result


class SimpleValueRateDataAnalyzer(DataAnalyzer):
    """单独计算答案占比，结果集不合并多学历(参考就业分布模板)"""

    def __init__(self, df, question_col, dict_config=None, do_combine=False):
        super().__init__(df, dict_config)
        self._question_col = question_col
        self._do_combine = do_combine

    def analyse(self):
        if self._dict_config is None:
            raise ("缺少配置文件，无法解析sheet name")
        sheet_name = self._dict_config[self._question_col]
        # find out necessary data columns
        de = DataExtractor(self._df, self._question_col)
        df = de.extract_ref_cols()

        result = dict()
        ls_metric = list(set(df[self._degree_col]))
        result["总体毕业生" + sheet_name] = AnswerRateCalculator(df, self._question_col).calculate()
        if len(ls_metric) > 1:
            if self._do_combine:
                result["总体毕业生各学院" + sheet_name] = GrpTopNCalculator(df, self._question_col,
                                                                    [CONFIG.BASE_COLUMN[0]]).calculate()
                result["总体毕业生各专业" + sheet_name] = GrpTopNCalculator(df, self._question_col,
                                                                    [CONFIG.BASE_COLUMN[0],
                                                                     CONFIG.BASE_COLUMN[1]]).calculate()
        for metric in ls_metric:
            df_filter = df[df[self._degree_col] == metric]
            result[metric + sheet_name] = AnswerRateCalculator(df_filter,
                                                               self._question_col).calculate()

            result[metric + "各学院" + sheet_name] = GrpTopNCalculator(df_filter, self._question_col,
                                                                    [CONFIG.BASE_COLUMN[0]]).calculate()
            result[metric + "各专业" + sheet_name] = GrpTopNCalculator(df_filter, self._question_col,
                                                                    [CONFIG.BASE_COLUMN[0],
                                                                     CONFIG.BASE_COLUMN[1]]).calculate()
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
        dict_college = self.degree_five_analysis({"学院": [CONFIG.BASE_COLUMN[0]]}, sheet_name)
        result.update(dict_college)
        dict_major = self.degree_five_analysis({"专业": [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]]}, sheet_name)
        result.update(dict_major)
        return result

    def degree_five_analysis(self, dict_grp, sheet_name):
        if dict_grp:
            result = {}
            for key in dict_grp:
                # find out necessary data columns
                rel_cols = list(dict_grp[key])
                rel_cols.append(self._question_col)
                de = DataExtractor(self._df, rel_cols)
                df = de.extract_ref_cols()

                # 筛选出学历 如果为多学历需要计算总体
                ls_metric = list(set(df[self._degree_col]))
                if len(ls_metric) > 1:
                    result["总体毕业生各" + key + sheet_name] = GrpFiveCalculator(df, self._question_col,
                                                                            dict_grp[key],
                                                                            self._metric_type).calculate()
                for metric in ls_metric:
                    df_filter = df[df[self._degree_col] == metric]
                    if not df_filter.empty:
                        result[metric + key + sheet_name] = GrpFiveCalculator(df_filter, self._question_col,
                                                                              dict_grp[key],
                                                                              self._metric_type).calculate()
            return result
        else:
            pass


########### 就业率及就业状态 start
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

        style = DegreeIndexStyler()
        result["总体毕业去向"] = OverallRateCalculator(df, self._question_col,
                                                 self._degree_col, do_t=True,
                                                 extra={"灵活就业": ["自主创业", "自由职业"]}
                                                 ).calculate()

        dict_grp_emp_rate = common_grp_anaysis(df, self._question_col, GrpEmpRate, "就业率")
        dict_grp_emp_go = common_grp_anaysis(df, self._question_col, GrpRateCalculator, "毕业去向")
        result.update(dict_grp_emp_rate)
        result.update(dict_grp_emp_go)
        return result


class WorkOptionDataAnalyzer(ValueRateDataAnalyzer):
    """就业机会"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'A3', dict_config)


class NonEmployeeDataAnalyzer(OverallAnswerIndexDataAnalyzer):
    """未就业报告"""

    def __init__(self, df, dic_config=None):
        super().__init__(df, ['C1', 'C2'], dic_config)


########### 就业率及就业状态 end


############# 就业竞争力 start
class WorkStabilityAnalyzer(DataAnalyzer):
    """工作稳定性"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, dict_config)
        self._question_col = 'B10-1'

    def analyse(self):
        de = DataExtractor(self._df, [self._question_col, self._degree_col])
        df = de.extract_ref_cols()

        if self._dict_config is None:
            raise ("缺少配置文件，无法解析sheet name")
        sheet_name = self._dict_config[self._question_col]
        result = dict()
        result["总体" + sheet_name] = OverallRateCalculator(df, self._question_col,
                                                          self._degree_col, do_t=True,
                                                          extra={"离职率": ["1次", "2次", "3次及以上"]}
                                                          ).calculate()
        result.update(common_grp_anaysis(df, self._question_col, GrpRateCalculator, sheet_name))

        # 更换工作原因
        result.update(OverallAnswerIndexDataAnalyzer(self._df, ["B10-2"], self._dict_config).analyse())
        return result


class JobMeetAnalyzer(FiveRateDataAnalyzer):
    """职业期待吻合度"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'B8', CONFIG.ANSWER_TYPE_MEET, dict_config)


class JobSatisfyAnalyzer(FiveRateDataAnalyzer):
    """就业满意度"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'B7-1', CONFIG.ANSWER_TYPE_SATISFY, dict_config)

    def analyse(self):
        result = super().analyse()

        # 添加三维拼接
        array_subj = ['B7' + '-' + str(sub) for sub in range(1, 5)]
        sheet_name = "对工作各方面满意情况"

        de = DataExtractor(self._df, array_subj)
        df = de.extract_ref_cols()

        result["总体毕业生" + sheet_name] = OverallThreeCalculator(df,
                                                              self._degree_col,
                                                              CONFIG.ANSWER_TYPE_SATISFY,
                                                              {sheet_name: array_subj}).calculate()
        # 筛选出学历 如果为多学历需要计算总体
        ls_metric = list(set(df[self._degree_col]))
        if len(ls_metric) > 1:
            result["总体毕业生各学院" + sheet_name] = GrpThreeCalculator(df, [CONFIG.BASE_COLUMN[0]],
                                                                 self._metric_type,
                                                                 {sheet_name: array_subj}).calculate()
            result["总体毕业生各专业" + sheet_name] = GrpThreeCalculator(df,
                                                                 [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]],
                                                                 self._metric_type,
                                                                 {sheet_name: array_subj}).calculate()

        for metric in ls_metric:
            df_filter = df[df[self._degree_col] == metric]
            result[metric + "各学院" + sheet_name] = GrpThreeCalculator(df_filter, [CONFIG.BASE_COLUMN[0]],
                                                                     self._metric_type,
                                                                     {sheet_name: array_subj}).calculate()
            result[metric + "各专业" + sheet_name] = GrpThreeCalculator(df_filter,
                                                                     [CONFIG.BASE_COLUMN[0], CONFIG.BASE_COLUMN[1]],
                                                                     self._metric_type,
                                                                     {sheet_name: array_subj}).calculate()
        return result


class MajorRelativeAnalyzer(FiveRateDataAnalyzer):
    """专业相关度"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'B9-1', CONFIG.ANSWER_TYPE_RELATIVE, dict_config)

    def analyse(self):
        result = super().analyse()

        # add B9-2
        dict_append = OverallAnswerIndexDataAnalyzer(self._df, ['B9-2'], self._dict_config).analyse()
        result.update(dict_append)
        return result


class IncomeAnalyzer(DataAnalyzer):
    """月均收入"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, dict_config)
        self._question_col = 'B6'

    def analyse(self):
        de = DataExtractor(self._df, [self._question_col, self._degree_col])
        df = de.extract_ref_cols()
        df = df[df['A2'] == CONFIG.A2_ANSWER[0]]
        result = dict()
        start = 2000
        period_n = 4
        steps = [500, 1000, 1500, 2000]
        for step in steps:
            sheet_name = '毕业生月均收入及薪酬分布_' + str(step)
            result[sheet_name] = AnswerPeriodCalculator(df, self._question_col, self._degree_col,
                                                        start, period_n, step).calculate()
        if self._dict_config is None:
            raise ("缺少配置文件，无法解析sheet name")
        sheet_name = self._dict_config[self._question_col]

        df_grp = common_grp_anaysis(df, self._question_col, GrpMeanCalculator, "就业职业月均收入")
        result.update(df_grp)
        return result


########### 就业竞争力 end


########### 就业分布 start

class EmpJobAnalyzer(SimpleValueRateDataAnalyzer):
    """就业职业分布"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'B4-B', dict_config, do_combine=True)

    def analyse(self):
        # 职业答题比例
        result = super().analyse()

        sheet_name = self._dict_config[self._question_col]
        # find out necessary data columns
        de = DataExtractor(self._df, [self._question_col, 'B6', 'B9-1', 'B7-1'])
        df = de.extract_ref_cols()
        # 职业均值
        dic_grp = {"就业职业": ['B4-B']}
        df_grp = common_grp_anaysis(df, 'B6', GrpMeanCalculator,
                                    "月均收入", dic_grp)
        result.update(df_grp)
        # 专业相关度差异分析
        df_grp = FiveRateDataAnalyzer(df,
                                      'B9-1',
                                      CONFIG.ANSWER_TYPE_RELATIVE,
                                      None).degree_five_analysis(dic_grp, "专业相关度差异分析")
        result.update(df_grp)

        # 就业满意度差异分析
        df_grp = FiveRateDataAnalyzer(df,
                                      'B7-1',
                                      CONFIG.ANSWER_TYPE_SATISFY,
                                      None).degree_five_analysis(dic_grp, "就业满意度差异分析")
        result.update(df_grp)

        return result


class EmpIndurstryAnalyzer(SimpleValueRateDataAnalyzer):
    """就业行业分布"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'B5-B', dict_config, do_combine=True)

    def analyse(self):
        # 就业行业比例
        result = super().analyse()

        sheet_name = self._dict_config[self._question_col]
        # find out necessary data columns
        de = DataExtractor(self._df, [self._question_col, 'B6', 'B9-1', 'B7-1'])
        df = de.extract_ref_cols()
        # 收入均值
        dic_grp = {"就业行业": ['B5-B']}
        df_grp = common_grp_anaysis(df, 'B6', GrpMeanCalculator,
                                    "月均收入", dic_grp)
        result.update(df_grp)
        # 专业相关度差异分析
        df_grp = FiveRateDataAnalyzer(df,
                                      'B9-1',
                                      CONFIG.ANSWER_TYPE_RELATIVE,
                                      None).degree_five_analysis(dic_grp, "专业相关度差异分析")
        result.update(df_grp)

        # 就业满意度差异分析
        df_grp = FiveRateDataAnalyzer(df,
                                      'B7-1',
                                      CONFIG.ANSWER_TYPE_SATISFY,
                                      None).degree_five_analysis(dic_grp, "就业满意度差异分析")
        result.update(df_grp)

        return result


class EmpRegionAnalyzer(SimpleValueRateDataAnalyzer):
    """就业地区分布"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'B3-A', dict_config, do_combine=True)

    def analyse(self):
        # 地区答题比例
        result = super().analyse()

        sheet_name = self._dict_config[self._question_col]
        # find out necessary data columns
        de = DataExtractor(self._df, [self._question_col,'_6', 'B6', 'B9-1', 'B7-1', 'B3-B', 'A1-A'])
        df = de.extract_ref_cols()
        # 职业均值
        dic_grp = {"就业地区": ['B3-B']}
        df_grp = common_grp_anaysis(df, 'B6', GrpMeanCalculator,
                                    "月均收入", dic_grp)
        result.update(df_grp)

        # 省内就业城市
        province = get_province(df)
        df_city = df[df['B3-A'] == province]
        df_province = SimpleValueRateDataAnalyzer(df_city, 'B3-B',
                                                  self._dict_config, True).analyse()
        result.update(df_province)
        # 省内就业城市月均收入
        df_province_income = common_grp_anaysis(df_city, 'B6', GrpMeanCalculator, "月均收入", dic_grp)
        result.update(df_province_income)

        # 省内生源就业地区流向
        result["省内生源就业地区流向"]=ProvinceRate(df, self._question_col,
                                          province, self._degree_col).calculate()

        # 省外生源就业地区流向
        result["省外生源就业地区流向"]=OtherProvinceRate(df, self._question_col,
                                               province, self._degree_col).calculate()

        return result

class EmpIndurstryTypeSizeAnalyzer(SimpleValueRateDataAnalyzer):
    """就业单位类型和规模"""

    def __init__(self, df, dict_config=None):
        super().__init__(df, 'B1', dict_config, do_combine=True)

    def analyse(self):
        # 就业行业比例
        result = super().analyse()
        sheet_name = self._dict_config[self._question_col]
        # find out necessary data columns
        de = DataExtractor(self._df, [self._question_col, 'B6', 'B9-1', 'B7-1'])
        df = de.extract_ref_cols()
        # 收入均值
        dic_grp = {"就业单位类型": ['B1']}
        df_grp = common_grp_anaysis(df, 'B6', GrpMeanCalculator,
                                    "月均收入", dic_grp)
        result.update(df_grp)
        # 专业相关度差异分析
        df_grp = FiveRateDataAnalyzer(df,
                                      'B9-1',
                                      CONFIG.ANSWER_TYPE_RELATIVE,
                                      None).degree_five_analysis(dic_grp, "专业相关度差异分析")
        result.update(df_grp)

        # 就业满意度差异分析
        df_grp = FiveRateDataAnalyzer(df,
                                      'B7-1',
                                      CONFIG.ANSWER_TYPE_SATISFY,
                                      None).degree_five_analysis(dic_grp, "就业满意度差异分析")
        result.update(df_grp)

        # 就业单位规模
        dict_size=ValueRateDataAnalyzer(self._df,'B2',self._dict_config).analyse()
        result.update(dict_size)

        return result

def get_province(data):
    subject = '_6'
    province = data.loc[0, subject]
    if pd.isnull(province) or len(str(province)) == 0:
        raise Exception('未获取到学校所属省份')
    else:
        return province


########### 就业分布 end

#######求职过程 start
class EmpDifficultAnalyzer(DataAnalyzer):
    """求职过程"""
    def __init__(self, df, dict_config=None):
        df_filter = df[df['A2'].isin([CONFIG.A2_ANSWER[0], CONFIG.A2_ANSWER[2]])]
        super().__init__(df_filter, dict_config)
        self._question_col ='D2'

    def analyse(self):
        result = {}
        sheet_name = self._dict_config[self._question_col]
        # find out necessary data columns
        de = DataExtractor(self._df, [self._question_col, 'D1'])
        df = de.extract_ref_cols()
        result[sheet_name]=OverallAnswerIndexDataAnalyzer(self._df, [self._question_col], self._dict_config).analyse()
        # 筛选出学历 如果为多学历需要计算总体
        ls_metric = list(set(self._df[self._degree_col]))
        if len(ls_metric) > 1:
            result["总体毕业生各专业" + sheet_name] = GrpTopNCalculator(self._df, self._question_col,
                                                              [CONFIG.BASE_COLUMN[0],
                                                              CONFIG.BASE_COLUMN[1]]).calculate()

        for metric in ls_metric:
            df_filter = self._df[self._df[self._degree_col] == metric]
            if not df_filter.empty:
                result[metric + "各专业" + sheet_name] = GrpTopNCalculator(df_filter, self._question_col,
                                                                     [CONFIG.BASE_COLUMN[0],
                                                                      CONFIG.BASE_COLUMN[1]]).calculate()
        sheet_name1=self._dict_config['D1']
        result[sheet_name1]=OverallAnswerIndexDataAnalyzer(self._df, ['D1'], self._dict_config).analyse()
        return result
#######求职过程 end


#######自主创业报告 start
class SelfEmpAnalyzer(DataAnalyzer):
    """自主创业报告"""
    def __init__(self, df, dict_config=None):
        super().__init__(df, dict_config)

    def analyse(self):
        result = {}
        df_a2=AnswerRateCalculator(self._df,'A2').calculate()
        result['自主创业比例']=df_a2[df_a2[CONFIG.RATE_COLUMN[0]] == CONFIG.A2_ANSWER[1]]

        style=AnswerIndexStyler()
        result['创业原因']=MultiRateCalculator(self._df,'G3',style).degree_cal()
        result['创业资金来源']=MultiRateCalculator(self._df,'G4',style).degree_cal()
        result['创业困难']=MultiRateCalculator(self._df,'G5',style).degree_cal()
        result['创业行业与所学专业相关度']=OverallFiveCalculator(self._df,'G2',
                                                     self._degree_col,
                                                     CONFIG.ANSWER_TYPE_RELATIVE).calculate()
        sheet_name='创业行业'
        ls_metric = list(set(self._df[self._degree_col]))
        if len(ls_metric) > 1:
            result["总体毕业生" + sheet_name] = AnswerRateCalculator(self._df, 'G1-B').calculate()

        for metric in ls_metric:
            df_filter = self._df[self._df[self._degree_col] == metric]
            if not df_filter.empty:
                result[metric + sheet_name] = AnswerRateCalculator(df_filter, 'G1-B').calculate()
        return result

#######自主创业报告 end



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
    # analyze 1

    #analyzer_collection['社团活动'] = EvelutionH4_RAnalyzer(df, dic_config)
    #analyzer_collection['母校学风认可度'] = EvelutionAcademicAnalyzer(df, dic_config)
    #analyzer_collection['教育教学总体评价'] = EvelutionH4_TAnalyzer(df, dic_config)
    #analyzer_collection['实践教学的评价'] = EvelutionH4_SAnalyzer(df, dic_config)
    #analyzer_collection['未就业分析'] = NonEmployeeDataAnalyzer(df, dic_config)
    analyzer_collection['自主创业']=SelfEmpAnalyzer(df,dic_config)
    analyzer_collection['求职过程']=EmpDifficultAnalyzer(df,dic_config)

    runner.run_batch(analyzer_collection)

    pass


if __name__ == '__main__':
    test()
