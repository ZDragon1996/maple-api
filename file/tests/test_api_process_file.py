from django.conf import settings
from rest_framework import status
import pytest
import os

default_django_path = 'file/files/nodelete_test.csv'


@pytest.mark.django_db
class TestProcessFile:
    # ========================================
    # Test 201 endpoint: /api/file/csv2xlsx/
    # ========================================
    def test_if_csv2xlsx_saved_in_media_returns_201(self, default_upload_file_and_conversion, clean_files):
        url_route = '/api/file/csv2xlsx/'
        response = default_upload_file_and_conversion(url_route)
        assert response.status_code == status.HTTP_201_CREATED
        clean_files()

# ========================================
# Test 201 endpoint: /api/file/csv2txt/
# ========================================
    def test_if_csv2txt_saved_in_media_returns_201(self, default_upload_file_and_conversion, clean_files):
        url_route = '/api/file/csv2txt/'
        target_ext = '.txt'
        response = default_upload_file_and_conversion(
            url_route, target_ext=target_ext)
        assert response.status_code == status.HTTP_201_CREATED
        clean_files()

# ========================================
# Test 201 endpoint: /api/file/xlsx2csv/
# ========================================
    def test_if_xlsx2csv_saved_in_media_returns_201(self, default_upload_file_and_conversion, clean_files):
        django_path = 'file/files/nodelete_test_111.xlsx'
        url_route = '/api/file/xlsx2csv/'
        target_ext = '.csv'
        response = default_upload_file_and_conversion(
            url_route, django_path=django_path, target_ext=target_ext)
        assert response.status_code == status.HTTP_201_CREATED
        clean_files()

# ========================================
# Test 201 endpoint: /api/file/xls2csv/
# ========================================
    def test_if_xls2csv_saved_in_media_returns_201(self, default_upload_file_and_conversion, clean_files):
        django_path = 'file/files/nodelete_file_example_XLS_10.xls'
        url_route = '/api/file/xlsx2csv/'
        target_ext = '.csv'
        response = default_upload_file_and_conversion(
            url_route, django_path=django_path, target_ext=target_ext)
        assert response.status_code == status.HTTP_201_CREATED
        clean_files()

# ========================================
# Test 201 endpoint: /api/file/xls2xlsx/
# ========================================
    def test_if_xls2xlsx_saved_in_media_returns_201(self, default_upload_file_and_conversion, clean_files):
        django_path = 'file/files/nodelete_file_example_XLS_10.xls'
        url_route = '/api/file/xls2xlsx/'
        target_ext = '.xlsx'
        response = default_upload_file_and_conversion(
            url_route, django_path=django_path, target_ext=target_ext)
        assert response.status_code == status.HTTP_201_CREATED
        clean_files()

# ========================================
# Test 201 endpoint: /api/file/txt2csv/
# ========================================
    def test_if_txt2csv_saved_in_media_returns_201(self, default_upload_file_and_conversion, clean_files):
        django_path = 'file/files/nodelete_test.txt'
        url_route = '/api/file/txt2csv/'
        target_ext = '.csv'
        response = default_upload_file_and_conversion(
            url_route, django_path=django_path, target_ext=target_ext)
        assert response.status_code == status.HTTP_201_CREATED
        clean_files()

# ========================================
# Test 201 endpoint: /api/file/txt2xlsx/
# ========================================
    def test_if_txt2xlsx_saved_in_media_returns_201(self, default_upload_file_and_conversion, clean_files):
        django_path = 'file/files/nodelete_file_test_txt.txt'
        url_route = '/api/file/txt2csv/'
        target_ext = '.xlsx'
        response = default_upload_file_and_conversion(
            url_route, django_path=django_path, target_ext=target_ext)
        assert response.status_code == status.HTTP_201_CREATED
        clean_files()

# ========================================
# Test 201 endpoint: /api/file/txt2xlsx/
# ========================================
    def test_if_txt2xlsx_saved_in_media_returns_201(self, default_upload_file_and_conversion, clean_files):
        django_path = 'file/files/nodelete_test.txt'
        url_route = '/api/file/txt2xlsx/'
        target_ext = '.xlsx'
        response = default_upload_file_and_conversion(
            url_route, django_path=django_path, target_ext=target_ext)
        assert response.status_code == status.HTTP_201_CREATED
        clean_files()

# ================================================
# Test 405: endpoint: /api/file/csv2xlsx/
# ================================================
    def test_if_csv2xlsx_get_put_delete_call_returns_405(self, validate_get_put_delete_call_returns_405):
        route = '/api/file/csv2xlsx/'
        validate_get_put_delete_call_returns_405(route)

