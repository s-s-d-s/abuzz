from django.contrib import admin
from django.contrib.auth.models import Group, User
from . import models

admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(models.User)
class User(admin.ModelAdmin):
    model = models.User
    search_fields = ['user', 'discord_id', 'steam_id', ]
    list_display = ['user', 'discord_id', 'steam_id', 'second_steam_id', 'level', 'experience', 'date_add', 'registered', ]
    list_editable = ['second_steam_id', 'level', 'experience', 'registered', ]
    list_filter = ['registered', ]


@admin.register(models.Queue)
class Queue(admin.ModelAdmin):
    model = models.Queue
    search_fields = ['user', ]
    list_display = ['user', ]


@admin.register(models.Mute)
class Mute(admin.ModelAdmin):
    model = models.Mute
    search_fields = ['user', ]
    list_display = ['user', 'mute_time', 'channel_id', ]
    list_editable = ['mute_time', ]


@admin.register(models.Message)
class Message(admin.ModelAdmin):
    model = models.Message
    list_display = ['message_id', 'message_type', ]


@admin.register(models.LvlSystem)
class LvlSystem(admin.ModelAdmin):
    model = models.LvlSystem
    list_display = ['key', 'value', ]
    list_editable = ['value', ]
