# Generated by Django 2.2.16 on 2020-09-12 09:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0011_auto_20200912_1221'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mute',
            options={'ordering': ['id'], 'verbose_name': 'Блокировака канала', 'verbose_name_plural': 'Блокировака каналов'},
        ),
        migrations.AlterField(
            model_name='message',
            name='message_id',
            field=models.BigIntegerField(default=0, help_text='ID сообщения для нужного типа', verbose_name='ID Сообщения'),
        ),
        migrations.AlterField(
            model_name='mute',
            name='channel_id',
            field=models.BigIntegerField(verbose_name='Канал'),
        ),
        migrations.AlterField(
            model_name='mute',
            name='mute_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 13, 12, 33, 47, 451661), verbose_name='Время Мута'),
        ),
        migrations.AlterField(
            model_name='queue',
            name='leave_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 15, 12, 33, 47, 450664), verbose_name='Время Кика из Очереди'),
        ),
        migrations.AlterField(
            model_name='user',
            name='discord_id',
            field=models.BigIntegerField(unique=True, verbose_name='Дискорд ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='experience',
            field=models.BigIntegerField(default=0, verbose_name='Опыт'),
        ),
        migrations.AlterField(
            model_name='user',
            name='second_steam_id',
            field=models.BigIntegerField(blank=True, default=0, verbose_name='Второй Стим ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='steam_id',
            field=models.BigIntegerField(unique=True, verbose_name='Стим ID'),
        ),
    ]