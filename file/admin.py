from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.File)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['file']
    list_editable = ['file']
    list_display_links = None
