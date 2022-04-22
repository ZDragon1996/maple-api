from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    list_editable = ['name', 'price']
    list_display_links = None


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'order_status', 'customer', 'product']
    list_editable = ['order_status', 'customer', 'product']
