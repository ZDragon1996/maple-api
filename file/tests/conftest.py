import pytest
from rest_framework.test import APIClient
from file.classes.file import File


@pytest.fixture
def api_client():
    return APIClient()


