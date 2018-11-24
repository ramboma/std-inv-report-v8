

class DataExtractor(object):
    def __init__(self, df):
        self._df = df

    def extract_by_col_indexes(self, col_list):
        # raise Exception('method not implement')
        df_metrics = self._df.loc[:, col_list]




