from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from image.classes.image import Image
from pathlib import Path
import pytest
import shutil
import redis
import os


default_django_path = 'file/files/file_test_location/nodelete_image_test.jpg'
default_source_test_file_location = os.path.join(
    settings.MEDIA_ROOT, 'file/files/nodelete_test_files').replace('/', '\\')
default_target_test_file_location = os.path.join(
    settings.MEDIA_ROOT, 'file/files/file_test_location').replace('/', '\\')


target_paths = [default_target_test_file_location]


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


def delete_target_file(image_obj):
    before_target_path = image_obj.target_image_path
    path_obj = Path(before_target_path)
    target_file_exists = path_obj.exists()
    if target_file_exists:
        path_obj.unlink(before_target_path)


@pytest.fixture
def default_image_obj(get_test_files):
    def wrapper(default_django_path):
        get_test_files()
        image_obj = Image(default_django_path)
        # remove target_file in the test location before calling the methods
        delete_target_file(image_obj)
        return image_obj
    return wrapper


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
def default_upload_image_and_conversion(api_client, default_image_obj):
    def wrapper(url_route, django_path=default_django_path):
        image_obj = default_image_obj(django_path)
        test_image_path = image_obj.source_image_path

        with open(test_image_path, 'rb') as f:
            file = SimpleUploadedFile(Path(django_path).name, f.read())
            response = api_client.post(
                url_route, data={'image': file})
        if not hasattr(response.data, 'target_name'):
            return response
        file_path = os.path.join(
            image_obj.media_root, 'file', 'files', response.data['target_name'])
        final_image_exists = os.path.exists(file_path)
        assert final_image_exists == True
        return response
    return wrapper
