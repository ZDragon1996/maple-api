# Generated by Django 4.0.3 on 2022-04-08 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_user_login_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_token', models.CharField(default='0', max_length=255)),
                ('membership', models.CharField(choices=[('S', 'Standard'), ('G', 'Gold'), ('D', 'Diamond'), ('P', 'Premium')], default='S', max_length=1)),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='membership',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.membership'),
        ),
    ]