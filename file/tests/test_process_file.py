from rest_framework.test import APIClient
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
import pytest
import os
from file.classes.csvfile import File


@pytest.mark.django_db
class TestProcessFile:
    def test_if_csv2xlsx_saved_in_media_returns_201(self, api_client):
        django_path = 'file/files/test.csv'
        file_obj = File(django_path)
        test_csv_path = file_obj.source_file_path

        with open(test_csv_path, 'rb') as f:
            file = SimpleUploadedFile('test.csv', f.read())
            response = api_client.post(
                '/api/file/csv2xlsx/', data={'file': file})

        xlsx_exists = os.path.exists(file_obj.target_file_path)

        assert response.status_code == status.HTTP_201_CREATED
        assert xlsx_exists == True
