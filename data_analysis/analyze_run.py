
from data_analysis.data_extract import *
from data_analysis.data_calculate import *
from data_analysis.data_style import *
from data_analysis.result_write import *
from data_analysis.data_analyze import *
from data_cleansing.logging import *

logger = get_logger(__name__)

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
            logger.info("{} report finished".format(name))
        except Exception as e:
            # log error message to log file
            # write user friendly error file
            # normal exit for next analyzer running
            logger.info("{} report failed, fail reason:{}".format(name,str(e)))

            tip_file = os.path.join(self._write.folder, name + '.txt')
            with open(tip_file, 'w') as f:
                f.write('{} 报表生成是发生错误，产生错误原因:{}'.format(name, str(e)))
        finally:
            pass
