import discord
import datetime
from qbot import settings
from bot import models
from discord.ext import commands, tasks
from django.utils import timezone


class ModerationCog(commands.Cog):

    muted_role_id = settings.MUTE_ROLE_ID

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def mute_handler(guild, member, messages=False):
        for channel in guild.text_channels:
            if messages:
                await channel.set_permissions(member, overwrite=None)
            else:
                await channel.set_permissions(member, send_messages=messages)

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_muted.start()

    def missing_argument_embed(self, ctx):
        embed = discord.Embed(title='Системное сообщение \⚙',
                              description=f'\🔸 **`@user`** обязательный аргумент, который отсутствует.\n'
                                          f'\🔸 Нужно упомянуть пользователя, для работы с этой командой.')

        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        return embed

    @commands.command(usage='clear N', brief='Очистить N к-во сообщений')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, x: int):
        await ctx.channel.purge(limit=x + 1)

    @commands.command(usage='kick @user reason', brief='Кикнуть пользователя')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason: str = 'не указана'):
        await ctx.message.delete()

        if member:
            await member.kick(reason=reason)

            embed = discord.Embed(title='\📕 Участник был кикнут',
                                  description=f'{ctx.author.mention} кикнул **{member}**\n'
                                              f'Причина: {reason}',
                                  color=settings.RED)
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed=embed)
        else:
            embed = self.missing_argument_embed(ctx)
            await ctx.author.send(embed=embed)

    @commands.command(usage='ban @user reason', brief='Забанить пользователя')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason: str = 'не указана'):
        await ctx.message.delete()

        if member:
            await member.ban(reason=reason)

            embed = discord.Embed(title='\📕 Участник был забанен',
                                  description=f'{ctx.author.mention} забанил **{member}**\n'
                                              f'Причина: {reason}',
                                  color=settings.RED)
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed=embed)
        else:
            embed = self.missing_argument_embed(ctx)
            await ctx.author.send(embed=embed)

    @commands.command(usage='unban @user reason', brief='Разбанить пользователя')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: str = None, *, reason: str = 'не указана'):
        await ctx.message.delete()

        if member:
            ban_list = await ctx.guild.bans()

            if not ban_list:

                embed = discord.Embed(title='Что-то пошло не так \⚙',
                                      description='\🔸 Нету забаненных участников.',
                                      color=settings.YELLOW)
                embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                embed.timestamp = datetime.datetime.utcnow()

                await ctx.send(embed=embed)
                return

            for entry in ban_list:
                if member in entry.user.name:
                    await ctx.guild.unban(entry.user, reason=reason)

                    embed = discord.Embed(title='\📕 Участник была разбанен',
                                          description=f'{ctx.author.mention} разбанил **{entry.user.mention}**\n'
                                                      f'Причина: {reason}',
                                          color=settings.GREEN)
                    embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                    embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                    embed.timestamp = datetime.datetime.utcnow()

                    await ctx.send(embed=embed)
                    return

            embed = discord.Embed(title='Что-то пошло не так \⚙',
                                  description='\🔸 Корректно укажите участника.',
                                  color=settings.YELLOW)
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed=embed)
            return
        else:
            embed = self.missing_argument_embed(ctx)
            await ctx.author.send(embed=embed)

    @commands.command(usage='mute @user reason', brief='Замутить пользователя')
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason: str = 'не указана'):
        await ctx.message.delete()

        guild = member.guild
        muted = guild.get_role(self.muted_role_id)
        await self.mute_handler(guild, member)
        await member.add_roles(muted)

        embed = discord.Embed(title='\🔇 Участник был замучен',
                              description=f'{ctx.author.mention} замутил **{member.mention}** на 24 часа.\n'
                                          f'Причина: {reason}',
                              color=settings.RED)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=embed)

        try:
            muted_user = models.Mute()
            muted_user.user = models.User.objects.get(discord_id=member.id)
            muted_user.channel_id = ctx.channel.id
            muted_user.save()
        except:
            pass

    @tasks.loop(minutes=60.0)
    async def check_muted(self):
        guild = self.bot.get_guild(settings.GUILD_ID)
        unmuted = models.Mute.objects.exclude(mute_time__gt=timezone.now())

        for user in unmuted:
            unmuted_user = discord.utils.get(guild.members, id=user.user.discord_id)
            muted = guild.get_role(self.muted_role_id)
            channel = self.bot.get_channel(user.channel_id)

            await self.mute_handler(guild, unmuted_user, True)
            await unmuted_user.remove_roles(muted)
            models.Mute.objects.filter(user__discord_id=unmuted_user.id).delete()

            embed = discord.Embed(description=f'{unmuted_user.mention} был размучен.',
                                  color=settings.GREEN)
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_author(name=guild.name, icon_url=guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)

    @clear.error
    @kick.error
    @ban.error
    @unban.error
    @mute.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.delete()

            embed = discord.Embed(title='Системное сообщение \⚙',
                                  description='\🔸 У вас не хватает прав на использования этой команды!',
                                  color=settings.BOT_COLOR)
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.author.send(embed=embed)
