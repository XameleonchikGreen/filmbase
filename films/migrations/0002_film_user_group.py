# Generated by Django 5.1.3 on 2024-11-27 15:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='user_group',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group', verbose_name='Группа пользователей'),
        ),
    ]
