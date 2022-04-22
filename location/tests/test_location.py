from email import header
from pydoc import cli
from rest_framework.test import APIClient
from rest_framework import status
from django.conf import settings
import redis
import pytest
from core.models import Membership, User
from core.utils import utils
from model_bakery import baker


@pytest.mark.django_db
class TestLocation:
    def test_if_list_state_returns_200(self):
        client = APIClient()

        response = client.get('/api/list_state/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_state_list_returns_200(self):
        client = APIClient()

        response = client.get('/api/state_list/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_list_state_post_put_delete_call_returns_405(self):
        client = APIClient()

        response_post = client.post('/api/list_state/', data={})
        response_put = client.put('/api/list_state/', data={})
        response_patch = client.patch('/api/list_state/', data={})
        response_delete = client.delete('/api/list_state/', data={})

        assert response_post.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_put.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_patch.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_delete.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_if_state_list_post_put_delete_call_returns_405(self):
        client = APIClient()

        response_post = client.post('/api/state_list/', data={})
        response_put = client.put('/api/state_list/', data={})
        response_patch = client.patch('/api/state_list/', data={})
        response_delete = client.delete('/api/state_list/', data={})

        assert response_post.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_put.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_patch.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_delete.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_if_membership_is_anonymous_returns_429(self):
        redis.Redis().flushall()
        client = APIClient()
        max_call = int(
            settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['standard'].strip('/day'))

        for _ in range(max_call+1):
            response = client.get('/api/state_list/')
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        redis.Redis().flushall()

    def test_if_membership_is_anonymous_returns_200(self):
        redis.Redis().flushall()
        client = APIClient()
        max_call = int(
            settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['standard'].strip('/day'))

        for _ in range(max_call):
            response = client.get('/api/state_list/')
            assert response.status_code == status.HTTP_200_OK
        redis.Redis().flushall()
