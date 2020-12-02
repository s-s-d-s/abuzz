import discord
import datetime
from qbot import settings
from discord.ext import commands

class Monitoring(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.green = 5498133
        self.red = 14229549
        self.yellow = 16768256

    @commands.Cog.listener()
    async def on_ready(self):
        self.log_channel = self.bot.get_channel(settings.MONITORING_CHANNEL_ID)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed = discord.Embed(title='Никнем изменен', color=self.yellow)
            embed.add_field(name='Участник', value='{0}#{1}'.format(before.name, before.discriminator), inline=False)
            embed.add_field(name='Раньше', value=before.name, inline=True)
            embed.add_field(name='Сейчас', value=after.name, inline=True)
            embed.set_thumbnail(
                url='https://images-ext-2.discordapp.net/external/Nehs2RB797gIUxyuQ3cBJzsqTAPf6lfU8T8Km6X7jIw/https/i.imgur.com/XW2damX.png')
            embed.set_footer(text='ID: {0}'.format(after.id), icon_url=after.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await self.log_channel.send(embed=embed)

        if before.avatar_url != after.avatar_url:
            embed = discord.Embed(title='Аватар пользователя изменён', color=self.yellow)
            embed.add_field(name='Участник', value='{0}#{1}'.format(before.name, before.discriminator), inline=False)
            embed.set_thumbnail(url=before.avatar_url)
            url = str(after.avatar_url)[:-10]
            embed.set_image(url=url)
            embed.set_thumbnail(
                url='https://images-ext-2.discordapp.net/external/Nehs2RB797gIUxyuQ3cBJzsqTAPf6lfU8T8Km6X7jIw/https/i.imgur.com/XW2damX.png')
            embed.set_footer(text='ID: {0}'.format(after.id), icon_url=after.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = discord.Embed(title='Никнем изменен', color=self.yellow)
            embed.add_field(name='Участник', value='{0}#{1}'.format(before.name, before.discriminator), inline=False)
            embed.add_field(name='Раньше', value=before.display_name, inline=True)
            embed.add_field(name='Сейчас', value=after.display_name, inline=True)
            embed.set_thumbnail(
                url='https://images-ext-2.discordapp.net/external/Nehs2RB797gIUxyuQ3cBJzsqTAPf6lfU8T8Km6X7jIw/https/i.imgur.com/XW2damX.png')
            embed.set_footer(text='ID: {0}'.format(after.id), icon_url=after.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await self.log_channel.send(embed=embed)

        elif before.roles != after.roles:
            for role in after.roles:
                if role not in before.roles:
                    embed = discord.Embed(title='Роль добавлена', color=self.green)
                    embed.add_field(name='Участник', value='{0}#{1}'.format(before.name, before.discriminator), inline=True)
                    embed.add_field(name='Роль', value=role.mention, inline=True)
                    embed.set_thumbnail(
                        url='https://images-ext-2.discordapp.net/external/Nehs2RB797gIUxyuQ3cBJzsqTAPf6lfU8T8Km6X7jIw/https/i.imgur.com/XW2damX.png')
                    embed.set_footer(text='ID: {0}'.format(after.id), icon_url=after.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await self.log_channel.send(embed=embed)
            for role in before.roles:
                if role not in after.roles:
                    embed = discord.Embed(title='Роль убрана', color=self.red)
                    embed.add_field(name='Участник', value='{0}#{1}'.format(before.name, before.discriminator), inline=True)
                    embed.add_field(name='Роль', value=role.mention, inline=True)
                    embed.set_thumbnail(
                        url='https://images-ext-2.discordapp.net/external/Nehs2RB797gIUxyuQ3cBJzsqTAPf6lfU8T8Km6X7jIw/https/i.imgur.com/XW2damX.png')
                    embed.set_footer(text='ID: {0}'.format(after.id), icon_url=after.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await self.log_channel.send(embed=embed)
