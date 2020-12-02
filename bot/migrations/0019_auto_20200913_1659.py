# Generated by Django 2.2.16 on 2020-09-13 13:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0018_auto_20200913_1658'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='embeds',
            options={'ordering': ['id'], 'verbose_name': 'Системный Embed', 'verbose_name_plural': 'Системные Embeds'},
        ),
        migrations.AlterField(
            model_name='mute',
            name='mute_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 14, 16, 59, 21, 419450), help_text='Время Мута', verbose_name='Время Мута'),
        ),
        migrations.AlterField(
            model_name='queue',
            name='leave_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 16, 16, 59, 21, 419450), help_text='Время Кика из Очереди', verbose_name='Время Кика из Очереди'),
        ),
    ]
