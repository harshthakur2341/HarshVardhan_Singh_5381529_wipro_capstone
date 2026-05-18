import openpyxl, os

class ExcelReader:
    def __init__(self, file_path, sheet_name):
        self.file_path = os.path.join(os.getcwd(), file_path)
        self.sheet_name = sheet_name

    def get_data(self):
        workbook = openpyxl.load_workbook(self.file_path)
        sheet = workbook[self.sheet_name]
        data = []
        headers = [cell.value for cell in sheet[1]]
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if any(row):
                data.append(dict(zip(headers, row)))
        return data