# ================================================
# Test 405: endpoint: /api/file/csv2txt/
# ================================================
    def test_if_csv2txt_get_put_delete_call_returns_405(self, validate_get_put_delete_call_returns_405):
        route = '/api/file/csv2txt/'
        validate_get_put_delete_call_returns_405(route)

# ================================================
# Test 405: endpoint: /api/file/xlsx2csv/
# ================================================
    def test_if_xlsx2csv_get_put_delete_call_returns_405(self, validate_get_put_delete_call_returns_405):
        route = '/api/file/xlsx2csv/'
        validate_get_put_delete_call_returns_405(route)

# ================================================
# Test 405: endpoint: /api/file/xls2csv/
# ================================================
    def test_if_xls2csv_get_put_delete_call_returns_405(self, validate_get_put_delete_call_returns_405):
        route = '/api/file/xls2csv/'
        validate_get_put_delete_call_returns_405(route)

# ================================================
# Test 405: endpoint: /api/file/xls2xlsx/
# ================================================
    def test_if_xls2xlsx_get_put_delete_call_returns_405(self, validate_get_put_delete_call_returns_405):
        route = '/api/file/xls2xlsx/'
        validate_get_put_delete_call_returns_405(route)

# ================================================
# Test 405: endpoint: /api/file/txt2csv/
# ================================================
    def test_if_txt2csv_get_put_delete_call_returns_405(self, validate_get_put_delete_call_returns_405):
        route = '/api/file/txt2csv/'
        validate_get_put_delete_call_returns_405(route)

# ================================================
# Test 405: endpoint: /api/file/txt2xlsx/
# ================================================
    def test_if_txt2xlsx_get_put_delete_call_returns_405(self, validate_get_put_delete_call_returns_405):
        route = '/api/file/txt2xlsx/'
        validate_get_put_delete_call_returns_405(route)


# ================================================
# Test 400: endpoint: /api/file/csv2xlsx/
# ================================================

    def test_if_csv2xlsx_invalid_file_returns_400(self, default_upload_file_and_conversion):
        route = '/api/file/csv2xlsx/'
        django_path = 'file/files/file_test_location/nodelete_test.png'
        response = default_upload_file_and_conversion(
            route, django_path=django_path, target_ext='.xlsx')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

# ================================================
# Test 400: endpoint: /api/file/csv2txt/
# ================================================
    def test_if_csv2txt_invalid_file_returns_400(self, default_upload_file_and_conversion):
        route = '/api/file/csv2txt/'
        django_path = 'file/files/file_test_location/nodelete_test.png'
        response = default_upload_file_and_conversion(
            route, django_path=django_path, target_ext='.txt')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ================================================
# Test 400: endpoint: /api/file/xlsx2csv/
# ================================================

    def test_if_xlsx2csv_invalid_file_returns_400(self, default_upload_file_and_conversion):
        route = '/api/file/xlsx2csv/'
        django_path = 'file/files/file_test_location/nodelete_test.png'
        response = default_upload_file_and_conversion(
            route, django_path=django_path, target_ext='.csv')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

# ================================================
# Test 400: endpoint: /api/file/xls2csv/
# ================================================
    def test_if_xls2csv_invalid_file_returns_400(self, default_upload_file_and_conversion):
        route = '/api/file/xls2csv/'
        django_path = 'file/files/file_test_location/nodelete_test.png'
        response = default_upload_file_and_conversion(
            route, django_path=django_path, target_ext='.csv')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ================================================
# Test 400: endpoint: /api/file/xls2xlsx/
# ================================================

    def test_if_xls2xlsx_invalid_file_returns_400(self, default_upload_file_and_conversion):
        route = '/api/file/xls2xlsx/'
        django_path = 'file/files/file_test_location/nodelete_test.png'
        response = default_upload_file_and_conversion(
            route, django_path=django_path, target_ext='.xlsx')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

# ================================================
# Test 400: endpoint: /api/file/txt2csv/
# ================================================
    def test_if_txt2csv_invalid_file_returns_400(self, default_upload_file_and_conversion):
        route = '/api/file/txt2csv/'
        django_path = 'file/files/file_test_location/nodelete_test.png'
        response = default_upload_file_and_conversion(
            route, django_path=django_path, target_ext='.csv')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

# ================================================
# Test 400: endpoint: /api/file/txt2xlsx/
# ================================================
    def test_if_txt2xlsx_invalid_file_returns_400(self, default_upload_file_and_conversion):
        route = '/api/file/txt2xlsx/'
        django_path = 'file/files/file_test_location/nodelete_test.png'
        response = default_upload_file_and_conversion(
            route, django_path=django_path, target_ext='.xlsx')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
