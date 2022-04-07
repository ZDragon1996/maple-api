# Generated by Django 4.0.3 on 2022-04-07 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_alter_us_city_latitude_alter_us_city_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='us_city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='location.us_state'),
        ),
    ]