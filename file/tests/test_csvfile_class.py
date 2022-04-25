from file.classes.csvfile import CSVFile
from pathlib import Path
from zipfile import ZipFile
import pytest
import pandas as pd


@pytest.fixture
def convert_file_test_setup(file_func):
    def wrapper(
        method_name,
        django_p1='file/files/file_test_location/test.csv',
        django_p2='file/files/file_test_location/inconsistent_test.csv',
        target_ext='.xlsx',
        target_ext2='.xlsx'
    ):
        # good csv setup
        good_csv_file = file_func(
            cls=CSVFile, django_path=django_p1, target_ext=target_ext)
        good_csv_method = getattr(good_csv_file, method_name)
        good_csv_file_output = good_csv_method()
        good_xlsx_file_exists = Path(good_csv_file.target_file_path).exists()

        # inconsistent csv setup
        inconsistent_csv_file = file_func(
            django_path=django_p2, cls=CSVFile, target_ext=target_ext2)
        inconsistent_csv_method = getattr(inconsistent_csv_file, method_name)
        inconsistent_csv_file_output = inconsistent_csv_method()
        inconsistent_xlsx_file_exists = Path(
            inconsistent_csv_file.target_file_path).exists()

        assert isinstance(good_csv_file_output, str)
        assert isinstance(inconsistent_csv_file_output, str)
        assert good_xlsx_file_exists == True
        assert inconsistent_xlsx_file_exists == True
        assert good_csv_file.target_file_ext == target_ext
        assert inconsistent_csv_file.target_file_ext == target_ext2
        return good_csv_file, inconsistent_csv_file
    return wrapper


class TestCSVFileClass:
    def test_convert_csv2xlsx_returns_str(self, convert_file_test_setup):
        convert_file_test_setup('convert_csv2xlsx')

    def test_convert_csv2xlsx_xlsxwriter_returns_str(self, convert_file_test_setup):
        convert_file_test_setup('convert_csv2xlsx_xlsxwriter')

    def test_convert_csv2xlsx_pd_returns_str(self, convert_file_test_setup):
        convert_file_test_setup('convert_csv2xlsx_pd')

    def test_convert_csv2txt_returns_str(self, convert_file_test_setup):
        convert_file_test_setup(
            'convert_csv2txt', target_ext='.txt', target_ext2='.txt')

    def test_convert_xlsx2csv_returns_str(self, convert_file_test_setup):
        # good xlsx file
        good_django_path = 'file/files/file_test_location/file_test.xlsx'
        three_sheets_django_path = 'file/files/file_test_location/file_three_sheets_test.xlsx'

        _, three_sheets_file = convert_file_test_setup(
            'convert_xlsx2csv',
            django_p1=good_django_path,
            django_p2=three_sheets_django_path,
            target_ext='.csv',
            target_ext2='.zip'
        )

        expected_file_count = len(pd.ExcelFile(
            three_sheets_file.source_file_path).sheet_names)
        with ZipFile(three_sheets_file.target_file_path, 'r') as zipfile:
            zip_file_count = len(zipfile.namelist())

        assert expected_file_count == zip_file_count
