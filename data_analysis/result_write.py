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
                df.to_excel(writer, sheet_name, index=isinstance(df.columns, pd.MultiIndex))
            else:
                book = xl.load_workbook(writer.path)
                writer.book = book
                df.to_excel(excel_writer=writer, sheet_name=sheet_name, index=isinstance(df.columns, pd.MultiIndex))
            writer.save()
        except Exception as e:
            raise ("文件写入时，发生异常，异常：{}".format(e.__str__()))
        finally:
            writer.close()

    def write_new_book(self, book_name, df_dict):
        for sheet_name in df_dict:
            self.write_new_sheet(book_name, sheet_name, df_dict[sheet_name])

    def formate_percent(self, file_path, sheet_name, percent_cols, head=1):
        wbook = xl.load_workbook(file_path)
        sheet = wbook[sheet_name]
        max_row = sheet.max_row
        max_col = sheet.max_column

        for i in range(1, max_col + 1):
            colTag = xl.utils.get_column_letter(i)
            sheet.column_dimensions[colTag].width = 10

            if sheet.cell(row=head, column=i).value in percent_cols:
                sheet.column_dimensions[colTag].number_format = numStyle.FORMAT_PERCENTAGE_00
                for j in range(head + 1, max_row + 1):
                    sheet.cell(row=j, column=i).number_format = numStyle.FORMAT_PERCENTAGE_00
            elif str(sheet.cell(row=head, column=i).value).find("均值")>0:
                sheet.column_dimensions[colTag].number_format = numStyle.FORMAT_NUMBER_00
                for j in range(head + 1, max_row + 1):
                    sheet.cell(row=j, column=i).number_format = numStyle.FORMAT_NUMBER_00

        wbook.save(file_path)
        wbook.close()