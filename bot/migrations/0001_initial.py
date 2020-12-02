# Generated by Django 2.2.16 on 2020-09-11 22:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.IntegerField(default=0, max_length=25, verbose_name='ИД Сообщения')),
                ('message_type', models.CharField(blank=True, choices=[('1', 'Queue Message'), ('2', 'Party Message'), ('3', 'Voice Message')], default='', max_length=1, verbose_name='Сообщение')),
            ],
            options={
                'verbose_name': 'Системнное Сообщение',
                'verbose_name_plural': 'Системные Сообщения',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Пользователь')),
                ('discord_id', models.IntegerField(max_length=25, unique=True, verbose_name='Дискорд ID')),
                ('steam_id', models.IntegerField(max_length=25, unique=True, verbose_name='Стим ID')),
                ('second_steam_id', models.IntegerField(blank=True, default=0, verbose_name='Второй Стим ID')),
                ('rep', models.PositiveIntegerField(default=0, verbose_name='Репутация')),
                ('date_add', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='bot.User')),
            ],
            options={
                'verbose_name': 'Очередь',
                'verbose_name_plural': 'Очереди',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Mute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mute_time', models.DateTimeField(default=datetime.datetime(2020, 9, 13, 1, 31, 1, 631469), verbose_name='Время Мута')),
                ('channel_id', models.IntegerField(max_length=25, verbose_name='Канал')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.User', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Бан канала',
                'verbose_name_plural': 'Бан каналов',
                'ordering': ['id'],
            },
        ),
    ]