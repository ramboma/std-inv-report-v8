

class AnalysisResultWriter(object):
    def __init__(self, folder):
        self._folder = folder

    def write_new_sheet(self, book_name, sheet_name, df):
        pass

    def write_new_book(self, book_name, df_dict):
        for sheet_name in df_dict:
            # create new sheet
            pass
        # write to new book(excel file)
