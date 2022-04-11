from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction
from django.conf import settings
from core.models import Customer, Membership, User
from core.utils import utils

PAYPALORDER = settings.PAYPALORDER


@receiver(post_save, sender=PAYPALORDER)
def change_membership_after_transaction(sender, **kwargs):
    if kwargs['created']:
        with transaction.atomic():
            mt_token = utils.generate_membership_token()
            membership = Membership.objects.create(
                level=2, member_token=mt_token, membership='G')
            print(membership.id)
            Customer.objects.filter(user_id=kwargs['user_id']).update(
                membership_id=membership.id)


@receiver(post_save, sender=User)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        with transaction.atomic():
            mt_token = utils.generate_membership_token()
            membership = Membership.objects.create(
                level=1, member_token=mt_token, membership='S')
        print(kwargs['instance'])
        Customer.objects.create(
            membership=membership, user=kwargs['instance'])
