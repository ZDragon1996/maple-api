from datetime import datetime
import django
from django.conf import settings
from numpy import isin
from file.classes.file import File
from file.classes.csvfile import CSVFile
import os
import pytest


@pytest.mark.django_db
class TestFileClass:

    # file_obj is a fixture
    def test_get_full_path_check_path_and_returns_str(self, default_file_obj, file_func):
        file = default_file_obj
        csv_file = file_func(cls=CSVFile)
        path = file.get_full_path()
        csv_path = file.get_full_path()

        # validate File class
        assert isinstance(path, str) == True
        assert file.source_file_ext == '.csv'
        assert file.target_file_ext == '.xlsx'
        assert not path == True
        assert os.path.exists(path) == True

        # validate CSVFile class
        assert isinstance(csv_path, str) == True
        assert csv_file.source_file_ext == '.csv'
        assert csv_file.target_file_ext == '.xlsx'
        assert not csv_path == True
        assert os.path.exists(csv_path) == True

    def test_get_file_deli_and_returns_str(self, file_func):
        empty_file = file_func(
            django_path='file/files/file_test_location/empty_test.csv')
        comma_file = file_func(
            django_path='file/files/file_test_location/comma_test.csv')
        pipe_file = file_func(
            django_path='file/files/file_test_location/pipe_test.csv')
        colon_file = file_func(
            django_path='file/files/file_test_location/colon_test.csv')
        semicolon_file = file_func(
            django_path='file/files/file_test_location/semicolon_test.csv')
        unknown_file = file_func(
            django_path='file/files/file_test_location/unknown_test.csv')

        empty_file_output = empty_file.get_file_deli()
        comma_file_output = comma_file.get_file_deli()
        pipe_file_output = pipe_file.get_file_deli()
        colon_file_output = colon_file.get_file_deli()
        semicolon_file_output = semicolon_file.get_file_deli()
        unknown_file_output = unknown_file.get_file_deli()

        assert isinstance(empty_file_output, str)
        assert isinstance(comma_file_output, str)
        assert isinstance(pipe_file_output, str)
        assert isinstance(colon_file_output, str)
        assert isinstance(semicolon_file_output, str)
        assert isinstance(unknown_file_output, str)
        assert empty_file_output == ','
        assert comma_file_output == ','
        assert pipe_file_output == '|'
        assert colon_file_output == ':'
        assert semicolon_file_output == ';'
        assert unknown_file_output == 'unknown'

    def test_get_deli_count_returns_int(self, default_file_obj):
        empty_file_output = default_file_obj.get_deli_count('', ',')
        comma_file_output = default_file_obj.get_deli_count('a,b,c', ',')
        pipe_file_output = default_file_obj.get_deli_count('a|b|c', '|')
        colon_file_output = default_file_obj.get_deli_count('a:b:c', ':')
        semicolon_file_output = default_file_obj.get_deli_count('a;b;c', ';')
        unknown_file_output = default_file_obj.get_deli_count(
            'sdasdsadweq:|?', ',')

        assert isinstance(empty_file_output, int)
        assert isinstance(comma_file_output, int)
        assert isinstance(pipe_file_output, int)
        assert isinstance(colon_file_output, int)
        assert isinstance(semicolon_file_output, int)
        assert isinstance(unknown_file_output, int)
        assert empty_file_output == 0
        assert comma_file_output == 2
        assert pipe_file_output == 2
        assert colon_file_output == 2
        assert semicolon_file_output == 2
        assert unknown_file_output == 0

    def test_valid_deli_count_returns_bool(self, file_func):
        good_file = file_func(
            django_path='file/files/file_test_location/good_test.csv')
        bad_file = file_func(
            django_path='file/files/file_test_location/inconsistent_test.csv')
        empty_file = file_func(
            django_path='file/files/file_test_location/empty_test.csv')

        good_file_output = good_file.valid_deli_count()
        bad_file_output = bad_file.valid_deli_count()
        empty_file_output = empty_file.valid_deli_count()

        assert isinstance(good_file_output, bool)
        assert isinstance(bad_file_output, bool)
        assert isinstance(empty_file_output, bool)
        assert good_file_output == True
        assert bad_file_output == False
        assert empty_file_output == True

    def test_get_target_file_name_returns_str(self, default_file_obj):
        target_file_name = default_file_obj.get_target_file_name()

        assert isinstance(target_file_name, str)
        assert target_file_name == default_file_obj.target_file_name

    def test_get_file_size_returns_str(self, default_file_obj):
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        # source file
        file_info = default_file_obj.source_file_info
        file_size = default_file_obj.get_file_size(file_info)
        unit_in_output = any(unit in file_size for unit in units)

        assert isinstance(file_size, str)
        assert file_size == default_file_obj.source_file_size
        assert unit_in_output == True

    def test_get_file_mt_time_returns_datetime(self, default_file_obj):
        mft_time = default_file_obj.get_file_mt_time()

        assert isinstance(mft_time, datetime)
        assert mft_time == default_file_obj.source_file_mt_time
