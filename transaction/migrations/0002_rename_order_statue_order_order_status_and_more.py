# Generated by Django 4.0.3 on 2022-04-09 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_membership_level_alter_membership_membership'),
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_statue',
            new_name='order_status',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='customer',
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='core.customer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='product',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='transaction.order'),
            preserve_default=False,
        ),
    ]