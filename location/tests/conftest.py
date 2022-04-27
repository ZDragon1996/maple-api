from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status
import pytest
import redis


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_get_request(api_client):
    def wrapper(route_path):
        redis.Redis().flushall()
        return api_client.get(route_path)
    return wrapper


@pytest.fixture
def validate_too_many_requests(api_client):
    def wrapper(route_path):
        redis.Redis().flushall()
        max_call = int(
            settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['standard'].strip('/day'))

        for _ in range(max_call+1):
            response = api_client.get(route_path)
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        redis.Redis().flushall()
    return wrapper
