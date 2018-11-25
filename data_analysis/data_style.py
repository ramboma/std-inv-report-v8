import pandas as pd
class AnalysisResultStyler(object):
    def __init__(self):
        pass

    @staticmethod
    def prettify(base,append,axis=0):
        raise Exception('method not implement')


class AppendOverall(AnalysisResultStyler):

    @staticmethod
    def prettify(base,append,axis=0):
        base=pd.concat([base,append], ignore_index=True, sort=True, axis=axis)


class LookingBStyler(AnalysisResultStyler):

    @staticmethod
    def prettify(df):
        pass


class LookingCStyler(AnalysisResultStyler):

    @staticmethod
    def prettify(df):
        pass

