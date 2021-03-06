# Generated by Django 2.2.16 on 2020-09-14 12:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0026_auto_20200913_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embeds',
            name='description',
            field=models.TextField(blank=True, default='', max_length=2048, verbose_name='Значение'),
        ),
        migrations.AlterField(
            model_name='embeds',
            name='title',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='mute',
            name='mute_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 15, 12, 20, 37, 785152, tzinfo=utc), help_text='Время Мута', verbose_name='Время Мута'),
        ),
        migrations.AlterField(
            model_name='queue',
            name='leave_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 17, 12, 20, 37, 785152, tzinfo=utc), help_text='Время Кика из Очереди', verbose_name='Время Кика из Очереди'),
        ),
    ]
