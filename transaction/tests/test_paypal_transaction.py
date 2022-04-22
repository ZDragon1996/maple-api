
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from core.models import User
from model_bakery import baker
import json
from transaction.models import PaypalOrder


@pytest.mark.django_db
class TestPaypalTranscatoon:
    def test_if_user_is_anonymouse_get_put_patch_delete_call_returns_401(self):
        client = APIClient()

        response_get = client.get('/api/transaction/paypal/', data={})
        response_put = client.put('/api/transaction/paypal/', data={})
        response_patch = client.patch('/api/transaction/paypal/', data={})
        response_delete = client.delete('/api/transaction/paypal/', data={})

        assert response_get.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_put.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_patch.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_delete.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_get_put_patch_delete_call_returns_405(self):
        client = APIClient()
        client.force_authenticate(user=User)
        response_get = client.get('/api/transaction/paypal/', data={})
        response_put = client.put('/api/transaction/paypal/', data={})
        response_patch = client.patch('/api/transaction/paypal/', data={})
        response_delete = client.delete('/api/transaction/paypal/', data={})

        assert response_get.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_put.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_patch.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response_delete.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.skip
    def test_authenticated_user_create_paypal_order_returns_201(self):
        client = APIClient()
        client.force_authenticate(user=User)
        data = json.dumps({
            "order_id": "2L4450093E531022B",
            "intent": "CAPTURE",
            "create_time": "2022-04-17T00:08:27Z",
            "payer_country_code": "US",
            "payer_first_name": "John",
            "payer_last_name": "Doe",
            "payer_email_address": "sb-h5bhr15679238@personal.example.com",
            "links": [
                {
                    "href": "https://api.sandbox.paypal.com/v2/checkout/orders/2L4450093E531022B",
                    "rel": "self",
                    "method": "GET"
                }
            ],
            "purchase": [
                {
                    "purchase_reference_id": "default",
                    "purchase_currency_code": "USD",
                    "purchase_amount": 1.70,
                    "purhcase_description": "gold",
                    "payee_email": "sb-xpiih15253698@business.example.com",
                    "payee_merchant_id": "N3W3EZ6DRA6FJ",
                    "shipping_street": "1 Main St",
                    "shipping_state": "CA",
                    "shipping_city": "San Jose",
                    "shipping_country_code": "US",
                    "shipping_zip": "95131",
                    "shipping_full_name": "John Doe",
                    "payment_id": "31H155916X7389603",
                    "payment_status": "COMPLETED",
                    "payment_currency_code": "USD",
                    "payment_amount": 1.70,
                    "payment_final_capture": True,
                    "seller_protection_status": "ELIGIBLE"
                }
            ],
            "status": "COMPLETED",
            "update_time": "2022-04-17T00:08:34Z"
        }, indent=2)

        response_get = client.post(
            '/api/transaction/paypal/', data=data)

        assert response_get.status_code == status.HTTP_201_CREATED
