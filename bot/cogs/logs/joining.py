import discord
import datetime
from qbot import settings
from discord.ext import commands

class Joining(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.green = 5498133
        self.red = 14229549

    @commands.Cog.listener()
    async def on_ready(self):
        self.log_channel = self.bot.get_channel(settings.JOINING_CHANNEL_ID)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        embed = discord.Embed(title='Участник присоединился',
                              description='{0}'.format(member), color=self.green)
        embed.add_field(name='Участников', value='{0}'.format(len(list(guild.members))))
        embed.set_footer(text='ID: {0}'.format(member.id), icon_url=member.avatar_url)
        embed.set_thumbnail(url='https://images-ext-1.discordapp.net/external/n0o4EhyXlrEEgrN9a55AGqMKz_OT5jvm828G1tUCpXY/https/i.imgur.com/PhcFCzC.png')
        embed.timestamp = datetime.datetime.utcnow()
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        embed = discord.Embed(title='Участник вышел',
                              description='{0}'.format(member), color=self.red)
        embed.add_field(name='Участников', value='{0}'.format(len(list(guild.members))))
        embed.set_footer(text='ID: {0}'.format(member.id), icon_url=member.avatar_url)
        embed.set_thumbnail(url='https://images-ext-1.discordapp.net/external/bDbOMbawEqiLd0qlgtnLN9Hb_UMuaXLO0sr3xnCl1GA/https/i.imgur.com/wN9N2jk.png')
        embed.timestamp = datetime.datetime.utcnow()
        await self.log_channel.send(embed=embed)
