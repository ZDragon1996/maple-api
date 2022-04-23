from django.conf import settings
from file.classes.file import File
from xlsxwriter import Workbook
import pandas as pd
import csv
import os


class CSVFile(File):
    def __init__(self, django_path) -> None:
        super().__init__(django_path)
        self.target_file_type = '.xlsx'
        self.target_file_name = self.handle_file_name(self.target_file_type)
        self.xlsx_path = self.full_path.replace('.csv', self.target_file_type)
        self.xlsx_django_path = self.django_path.replace(
            '.csv', self.target_file_type)
        self.xlsx_file_path = os.path.join(self.media_root, self.xlsx_path)
        self.xlsx_url_path = os.path.join(
            settings.API_MEDIA_ROOT_URL, self.xlsx_django_path)

    def convert_csv2xlsx(self):
        deli = self.get_file_deli()
        valid_deli_count = self.valid_deli_count()
        print(deli)
        print(valid_deli_count)
        if deli != 'unknown' and valid_deli_count:
            return self.convert_csv2xlsx_pd()
        else:
            return self.convert_csv2xlsx_xlsxwriter()

    def convert_csv2xlsx_xlsxwriter(self):
        print('converting using xlsxwriter')
        with Workbook(self.xlsx_file_path) as workbook:
            worksheet = workbook.add_worksheet()
            with open(self.full_path, 'rt') as f:
                csv_reader = csv.reader(f)
                for r, row in enumerate(csv_reader):
                    for c, col in enumerate(row):
                        worksheet.write(r, c, col)
        return self.xlsx_url_path

    def convert_csv2xlsx_pd(self):
        df = pd.read_csv(self.full_path)
        excel_writer = pd.ExcelWriter(self.xlsx_file_path)
        df.to_excel(excel_writer, index=False, engine='xlsxwriter')
        excel_writer.save()

        return self.xlsx_url_path

    def convert_csv2txt(self):
        with open(self.full_path, 'rt') as rf, open(self.full_path.replace('.csv', '.txt'), 'wt') as wf:
            lines = rf.readlines()
            wf.writelines(lines)
        return os.path.join(
            settings.API_MEDIA_ROOT_URL, self.django_path.replace(
                '.csv', '.txt'))
