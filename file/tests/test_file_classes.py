import django
from django.conf import settings
from file.classes.file import File
from file.classes.csvfile import CSVFile
import os
import pytest


@pytest.fixture
def file_func():
    def wrapper(django_path='file/files/file_test_location/test.csv', cls=File):
        return cls(django_path)
    return wrapper

@pytest.fixture
def default_file_obj():
    return File('file/files/file_test_location/test.csv')

@pytest.mark.django_db
class TestFileClasses:

    # file_obj is a fixture
    def test_get_full_path_check_path_and_returns_str(self, default_file_obj, file_func):
        file = default_file_obj
        csv_file = file_func(cls=CSVFile)
        path = file.get_full_path()
        csv_path = file.get_full_path()

        # validate File class
        assert file.source_file_ext == '.csv'
        assert file.target_file_ext == '.xlsx'
        assert not path == True
        assert os.path.exists(path) == True
        assert isinstance(path, str) == True

        # validate CSVFile class
        assert csv_file.source_file_ext == '.csv'
        assert csv_file.target_file_ext == '.xlsx'
        assert not csv_path == True
        assert os.path.exists(csv_path) == True
        assert isinstance(csv_path, str) == True

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
        unknown_file_output = default_file_obj.get_deli_count('sdasdsadweq:|?', ',')

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
            django_path='file/files/file_test_location/bad_test.csv')
        empty_file = file_func(
            django_path='file/files/file_test_location/empty_test.csv')

        good_file_output = good_file.valid_deli_count()
        bad_file_output = bad_file.valid_deli_count()
        empty_file_output = empty_file.valid_deli_count()

        assert good_file_output == True
        assert bad_file_output == False
        assert empty_file_output == True
