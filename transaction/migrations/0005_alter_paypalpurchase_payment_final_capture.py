# Generated by Django 4.0.3 on 2022-04-10 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_paypallink_paypalpurchase_paypalorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paypalpurchase',
            name='payment_final_capture',
            field=models.BooleanField(),
        ),
    ]