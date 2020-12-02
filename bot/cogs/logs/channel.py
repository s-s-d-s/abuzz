import discord
import datetime
from bot import models
from qbot import settings
from discord.ext import commands


class Channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.log_channel = self.bot.get_channel(settings.CHANNEL_LOG_ID)
        channel = models.Message.objects.filter(message_type='3')

        for vc in channel:
            voice_channel = self.bot.get_channel(vc.message_id)
            await self.delete_vc(voice_channel)

    async def add_to(self, voice_channel):
        channel = models.Message()
        channel.message_id = voice_channel.id
        channel.message_type = '3'
        channel.save()

    async def delete_from(self, voice_channel):
        try:
            models.Message.objects.filter(message_id=voice_channel.id).delete()
        except:
            pass

    def get_channel_by_name(self, guild, channel_name):
        channel = None
        for c in guild.channels:
            if c.name == channel_name:
                channel = c
                break
        return channel

    def get_category_by_name(self, guild, category_name):
        category = None
        for c in guild.categories:
            if c.name == category_name:
                category = c
                break
        return category

    async def create_vc(self, guild, channel_name, member, category_name=None, user_limit=None, position=None):
        category = self.get_category_by_name(guild, category_name)
        members_role = discord.utils.get(member.guild.roles, name="Members")
        registered_role = discord.utils.get(member.guild.roles, name="Registered")
        host_role = discord.utils.get(member.guild.roles, name="Host")

        await guild.create_voice_channel(channel_name,
                                         overwrites={host_role: discord.PermissionOverwrite(connect=False, move_members=True),
                                                     registered_role: discord.PermissionOverwrite(connect=True, view_channel=False),
                                                     members_role: discord.PermissionOverwrite(connect=False, view_channel=True),
                                                     guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=False),
                                                     member: discord.PermissionOverwrite(manage_channels=True)},
                                         category=category,
                                         user_limit=user_limit,
                                         position=position)
        channel = self.get_channel_by_name(guild, channel_name)
        return channel

    async def delete_vc(self, channel):
        def check(x, y, z):
            return len(channel.members) == 0
        try:
            await self.bot.wait_for('voice_state_update', check=check)
            await self.delete_from(channel)
            await channel.delete()
        except:
            pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is not None:
            if after.channel.id == settings.KILLS_VOICE_CHANNEL_ID:
                voice_channel = await self.create_vc(after.channel.guild, f'Kills: {member.name}',
                                                     member,
                                                     category_name='Abuzz',
                                                     user_limit=6)

                if voice_channel is not None:
                    await self.add_to(voice_channel)
                    await member.edit(voice_channel=voice_channel)
                await self.delete_vc(voice_channel)
            elif after.channel.id == settings.SURVIVAL_VOICE_CHANNEL_ID:
                voice_channel = await self.create_vc(after.channel.guild, f'Survival: {member.name}',
                                                     member,
                                                     category_name='Abuzz',
                                                     user_limit=6)

                if voice_channel is not None:
                    await self.add_to(voice_channel)
                    await member.edit(voice_channel=voice_channel)
                await self.delete_vc(voice_channel)
            elif after.channel.id == settings.GAMBIT_VOICE_CHANNEL_ID:
                voice_channel = await self.create_vc(after.channel.guild, f'Gambit: {member.name}',
                                                     member,
                                                     category_name='Abuzz',
                                                     user_limit=8)

                if voice_channel is not None:
                    await self.add_to(voice_channel)
                    await member.edit(voice_channel=voice_channel)
                await self.delete_vc(voice_channel)
            elif after.channel.id == settings.TRIALS_VOICE_CHANNEL_ID:
                #Feito
                if member.id == 181481113359745025:
                    voice_channel = await self.create_vc(after.channel.guild, f'🍉Безупречный: {member.name}',
                                                         member,
                                                         category_name='Trials of Osiris',
                                                         user_limit=5,
                                                         position=10)
                    if voice_channel is not None:
                        await self.add_to(voice_channel)
                        await member.edit(voice_channel=voice_channel)
                    await self.delete_vc(voice_channel)
                #ssds
                elif member.id == 362956199400046592:
                    voice_channel = await self.create_vc(after.channel.guild, f'🍉Abuz: {member.name}',
                                                         member,
                                                         category_name='Trials of Osiris',
                                                         user_limit=2,
                                                         position=10)
                    if voice_channel is not None:
                        await self.add_to(voice_channel)
                        await member.edit(voice_channel=voice_channel)
                    await self.delete_vc(voice_channel)
                else:
                    voice_channel = await self.create_vc(after.channel.guild, f'🍉Trials: {member.name}',
                                                         member,
                                                         category_name='Trials of Osiris',
                                                         user_limit=6)
                    if voice_channel is not None:
                        await self.add_to(voice_channel)
                        await member.edit(voice_channel=voice_channel)
                    await self.delete_vc(voice_channel)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        embed = discord.Embed(title='Голосовой канал создан',
                              color=settings.GREEN)
        embed.add_field(name='Название', value=f'{channel.name}', inline=True)
        embed.add_field(name='Категория', value=channel.category, inline=True)
        embed.add_field(name='Позиция', value=channel.position, inline=True)
        embed.set_footer(text=f'ID: {channel.guild.id}', icon_url=channel.guild.icon_url)
        embed.set_thumbnail(
            url='https://images-ext-1.discordapp.net/external/2A3JI5OT04uRGefP07L0YLq0tmcLkJ5kDNWPHJDGHlw/https/i.imgur.com/kUiNNNX.png')

        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        embed = discord.Embed(title='Голосовой канал удалён',
                              color=settings.RED)
        embed.add_field(name='Название', value=f'{channel.name}', inline=True)
        embed.add_field(name='Категория', value=channel.category, inline=True)
        embed.add_field(name='Позиция', value=channel.position, inline=True)
        embed.set_footer(text=f'ID: {channel.guild.id}', icon_url=channel.guild.icon_url)
        embed.set_thumbnail(
            url='https://images-ext-2.discordapp.net/external/SYpeEs9TVLEzhaGpEgULVORVAq22zJQFKJi-nNY_wrU/https/i.imgur.com/ZHQfrwC.png')
        embed.timestamp = datetime.datetime.utcnow()

        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        try:
            if before.name != after.name:
                embed = discord.Embed(title='Голосовой канал изменен',
                                      color=settings.YELLOW)
                embed.add_field(name='Канал', value=f'#{after.name}', inline=False)
                embed.add_field(name='Название Раньше', value=before.name, inline=True)
                embed.add_field(name='Сейчас', value=after.name, inline=True)
                embed.set_footer(text=f'ID: {before.guild.id}', icon_url=before.guild.icon_url)
                embed.set_thumbnail(url='https://images-ext-1.discordapp.net/external/VRlmH8IWt47ATxdaLrBkKVdWdIzeCzVtP2z0y-VIDEY/https/i.imgur.com/LYpqejS.png')
                embed.timestamp = datetime.datetime.utcnow()

                await self.log_channel.send(embed=embed)
            elif before.user_limit != after.user_limit:
                embed = discord.Embed(title='Голосовой канал изменен',
                                      color=settings.YELLOW)
                embed.add_field(name='Канал', value=f'#{after.name}', inline=False)
                embed.add_field(name='Лимит пользователей Раньше', value=before.user_limit, inline=True)
                embed.add_field(name='Сейчас', value=after.user_limit, inline=True)
                embed.set_footer(text=f'ID: {before.guild.id}', icon_url=before.guild.icon_url)
                embed.set_thumbnail(
                    url='https://images-ext-1.discordapp.net/external/VRlmH8IWt47ATxdaLrBkKVdWdIzeCzVtP2z0y-VIDEY/https/i.imgur.com/LYpqejS.png')
                embed.timestamp = datetime.datetime.utcnow()

                await self.log_channel.send(embed=embed)
            elif before.position != after.position:
                embed = discord.Embed(title='Голосовой канал изменен',
                                      color=settings.YELLOW)
                embed.add_field(name='Канал', value=f'#{after.name}', inline=False)
                embed.add_field(name='Позиция Раньше', value=before.position, inline=True)
                embed.add_field(name='Сейчас', value=after.position, inline=True)
                embed.set_footer(text=f'ID: {before.guild.id}', icon_url=before.guild.icon_url)
                embed.set_thumbnail(url='https://images-ext-1.discordapp.net/external/VRlmH8IWt47ATxdaLrBkKVdWdIzeCzVtP2z0y-VIDEY/https/i.imgur.com/LYpqejS.png')
                embed.timestamp = datetime.datetime.utcnow()

                await self.log_channel.send(embed=embed)
            elif before.bitrate != after.bitrate:
                embed = discord.Embed(title='Голосовой канал изменен',
                                      color=settings.YELLOW)
                embed.add_field(name='Канал', value=f'#{after.name}', inline=False)
                embed.add_field(name='Битрейт Раньше', value=before.bitrate, inline=True)
                embed.add_field(name='Сейчас', value=after.bitrate, inline=True)
                embed.set_footer(text=f'ID: {before.guild.id}', icon_url=before.guild.icon_url)
                embed.set_thumbnail(url='https://images-ext-1.discordapp.net/external/VRlmH8IWt47ATxdaLrBkKVdWdIzeCzVtP2z0y-VIDEY/https/i.imgur.com/LYpqejS.png')
                embed.timestamp = datetime.datetime.utcnow()

                await self.log_channel.send(embed=embed)
        except:
            pass
