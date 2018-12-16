import pandas as pd
import data_analysis.config as CONFIG


class AnalysisResultStyler(object):
    def __init__(self):
        pass

    @staticmethod
    def prettify(base, append, axis=0):
        raise Exception('method not implement')


class DegreeIndexStyler(AnalysisResultStyler):
    """总体 行专列 按学历索引"""

    @staticmethod
    def prettify(df):
        rel_cols = [CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[2], CONFIG.RATE_COLUMN[-1], "_12"]
        for col in rel_cols:
            if col not in df.columns:
                raise ("行转列时，格式不支持，需要列{}".format(CONFIG.RATE_COLUMN[0]))
        # 比例转置
        df_t = df.pivot_table(index=["_12", CONFIG.RATE_COLUMN[2]], columns=CONFIG.RATE_COLUMN[0],
                              values=CONFIG.RATE_COLUMN[-1])
        df_t.fillna(0, inplace=True)
        df_t.reset_index(inplace=True)
        return df_t


class AnswerIndexStyler(AnalysisResultStyler):
    """总体 行专列 按答案索引"""

    @staticmethod
    def prettify(df):
        rel_cols = [CONFIG.RATE_COLUMN[0], CONFIG.RATE_COLUMN[1],
                    CONFIG.RATE_COLUMN[2], CONFIG.RATE_COLUMN[-1], "_12"]
        for col in rel_cols:
            if col not in df.columns:
                raise ("行转列时，格式不支持，需要列{}".format(CONFIG.RATE_COLUMN[0]))
        # 比例转置
        df_t = df.pivot_table(index=CONFIG.RATE_COLUMN[0],
                              columns='_12', values=[CONFIG.RATE_COLUMN[1], CONFIG.RATE_COLUMN[-1]])
        df_t.fillna(0, inplace=True)
        df_t.reset_index(inplace=True)
        return df_t


class AppendOverall(AnalysisResultStyler):
    """总计时，num 求和，其他求均值"""
    @staticmethod
    def prettify(df, grp_cols):
        nums = []
        others = []
        cols = df.columns
        for col in cols:
            if col in grp_cols:
                continue
            if col.find(CONFIG.RATE_COLUMN[2]) > 0:
                nums.append(col)
            else:
                others.append(col)

        df_num = df.loc[:, nums].agg(['sum'])
        df_mean = df.loc[:, others].agg(['mean'])
        df_num.reset_index(inplace=True)
        df_mean.reset_index(inplace=True)
        df_sum = pd.concat([df_num, df_mean], axis=1)
        nums.extend(others)
        df_sum = df_sum[nums]
        df_combine = pd.concat([df, df_sum], sort=False)
        df_combine.iloc[-1,0:len(grp_cols)]=CONFIG.TOTAL_COLUMN
        return df_combine

class LookingBStyler(AnalysisResultStyler):

    @staticmethod
    def prettify(df):
        pass
