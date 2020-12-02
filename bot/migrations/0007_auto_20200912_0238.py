# Generated by Django 2.2.16 on 2020-09-11 23:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_auto_20200912_0232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='mute',
            name='mute_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 13, 2, 37, 59, 188271), verbose_name='Время Мута'),
        ),
        migrations.AlterField(
            model_name='queue',
            name='leave_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 14, 2, 37, 59, 187274), verbose_name='Время Окончания Абуза'),
        ),
        migrations.AlterField(
            model_name='queue',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='queue_user', to='bot.User'),
        ),
    ]