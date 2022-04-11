from rest_framework import serializers
from django.db import IntegrityError
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model
from .utils import utils
from .models import User, Membership
# Custom User Serializer for create user: host/auth/users/


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']

        def create(self, validated_data):
            ip = utils.get_client_ip(self.context['request'])
            return User.objects.create(login_ip=ip, **validated_data)


class Membership(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['membership_token', 'membership','level']