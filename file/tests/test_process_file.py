from rest_framework.test import APIClient
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
import pytest
import os


@pytest.mark.django_db
class TestProcessFile:
    def test_if_csv2xlsx_saved_in_media_returns_201(self):

        test_csv_path = os.path.join(
            settings.MEDIA_ROOT, 'file/files/test.csv')

        client = APIClient()
        with open(test_csv_path, 'rb') as f:
            file = SimpleUploadedFile('test.csv', f.read())
            response = client.post(
                '/api/file/', data={'file': file})

        xlsx_exists = os.path.exists(test_csv_path.replace('.csv', '.xlsx'))

        assert response.status_code == status.HTTP_201_CREATED
        assert xlsx_exists == True
