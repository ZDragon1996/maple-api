from rest_framework import status
import pytest


route = '/api/image/image2sketch/'


@pytest.mark.django_db
class TestImageAPI:

    def test_if_image2sketch_returns_201(self, default_upload_image_and_conversion, clean_files):
        response = default_upload_image_and_conversion(route)
        assert response.status_code == status.HTTP_201_CREATED
        clean_files()

    def test_if_image2sketch_get_put_delete_returns405(self, validate_get_put_delete_call_returns_405):
        validate_get_put_delete_call_returns_405('/api/image/image2sketch/')

    def test_if_image2sketch_returns400(self, default_upload_image_and_conversion, clean_files):
        response = default_upload_image_and_conversion(
            route, django_path='file/files/file_test_location/nodelete_test.csv')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        clean_files()
