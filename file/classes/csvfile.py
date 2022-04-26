from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import bad_request
from rest_framework.response import Response
from file.classes.file import File
from file.custom_decorators.decorators import handle_invalid_file
from xlsxwriter import Workbook
from zipfile import ZipFile
from pathlib import Path
import pandas as pd
import csv
import os

# ==============================
# Validate Source File Type
# ==============================


def validate_source_file(file_name=None, expected_type=['.xlsx', '.xls']) -> bool:
    return True if Path(file_name).suffix in expected_type else False


class CSVFile(File):

    # ================================================
    # Pick conversion options for csv to xlsx
    # ================================================
    def convert_csv2xlsx(self) -> str:
        '''
        If the file delimiter is unknown or invalid delimiter count for the file, 
        uses the xlsx writer conversion approach; otherwise, 
        it uses the pandas module to convert the file.
        The reason behind this implementation is because of inconsistent data/column 
        count for each row. The data will be wiped using pandas module to convert 
        the file from csv to xlsx. 
        '''
        deli = self.get_file_deli()
        valid_deli_count = self.valid_deli_count()
        if deli != 'unknown' and valid_deli_count:
            return self.convert_csv2xlsx_pd()
        else:
            return self.convert_csv2xlsx_xlsxwriter()

# ================================================
#  csv to xlsx using xlsxwriter
# ================================================
    def convert_csv2xlsx_xlsxwriter(self) -> str:
        '''
        Using the xlsxwriter module to create an excel file, and then read through
        the csv file and write data in the excel file in xlsx format.
        '''
        print('converting using xlsxwriter')
        with Workbook(self.target_file_path) as workbook:
            worksheet = workbook.add_worksheet()
            with open(self.source_file_path, 'rt') as f:
                csv_reader = csv.reader(f)
                for r, row in enumerate(csv_reader):
                    for c, col in enumerate(row):
                        worksheet.write(r, c, col)
        return self.target_url_path

# ================================================
#  csv to xlsx using pandas ExcelWriter
# ================================================
    def convert_csv2xlsx_pd(self) -> str:
        '''
        Using the pandas module to create DataFrame obj, and then 
        convert csv file to xlsx format.
        '''
        df = pd.read_csv(self.source_file_path)
        excel_writer = pd.ExcelWriter(self.target_file_path)
        df.to_excel(excel_writer, index=False, engine='openpyxl')
        excel_writer.save()
        return self.target_url_path

# ==================
#  csv to txt
# ==================
    def convert_csv2txt(self) -> str:
        '''
        Read csv file and write the file in txt format.
        '''
        with open(self.source_file_path, 'rt') as rf, open(self.target_file_path, 'wt') as wf:
            lines = rf.readlines()
            wf.writelines(lines)
        return os.path.join(
            settings.API_MEDIA_ROOT_URL, self.django_path.replace(
                self.source_file_ext, self.target_file_ext))

# ==========================================
#  xlsx to csv or xls to csv using pandas
# ==========================================
    def convert_xlsx2csv(self) -> str:
        '''
        Using the pandas module using openpyxl,
        convert xlsx file to csv format. If xlsx file contains more than one sheet, 
        create multiple csv files and put them in a zip file.
        '''
        sheets_names = pd.ExcelFile(self.source_file_path).sheet_names
        sheets_count = len(sheets_names)

        zip_file_path = self.target_file_path.replace(
            self.target_file_ext, '.zip')
        zip_files = []

        for sheet_name in sheets_names:
            excel_df = pd.read_excel(
                self.source_file_path, sheet_name=sheet_name, dtype=object, index_col=None)

            if sheets_count > 1:
                file_path = self.target_file_path.replace(
                    self.target_file_ext, f'_{sheet_name}{self.target_file_ext}')
            else:
                file_path = self.target_file_path

            excel_df.to_csv(file_path, index=False, encoding='utf-8')
            zip_files.append(file_path)

        if sheets_count > 1:
            with ZipFile(zip_file_path, 'w') as zipfile:
                for file in zip_files:
                    arcname = os.path.basename(file)
                    zipfile.write(file, arcname=arcname)

        if os.path.exists(zip_file_path):
            return self.target_url_path.replace(
                self.target_file_ext, '.zip')

        return self.target_url_path
