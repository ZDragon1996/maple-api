from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
# Register your models here.


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", 'first_name', 'last_name'),
            },
        ),
    )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',  'membership']
    list_editable = ['membership']


@admin.register(models.Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['member_token', 'membership', 'level']
