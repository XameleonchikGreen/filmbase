# Generated by Django 5.1.3 on 2024-11-29 13:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0005_usergroup_waiters_alter_usergroup_admin'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergroup',
            name='waiters',
            field=models.ManyToManyField(null=True, related_name='waiting_to_be_added', to=settings.AUTH_USER_MODEL, verbose_name='Подавшие заявку на вступление'),
        ),
    ]