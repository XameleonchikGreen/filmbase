# Generated by Django 5.1.3 on 2024-12-03 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0007_alter_usergroup_waiters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='messages/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(verbose_name='Сообщение'),
        ),
    ]
