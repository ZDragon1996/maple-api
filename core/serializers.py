from operator import mod
from django.db import IntegrityError
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model
from .utils import utils
from .models import User
# Custom User Serializer for create user: host/auth/users/


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']

        def create(self, validated_data):
            ip = utils.get_client_ip(self.context['request'])
            return User.objects.create(login_ip=ip, **validated_data)
