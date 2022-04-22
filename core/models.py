from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from .utils import constants

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    login_ip = models.GenericIPAddressField(null=False, default='0.0.0.0')


class Membership(models.Model):
    member_token = models.CharField(unique=True, max_length=255)
    membership = models.CharField(
        max_length=1, choices=constants.MEMBERSHIP_CHOICE, default=constants.MEMBERSHIP_STANDARD)
    level = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.membership}({self.level}) - {self.member_token}'


class Customer(models.Model):
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.OneToOneField(
        Membership, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.first_name

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class CustomerImage(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='core/images')
