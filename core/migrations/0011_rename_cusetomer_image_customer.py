# Generated by Django 4.0.4 on 2022-04-20 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='cusetomer',
            new_name='customer',
        ),
    ]
