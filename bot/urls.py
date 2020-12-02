from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='homepage'),
    path('steam_login', views.login_steam, name='steam_login'),
    path('success_steam', views.login_process, name='success_steam'),
    path('success_discord', views.discord_process, name='discord_success'),
]