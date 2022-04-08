from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    login_ip = models.GenericIPAddressField(null=False, default='0.0.0.0')


class Customer(models.Model):
    MEMBERSHIP_STANDARD = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_DIAMOND = 'D'
    MEMBERSHIP_PREMIUM = 'P'
    MEMBERSHIP_CHOICE = [
        (MEMBERSHIP_STANDARD, 'Standard'),
        (MEMBERSHIP_GOLD, 'Gold'),
        (MEMBERSHIP_DIAMOND, 'Diamond'),
        (MEMBERSHIP_PREMIUM, 'Premium')
    ]
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICE, default=MEMBERSHIP_STANDARD)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.first_name

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
