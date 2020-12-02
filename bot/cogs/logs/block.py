import discord
import datetime
from qbot import settings
from discord.ext import commands


class Block(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.log_channel = self.bot.get_channel(settings.BLOCK_CHANNEL_ID)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        embed = discord.Embed(title='Блокировка выдана',
                              description='Участник {0} был заблокирован на сервере **{1}**'.format(user, guild),
                              color=settings.RED)
        embed.set_thumbnail(
            url='https://images-ext-1.discordapp.net/external/QZ7YcCFahIN6azdJmxcEERBvRmu4NBgPRNIpT56cEdg/https/i.imgur.com/tfSm8aN.png')
        embed.set_footer(text='ID: {0}'.format(user.id), icon_url=user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        embed = discord.Embed(title='Блокировка убрана',
                              description='Участник **{0}** был разблокирован на сервере **{1}**'.format(user, guild),
                              color=settings.GREEN)
        embed.set_thumbnail(
            url='https://images-ext-1.discordapp.net/external/Ygkl-w3ImFtFUKwtbHHYF8gFdBM6E3-kqqT_QaP4jeA/https/i.imgur.com/NLCI4I3.png')
        embed.set_footer(text='ID: {0}'.format(user.id), icon_url=user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        await self.log_channel.send(embed=embed)
