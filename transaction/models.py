from django.db import models
from core.models import Customer
from core.utils import constants
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name}({self.price})'


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=10,
                                    choices=constants.ORDER_CHOICE, default=constants.ORDER_PEN)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)


# ======================PAYPAL========================

class PaypalOrder(models.Model):
    order_id = models.CharField(max_length=255, unique=True)
    intent = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    payer_country_code = models.CharField(max_length=100)
    payer_first_name = models.CharField(max_length=255)
    payer_last_name = models.CharField(max_length=255)
    payer_email_address = models.EmailField()

    create_time = models.DateTimeField()
    update_time = models.DateTimeField()


# Link
class PaypalLink(models.Model):
    href = models.CharField(max_length=255)
    rel = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    paypal_order = models.ForeignKey(
        PaypalOrder, on_delete=models.CASCADE, related_name='link')


# Purchase
class PaypalPurchase(models.Model):
    purchase_reference_id = models.CharField(max_length=255)
    purchase_currency_code = models.CharField(max_length=255)
    purchase_amount = models.DecimalField(max_digits=8, decimal_places=2)
    purhcase_description = models.CharField(max_length=255)
    payee_email = models.EmailField()
    payee_merchant_id = models.CharField(max_length=255)

    shipping_full_name = models.CharField(max_length=255)
    shipping_street = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255)
    shipping_zip = models.CharField(max_length=255)
    shipping_country_code = models.CharField(max_length=255)

    payment_id = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255)
    payment_currency_code = models.CharField(max_length=255)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_final_capture = models.BooleanField()
    seller_protection_status = models.CharField(max_length=255)
    paypal_order = models.ForeignKey(
        PaypalOrder, on_delete=models.CASCADE, related_name='purchase')
