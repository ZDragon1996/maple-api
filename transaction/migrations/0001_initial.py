# Generated by Django 4.0.3 on 2022-04-09 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0009_alter_membership_level_alter_membership_membership'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order_statue', models.CharField(choices=[('PEN', 'Pending'), ('CAN', 'Canceled'), ('COM', 'Completed'), ('FAI', 'Failed')], default='PEN', max_length=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transaction.product')),
            ],
        ),
    ]