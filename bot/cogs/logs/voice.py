import discord
import datetime
from qbot import settings
from discord.ext import commands


class Voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.green = 5498133
        self.red = 14229549
        self.yellow = 16768256

    @commands.Cog.listener()
    async def on_ready(self):
        self.log_channel = self.bot.get_channel(settings.VOICE_LOG_CHANNEL_ID)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            embed = discord.Embed(title='Голосовое подключение',
                                  color=self.green)
            embed.add_field(name='Участник', value=member, inline=True)
            embed.add_field(name='Канал', value=after.channel, inline=True)
            embed.set_footer(text='ID: {0}'.format(member.id), icon_url=member.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await self.log_channel.send(embed=embed)
        elif before.channel is not None and after.channel is None:
            embed = discord.Embed(title='Голосовое отсоединение',
                                  color=self.red)
            embed.add_field(name='Участник', value=member, inline=True)
            embed.add_field(name='Канал', value=before.channel, inline=True)
            embed.set_footer(text='ID: {0}'.format(member.id), icon_url=member.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await self.log_channel.send(embed=embed)
        elif before.channel is not None and after.channel and before.channel != after.channel:
            embed = discord.Embed(title='Голосовое перемещение',
                                  color=self.yellow)
            embed.add_field(name='Участник', value=member, inline=True)
            embed.add_field(name='Старый канал', value=before.channel, inline=True)
            embed.add_field(name='Новый канал', value=after.channel, inline=True)
            embed.set_footer(text='ID: {0}'.format(member.id), icon_url=member.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await self.log_channel.send(embed=embed)