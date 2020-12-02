import requests
from qbot import settings
from . import models
from django.shortcuts import render, redirect
from django.http import HttpRequest
from steamauth import RedirectToSteamSignIn, GetSteamID64


def home(request):
    return render(request, './pages/main_page.html')

def login_steam(request):
    return RedirectToSteamSignIn('/success_steam', useSSL=settings.USE_STEAM_SSL)

def login_process(request):
    steam_id = GetSteamID64(request.GET)
    request.session['steam_id'] = steam_id

    if steam_id is False:
        return render(request, './pages/login_error.html')
    else:
        try:
            models.User.objects.get(steam_id=steam_id)
        except:
            user = models.User()
            user.steam_id = steam_id
            user.save()
        return redirect(settings.DISCORD_IDENTIFY)

def discord_process(request: HttpRequest):
    code = request.GET.get('code')
    exchange_code(request, code)
    return render(request, './pages/success.html')

def exchange_code(request, code: str):
    data = {
        'client_id': settings.CLIENT_BOT_ID,
        'client_secret': settings.CLIENT_SECRET_BOT,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.REDIRECT_URL_DISCORD,
        'scope': 'identify',
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
    credentials = response.json()
    access_token = credentials['access_token']
    response = requests.get('https://discord.com/api/v6/users/@me', headers={
        'Authorization': 'Bearer %s' % access_token
    })
    discord_user = response.json()
    user = models.User.objects.get(steam_id=request.session['steam_id'])
    user.discord_id = discord_user['id']
    user.user = '{0}#{1}'.format(discord_user['username'], discord_user['discriminator'])

    try:
        user.save()
    except:
        return render(request, './pages/login_error.html')
