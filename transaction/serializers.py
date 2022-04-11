from operator import mod
from statistics import mode
from sys import maxsize
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from django.db import transaction
from . import models


class PaypalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaypalLink
        fields = ['href', 'rel', 'method']


class PaypalPurchaseSerialzier(serializers.ModelSerializer):
    class Meta:
        model = models.PaypalPurchase
        fields = [
            'purchase_reference_id', 'purchase_currency_code', 'purchase_amount',
            'purhcase_description', 'payee_email', 'payee_merchant_id',
            'shipping_full_name', 'shipping_street', 'shipping_state',
            'shipping_city', 'shipping_zip', 'shipping_country_code',
            'payment_id', 'payment_status', 'payment_currency_code',
            'payment_amount', 'payment_final_capture', 'seller_protection_status'
        ]


# ===============================================================
class PaypalOrderSerializer(serializers.ModelSerializer):
    purchase = PaypalPurchaseSerialzier(many=True)
    links = PaypalLinkSerializer(
        many=True, source='link')

    def create(self, validated_data):
        with transaction.atomic():
            validated_links_data = validated_data.pop('link')
            validated_purchases_data = validated_data.pop('purchase')

            paypal_order = models.PaypalOrder.objects.create(**validated_data)
            for link, purchase in zip(validated_links_data, validated_purchases_data):
                models.PaypalLink.objects.create(
                    paypal_order=paypal_order, **link)
                models.PaypalPurchase.objects.create(paypal_order=paypal_order,
                                                                  **purchase)

            return paypal_order

    class Meta:
        model = models.PaypalOrder
        fields = [
            'order_id', 'intent', 'create_time', 'payer_country_code',
            'payer_first_name', 'payer_last_name', 'payer_email_address',
            'links', 'purchase', 'status', 'create_time', 'update_time'
        ]
