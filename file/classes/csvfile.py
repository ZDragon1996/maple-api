from django.conf import settings
from file.classes.file import File
from xlsxwriter import Workbook
import pandas as pd
import csv
import os


class CSVFile(File):

    # ================================================
    # Pick conversion options for csv to xlsx
    # ================================================
    def convert_csv2xlsx(self):
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
    def convert_csv2xlsx_pd(self):
        '''
        Using the pandas module to create DataFrame obj, and then 
        convert csv file to xlsx format.
        '''
        df = pd.read_csv(self.source_file_path)
        excel_writer = pd.ExcelWriter(self.target_file_path)
        df.to_excel(excel_writer, index=False, engine='xlsxwriter')
        excel_writer.save()
        return self.target_url_path

# ==================
#  csv to txt
# ==================
    def convert_csv2txt(self):
        '''
        Read csv file and write the file in txt format.
        '''
        with open(self.source_file_path, 'rt') as rf, open(self.target_file_path, 'wt') as wf:
            lines = rf.readlines()
            wf.writelines(lines)
        return os.path.join(
            settings.API_MEDIA_ROOT_URL, self.django_path.replace(
                self.source_file_ext, self.target_file_ext))
