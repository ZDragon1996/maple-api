from django.shortcuts import get_object_or_404
from core.models import Customer, Membership
from . import constants
import secrets
import string


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
