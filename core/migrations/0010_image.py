# Generated by Django 4.0.4 on 2022-04-20 03:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_membership_level_alter_membership_membership'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='image/images')),
                ('cusetomer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.customer')),
            ],
        ),
    ]
