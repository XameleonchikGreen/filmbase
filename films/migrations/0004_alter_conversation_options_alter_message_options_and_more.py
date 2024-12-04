# Generated by Django 5.1.3 on 2024-11-28 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_message_conversation_usergroup_alter_film_user_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conversation',
            options={'ordering': ['name'], 'verbose_name': 'Обсуждение', 'verbose_name_plural': 'Обсуждения'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['updated_at'], 'verbose_name': 'Сообщение', 'verbose_name_plural': 'Сообщения'},
        ),
        migrations.AlterModelOptions(
            name='usergroup',
            options={'verbose_name': 'Группа пользователей', 'verbose_name_plural': 'Группы пользователей'},
        ),
        migrations.RemoveField(
            model_name='conversation',
            name='messages',
        ),
        migrations.RemoveField(
            model_name='usergroup',
            name='conversations',
        ),
        migrations.AddField(
            model_name='conversation',
            name='user_group',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='films.usergroup'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='conversation',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='films.conversation'),
            preserve_default=False,
        ),
    ]
