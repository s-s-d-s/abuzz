import discord
import datetime
from qbot import settings
from discord.ext import commands

class Messanger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.red = 14229549
        self.yellow = 16768256

    @commands.Cog.listener()
    async def on_ready(self):
        self.log_channel = self.bot.get_channel(settings.MESSANGER_CHANNEL_ID)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            if not after.author.bot:
                if before.content != after.content:
                    embed = discord.Embed(title='Сообщение изменено',
                                  color=self.yellow)
                    embed.add_field(name='Отправитель', value=after.author, inline=True)
                    embed.add_field(name='Канал', value=after.channel.mention, inline=True)
                    embed.add_field(name='Раньше', value=before.content, inline=False)
                    embed.add_field(name='Сейчас', value=after.content, inline=False)
                    embed.set_footer(text='ID: {0}'.format(before.author.id), icon_url=before.author.avatar_url)
                    embed.set_thumbnail(
                        url='https://images-ext-2.discordapp.net/external/IvpYVRbl-OBczjPnxia1ER-BXoeqlwe9-BHBruMBZbI/https/i.imgur.com/Vfvgj9X.png')
                    embed.timestamp = datetime.datetime.utcnow()
                    await self.log_channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            if not message.author.bot:
                embed = discord.Embed(title='Сообщение удалено',
                                      color=self.red)
                embed.add_field(name='Отправитель', value=message.author, inline=True)
                embed.add_field(name='Канал', value=message.channel.mention, inline=True)
                embed.add_field(name='Содержание', value=message.content, inline=False)
                embed.set_footer(text='ID: {0}'.format(message.author.id), icon_url=message.author.avatar_url)
                embed.set_thumbnail(
                    url='https://images-ext-2.discordapp.net/external/WGdZ5Y0Lp5nXqqXbV0GRYmhcYQ5zhC8eRJ6CcLpCHzg/https/i.imgur.com/Bjk1NMO.png')
                embed.timestamp = datetime.datetime.utcnow()
                await self.log_channel.send(embed=embed)
        except:
            pass