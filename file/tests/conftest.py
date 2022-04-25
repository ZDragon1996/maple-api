import pytest
from rest_framework.test import APIClient
from file.classes.file import File
from pathlib import Path


default_django_path = 'file/files/file_test_location/test.csv'
default_ext = '.xlsx'


@pytest.fixture
def api_client():
    return APIClient()


def delete_target_file(file_obj):
    before_target_path = file_obj.target_file_path
    path_obj = Path(before_target_path)
    target_file_exists = path_obj.exists()
    if target_file_exists:
        path_obj.unlink(before_target_path)


@pytest.fixture
def file_func():
    def wrapper(django_path=default_django_path, cls=File, target_ext=default_ext):
        obj = cls(django_path=django_path, target_ext=target_ext)
        # remove target_file in the test location before calling the methods
        delete_target_file(obj)
        return obj
    return wrapper


@pytest.fixture
def default_file_obj():
    file_obj = File(default_django_path)
    # remove target_file in the test location before calling the methods
    delete_target_file(file_obj)
    return file_obj
