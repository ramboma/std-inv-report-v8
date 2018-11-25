
from data_analysis.data_extract import *
from data_analysis.data_calculate import *
from data_analysis.data_style import *
from data_analysis.result_write import *
from data_analysis.data_analyze import *


class AnalyzeRunner(object):
    def __init__(self, writer):
        self._write = writer
        pass

    def run_batch(self, analyzer_collection):
        for name in analyzer_collection:
            self.run(analyzer_collection[name], name)

    def run(self, analyzer, name):
        try:
            result = analyzer.analyse()
            self._write.write_new_book('{}.xlsx'.format(name), result)
        except Exception as e:
            # log error message to log file
            # write user friendly error file
            # normal exit for next analyzer running
            print(e)
            pass
        finally:
            pass
