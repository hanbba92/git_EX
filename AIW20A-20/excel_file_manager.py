import os

import openpyxl
import pandas as pd
import win32com.client as win32


class ExcelFileManager:

    def file_write(self, title, file_name, data_list, header=[]):
        print('Creating Excel File...')
        excel_file = openpyxl.Workbook()
        excel_sheet = excel_file.active
        excel_sheet.title = title

        if len(header) != 0:
            excel_sheet.append(header)
        for data in data_list:
            excel_sheet.append(data)
        excel_file.save(file_name)
        excel_file.close()
        print('Excel File Creation Successful')

    def file_read(self, file_path):
        df = pd.read_excel(file_path, skiprows=1, header=None, engine='openpyxl')
        return df

    def file_name_read(self, file_path):
        # 다운로드 받은 파일 이름을 알아내 경로 반환
        file_path_slash = self.backslash_to_slash(file_path)
        file_name_list = os.listdir(file_path_slash)
        # 다운로드 1개 파일 -> 1개 파일만 읽음
        for file_name in file_name_list:
            if file_name.split('.')[1] == 'xls':
                path = self.xls_to_xlsx(file_path + '\\'+file_name)
                return self.backslash_to_slash(path)

    def xls_to_xlsx(self, file_path):
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        wb = excel.Workbooks.Open(file_path)

        wb.SaveAs(file_path + "x", FileFormat=51)  # FileFormat = 51 is for .xlsx extension
        wb.Close()  # FileFormat = 56 is for .xls extension
        excel.Application.Quit()
        return file_path.split('.')[0] + '.xlsx'

    def backslash_to_slash(self, path):
        return path.replace('\\', '/')

    def directory_empty(self, directory_path):
        file_path_slash = self.backslash_to_slash(directory_path)
        file_name_list = os.listdir(file_path_slash)
        for file_name in file_name_list:
            os.remove(file_path_slash + '/' + file_name)