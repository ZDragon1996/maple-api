from rest_framework import status
from django.conf import settings
import redis
import pytest
from core.models import Membership, User
from core.utils import utils
from model_bakery import baker
import requests

list_states_route = '/api/location/states/'
states_and_cities_route = '/api/location/states_and_cities/'

def validate_post_put_delete_call_returns_405(api_client):
    def wrapper(route_path):
        response_post = api_client.post(route_path, data={})
        response_put = api_client.put(route_path, data={})
        response_patch = api_client.patch(route_path, data={})
        response_delete = api_client.delete(route_path, data={})

        assert response_post.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_put.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_patch.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_delete.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    return wrapper


@pytest.mark.django_db
class TestLocation:

    # ==============================
    # Test /api/location/states
    # ==============================
    def test_if_states_returns_200(self, api_client):
        response = api_client.get(list_states_route)

        assert response.status_code == status.HTTP_200_OK

    def test_if_states_post_put_delete_call_returns_405(self):
        validate_post_put_delete_call_returns_405(list_states_route)

    def test_if_states_membership_is_anonymous_returns_429(self, validate_too_many_requests):
        validate_too_many_requests(list_states_route)

# =========================================
# Test /api/location/states_and_cities
# =========================================
    def test_if_states_and_cities_returns_200(self, api_client):
        response = api_client.get(states_and_cities_route)

        assert response.status_code == status.HTTP_200_OK

    def test_if_states_and_cities_post_put_delete_call_returns_405(self):
        validate_post_put_delete_call_returns_405(states_and_cities_route)

    def test_if_states_with_cities_membership_is_anonymous_returns_429(self, validate_too_many_requests):
        validate_too_many_requests(states_and_cities_route)
