from operator import truediv
from pyexpat import model
from rest_framework import serializers
from django.db import IntegrityError
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model
from .utils import utils
from .models import User, Membership, Customer
from .models import CustomerImage
# Custom User Serializer for create user: host/auth/users/


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']

        def create(self, validated_data):
            ip = utils.get_client_ip(self.context['request'])
            return User.objects.create(login_ip=ip, **validated_data)


class UserSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username',
                  'first_name', 'last_name']


class UpdateUserSerializer(BaseUserCreateSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['membership_token', 'membership', 'level']


class CustomerSerializer(serializers.ModelSerializer):
    user = UpdateUserSerializer()
    phone = serializers.CharField(default='')

    class Meta:
        model = Customer
        fields = ['phone', 'birth_date', 'user']


class ImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        customer_id = self.context['customer_id']
        return CustomerImage.objects.create(customer_id=customer_id, **validated_data)

    class Meta:
        model = CustomerImage
        fields = ['id', 'image']
