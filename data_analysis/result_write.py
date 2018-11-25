import os
import pandas as pd
import openpyxl as xl
from openpyxl.styles import numbers as numStyle


class AnalysisResultWriter(object):
    def __init__(self, folder):
        self._folder = folder

    @property
    def folder(self):
        if self._folder[-1] != os.sep:
            self._folder = self._folder + os.sep
        else:
            self._folder = self._folder
        return self._folder

    def write_new_sheet(self, book_name, sheet_name, df):
        try:
            file = os.path.join(self.folder, book_name)
            writer = pd.ExcelWriter(file)
            if not os.path.exists(file):
                df.to_excel(writer, sheet_name, index=None)
            else:
                book = xl.load_workbook(writer.path)
                writer.book = book
                df.to_excel(excel_writer=writer, sheet_name=sheet_name, index=None)
            writer.save()
        except Exception as e:
            raise ("文件写入时，发生异常，异常：{}".format(e.__str__()))
        finally:
            writer.close()

    def write_new_book(self, book_name, df_dict):
        for sheet_name in df_dict:
            self.write_new_sheet(book_name, sheet_name, df_dict[sheet_name])
