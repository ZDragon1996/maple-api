from email import header
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from core.models import Customer, Membership
from . import constants
import secrets
import string
import requests
import os


def get_client_ip(request):
    http_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if http_forward_for:
        ip = http_forward_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_full_name(list, target):
    for short_name, full_name in list:
        if short_name == target:
            return full_name.lower()
    return constants.MEMBERSHIP_STANDARD.lower()


def get_membership(request) -> str:
    user_id = request.user.id
    member_token = request.META.get('HTTP_MAPLEMT')

    # vlidate request membership token and user id
    if not member_token and user_id:
        # check level when membership token is not valid(works for login user without header)
        level = Membership.objects.filter(customer__user_id=user_id)
        if level:
            return get_full_name(constants.MEMBERSHIP_LEVEL_CHOICE, level[0].level)
        return constants.MEMBERSHIP_STANDARD.lower()

    # skip db check if member token is empty
    membership = Membership.objects.filter(
        customer__user_id=user_id, member_token=member_token)
    if not membership:
        return constants.MEMBERSHIP_STANDARD.lower()

    # get membership full_name
    membership_full_name = get_full_name(
        constants.MEMBERSHIP_CHOICE, membership[0].membership)
    return membership_full_name


def generate_membership_token():
    return 'MT' + ''.join(secrets.choice(string.ascii_letters+string.digits) for i in range(20))


def _get_paypal_token():
    cache_key = 'paypal_business_token'
    request_header = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    body = {
        'grant_type': 'client_credentials'
    }
    paypal_client_id = os.environ.get('PAYPAL_CLIENT_ID')
    paypal_client_secret = os.environ.get('PAYPAL_CLIENT_SECRET')
    if cache.get(cache_key) is None:
        paypal_token_response = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token',
                                              body, request_header, auth=(paypal_client_id, paypal_client_secret))
        paypal_token = paypal_token_response.json()['access_token']
        print(paypal_token)
        cache.set(cache_key, paypal_token, timeout=32000)
        return paypal_token
    else:
        # cache has paypal token
        paypal_token = cache.get(cache_key)
        return paypal_token


def validate_paypal_transaction(order_id):
    token = _get_paypal_token()
    print(order_id)
    request_header = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(
        rf'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}', headers=request_header)
    if not response.status_code == 404:
        data = response.json()
        order_status = data['status']
        order_price = data['purchase_units'][0]['amount']['value']
        order_currency_code = data['purchase_units'][0]['amount']['currency_code']
        if order_status == 'COMPLETED' and order_price == '1.70' and order_currency_code == 'USD':
            return response.status_code
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    return response.status_code
