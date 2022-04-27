from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status
from file.classes.file import File
from file.classes.csvfile import CSVFile
from pathlib import Path
import pytest
import redis
import shutil
import os

default_django_path = 'file/files/file_test_location/nodelete_test.csv'
default_source_test_file_location = os.path.join(
    settings.MEDIA_ROOT, 'file/files/nodelete_test_files').replace('/', '\\')
default_target_test_file_location = os.path.join(
    settings.MEDIA_ROOT, 'file/files/file_test_location').replace('/', '\\')
default_target_test_file_location2 = os.path.join(
    settings.MEDIA_ROOT, 'file/files').replace('/', '\\')
default_ext = '.xlsx'

target_paths = [default_target_test_file_location,
                default_target_test_file_location2]


@pytest.fixture
def api_client():
    redis.Redis().flushall()
    return APIClient()


@pytest.fixture
def get_test_files():
    def wrapper():
        for file_location in target_paths:
            for file in os.listdir(default_source_test_file_location):
                source_file_path = os.path.join(
                    default_source_test_file_location, file).replace('/', '\\')
                target_file_path = os.path.join(
                    file_location, file).replace('/', '\\')
                if not os.path.exists(target_file_path):
                    shutil.copy(source_file_path, target_file_path)
    return wrapper


@pytest.fixture
def clean_files():
    def wrapper():
        for file_location in target_paths:
            for file in os.listdir(file_location):
                file_path = os.path.join(
                    file_location, file).replace('/', '\\')
                if os.path.isfile(file_path):
                    os.remove(file_path)
    return wrapper


def delete_target_file(file_obj):
    before_target_path = file_obj.target_file_path
    path_obj = Path(before_target_path)
    target_file_exists = path_obj.exists()
    if target_file_exists:
        path_obj.unlink(before_target_path)


@pytest.fixture
def file_func(get_test_files):
    def wrapper(django_path=default_django_path, cls=File, target_ext=default_ext):
        get_test_files()
        obj = cls(django_path=django_path, target_ext=target_ext)
        # remove target_file in the test location before calling the methods
        delete_target_file(obj)
        return obj
    return wrapper


@pytest.fixture
def default_file_obj(get_test_files):
    get_test_files()
    file_obj = File(default_django_path)
    # remove target_file in the test location before calling the methods
    delete_target_file(file_obj)
    return file_obj


@pytest.fixture
def validate_get_put_delete_call_returns_405(api_client):
    def wrapper(route_path):
        response_get = api_client.get(route_path)
        response_put = api_client.put(route_path, data={})
        response_patch = api_client.patch(route_path, data={})
        response_delete = api_client.delete(route_path, data={})

        assert response_get.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_put.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_patch.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_delete.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    return wrapper


@pytest.fixture
def default_upload_file_and_conversion(api_client, file_func):
    def wrapper(url_route, django_path=default_django_path, target_ext='.xlsx'):
        file_obj = file_func(
            cls=CSVFile, django_path=django_path, target_ext=target_ext)
        test_csv_path = file_obj.source_file_path

        with open(test_csv_path, 'rb') as f:
            file = SimpleUploadedFile(os.path.basename(django_path), f.read())
            response = api_client.post(
                url_route, data={'file': file})
        if not hasattr(response.data, 'target_name'):
            return response
        file_path = os.path.join(
            file_obj.media_root, 'file', 'files', response.data['target_name'])
        xlsx_exists = os.path.exists(file_path)
        assert xlsx_exists == True
        return response
    return wrapper
