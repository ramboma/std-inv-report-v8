import pandas as pd
import data_analysis.config as CONFIG


class AnalysisResultStyler(object):
    def __init__(self):
        pass

    @staticmethod
    def prettify(base, append, axis=0):
        raise Exception('method not implement')


class OverallProvotStyler(AnalysisResultStyler):
    """总体 行专列 按学历索引"""

    @staticmethod
    def prettify(df):
        rel_cols=[CONFIG.RATE_COLUMN[0],CONFIG.RATE_COLUMN[2],CONFIG.RATE_COLUMN[-1],"_12"]
        for col in rel_cols:
            if col not in df.columns:
                raise ("行转列时，格式不支持，需要列{}".format(CONFIG.RATE_COLUMN[0]))
        # 比例转置
        df_t = df.pivot_table(CONFIG.RATE_COLUMN[-1], index="_12",
                                   columns=CONFIG.RATE_COLUMN[0])
        if CONFIG.RATE_COLUMN[2] in df.columns:
            # 答题总人数
            df_overall = df[CONFIG.RATE_COLUMN[2]]
            df_t[CONFIG.RATE_COLUMN[2]] = df_overall
        df_t.reset_index(inplace=True)
        return df_t

class AppendOverall(AnalysisResultStyler):

    @staticmethod
    def prettify(base, append, axis=0):
        base = pd.concat([base, append], ignore_index=True, sort=True, axis=axis)


class LookingBStyler(AnalysisResultStyler):

    @staticmethod
    def prettify(df):
        pass


class LookingCStyler(AnalysisResultStyler):

    @staticmethod
    def prettify(df):
        pass
