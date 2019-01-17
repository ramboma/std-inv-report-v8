import data_analysis.config as CONFIG


class DataExtractor(object):
    def __init__(self, df, answer_cols, del_empty_col=None):
        self._df = df
        self._answer_cols = answer_cols
        self._del_empty_col=del_empty_col

    def extract_ref_cols(self):
        """提取相关列"""
        if self._df.empty:
            raise Exception('结果集为空')
        relative_cols = list(CONFIG.BASE_COLUMN)
        if isinstance(self._answer_cols, list):
            relative_cols.extend(self._answer_cols)
        else:
            relative_cols.append(self._answer_cols)
        # 去重
        relative_cols = list(set(relative_cols))
        # 列是否在结果集中
        for col in relative_cols:
            if col not in self._df.columns:
                raise Exception("列{}不存在，无法进行计算".format(col))
        answers = self._df[relative_cols]

        if self._del_empty_col is not None:
            # 将key为空的过滤
            answers.loc[:,self._del_empty_col] = answers[self._del_empty_col].fillna('DEL')
            answers = answers[answers[self._del_empty_col] != 'DEL']
        return answers

    def extract_objective_cols(self, base_cols):
        """提取客观数据相关列"""
        if self._df.empty:
            raise Exception('结果集为空')
        relative_cols = list(base_cols)
        if isinstance(self._answer_cols, list):
            relative_cols.extend(self._answer_cols)
        else:
            relative_cols.append(self._answer_cols)
        # 去重
        relative_cols = list(set(relative_cols))
        # 列是否在结果集中
        for col in relative_cols:
            if col not in self._df.columns:
                raise Exception("列{}不存在，无法进行计算".format(col))
        answers = self._df[relative_cols]

        if self._del_empty_col is not None:
            # 将key为空的过滤
            answers.loc[:, self._del_empty_col] = answers[self._del_empty_col].fillna('DEL')
            answers = answers[answers[self._del_empty_col] != 'DEL']
        return answers
