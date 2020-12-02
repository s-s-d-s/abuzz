from qbot import settings
from django.db import models
from datetime import timedelta
from django.utils import timezone


class User(models.Model):
    """
    Модель зарегистрированных пользователей
    """

    user = models.CharField(
        max_length=100,
        help_text='Имя Пользователя',
        verbose_name='Пользователь')
    discord_id = models.BigIntegerField(
        blank=True,
        null=True,
        unique=True,
        help_text='Дискорд ID Пользователя',
        verbose_name='Дискорд ID')
    steam_id = models.BigIntegerField(
        unique=True,
        help_text='Стим ID Пользователя',
        verbose_name='Стим ID')
    second_steam_id = models.BigIntegerField(
        default=0,
        blank=True,
        help_text='Резервный Стим ID Пользователя',
        verbose_name='Второй Стим ID')
    level = models.IntegerField(
        default=0,
        help_text='Уровень Пользователя',
        verbose_name='Уровень')
    experience = models.BigIntegerField(
        default=0,
        help_text='Опыт Пользователя',
        verbose_name='Опыт')
    date_add = models.DateTimeField(
        auto_now_add=True,
        help_text='Дата Присоединения на Сервер',
        verbose_name='Дата Присоединения')
    registered = models.BooleanField(
        default=False,
        verbose_name='Проверка на роль')

    def __str__(self):
        return '{0}'.format(self.user)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    class Meta:
        ordering = ["id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Queue(models.Model):
    """
    Модель Очереди
    """

    user = models.ForeignKey(
        User,
        related_name="queue_user",
        null=True,
        on_delete=models.CASCADE,
        help_text='Пользователь',
        verbose_name='Пользователь')

    def __str__(self):
        return '{0}'.format(self.user)

    class Meta:
        ordering = ["id"]
        verbose_name = "Очередь"
        verbose_name_plural = "Очереди"


class Mute(models.Model):
    """
    Модель забаненых в чате пользователей
    """

    user = models.ForeignKey(
        User,
        related_name="muted_user",
        on_delete=models.CASCADE,
        help_text='Пользователь',
        verbose_name='Пользователь')
    mute_time = models.DateTimeField(
        default=timezone.now()+timedelta(settings.MUTE_TIME),
        help_text='Время Мута',
        verbose_name='Время Мута')
    channel_id = models.BigIntegerField(
        help_text='Канал Сообщения',
        verbose_name='Канал')

    def __str__(self):
        return '{0}'.format(self.user)

    class Meta:
        ordering = ["id"]
        verbose_name = "Блокировака канала"
        verbose_name_plural = "Блокировака каналов"


class Message(models.Model):
    """
    Модель системных сообщений
    """

    MSG_TYPE = (
        ('1', 'Queue Message'),
        ('2', 'Party Message'),
        ('3', 'Voice Message'),)

    message_id = models.BigIntegerField(
        default=0,
        help_text='ID сообщения для нужного типа',
        verbose_name='ID Сообщения')
    message_type = models.CharField(
        max_length=1,
        choices=MSG_TYPE,
        blank=True,
        default='',
        help_text='Тип Сообщения',
        verbose_name='Сообщение')

    def __str__(self):
        return '{0}'.format(self.message_type)

    class Meta:
        ordering = ["id"]
        verbose_name = "Системнное Сообщение"
        verbose_name_plural = "Системные Сообщения"


class LvlSystem(models.Model):
    """
    Система начисления опыта
    """

    key = models.CharField(
        max_length=20,
        default='',
        verbose_name='Ключ')
    value = models.IntegerField(
        default=5,
        verbose_name='К-во опыта',
        help_text='Опыт, который получает пользователь')

    def __str__(self):
        return '{0}'.format(self.key)

    class Meta:
        ordering = ["id"]
        verbose_name = "Система опыта"
        verbose_name_plural = "Системы опыта"
