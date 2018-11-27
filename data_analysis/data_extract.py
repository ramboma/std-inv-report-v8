import data_analysis.config as CONFIG


class DataExtractor(object):
    def __init__(self, df, answer_cols):
        self._df = df
        self._answer_cols = answer_cols

    def extract_ref_cols(self):
        """提取相关列"""
        if self._df.empty:
            raise ('结果集为空')
        relative_cols = list(CONFIG.BASE_COLUMN)
        relative_cols.extend(self._answer_cols)
        # 去重
        relative_cols = list(set(relative_cols))
        # 列是否在结果集中
        for col in relative_cols:
            if col not in self._df.columns:
                raise ("列{}不存在，无法进行计算".format(col))
        answers = self._df[relative_cols]
        return answers
