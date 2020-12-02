# Generated by Django 2.2.16 on 2020-09-13 16:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0022_auto_20200913_1738'),
    ]

    operations = [
        migrations.RenameField(
            model_name='embeds',
            old_name='value',
            new_name='description',
        ),
        migrations.AlterField(
            model_name='mute',
            name='mute_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 14, 19, 34, 6, 921940), help_text='Время Мута', verbose_name='Время Мута'),
        ),
        migrations.AlterField(
            model_name='queue',
            name='leave_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 16, 19, 34, 6, 921940), help_text='Время Кика из Очереди', verbose_name='Время Кика из Очереди'),
        ),
    ]