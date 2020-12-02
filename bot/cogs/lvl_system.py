import discord
import datetime
from qbot import settings
from bot import models
from discord.ext import commands


class LevelSystemCog(commands.Cog):

    profile_channel_id = settings.PROFILE_CHANNEL_ID

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return
        for prefix in ['!', '$', '&', '_', '.']:
            if message.content.startswith(prefix):
                return

        try:
            user = models.User.objects.get(discord_id=message.author.id)
            user.experience += models.LvlSystem.objects.get(key='message_xp').value
            user.save()

            lvl_end = int(user.experience ** (1/4))

            if user.level < lvl_end:
                user.level = lvl_end
                user.save()

                embed = discord.Embed(title='Новый уровень \💎',
                                      description=f'\🔸 <@{user.discord_id}> ваш уровень теперь **{lvl_end}**',
                                      color=settings.BOT_COLOR)
                embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                embed.set_author(name=message.guild.name, icon_url=message.guild.icon_url)
                embed.set_thumbnail(url=message.author.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()

                channel = self.bot.get_channel(self.profile_channel_id)
                await channel.send(embed=embed)
        except:
            pass

    @commands.command(brief='Профиль пользователя')
    async def profile(self, ctx):
        await ctx.message.delete()

        user = models.User.objects.get(discord_id=ctx.author.id)
        channel = self.bot.get_channel(self.profile_channel_id)

        created_at = ctx.author.created_at.strftime('%d.%m.%Y в %H:%M')
        join_at = ctx.author.joined_at.strftime('%d.%m.%Y в %H:%M')
        register_at = user.date_add.strftime('%d.%m.%Y в %H:%M')

        content = f'**Информация о пользователе \🌀**\n'\
                  f'[Уровень {user.level}] `{user.experience } Опыта`\n\n'\
                  f'Никнейм: <@{user.discord_id}>\n'\
                  f'Discord ID: {user.discord_id}\n'\
                  f'Steam ID: {user.steam_id}\n\n'\
                  f'Роли: {"".join([r.mention for r in ctx.author.roles[1:]])}\n\n'\
                  f'Аккаунт создан: *{created_at}*\n'\
                  f'Дата присоединения: *{join_at}*\n'\
                  f'Дата регистрации: *{register_at}*\n'

        embed = discord.Embed(title=f'{ctx.author.display_name} ({user})',
                              description=content,
                              color=settings.BOT_COLOR)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()

        await channel.send(embed=embed)

    @commands.command(aliases=['top'], brief='ТОП-15 сервера')
    async def top15(self, ctx):
        await ctx.message.delete()

        top = models.User.objects.order_by('-experience')[:15]

        channel = self.bot.get_channel(self.profile_channel_id)

        content = ''.join(f'`#{user[0]}`:<@{user[1].discord_id}> \➡ **{user[1].level}** уровень, всего опыта: **{user[1].experience}**\n' for user in enumerate(top, start=1))

        embed = discord.Embed(title=f'ТОП-15 \🍉',
                              description=content,
                              color=settings.BOT_COLOR)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()

        await channel.send(embed=embed)


    @commands.command(aliases=['ID'], brief='Просмотреть циферки хоста')
    async def id(self, ctx, *members: discord.Member):
        await ctx.message.delete()

        if members:
            for member in members:
                try:
                    user = models.User.objects.get(discord_id=member.id)

                    if user.second_steam_id == 0:
                        embed = discord.Embed(title='\🍉Циферки на присоединение',
                                              description=f'\🔸 <@{user.discord_id}> \➡ /вступить {user.steam_id}',
                                              color=settings.BOT_COLOR)
                        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                        embed.timestamp = datetime.datetime.utcnow()

                        await ctx.author.send(embed=embed)
                    else:
                        embed = discord.Embed(title='\🍉Циферки на присоединение',
                                              description=f'\🔸 <@{user.discord_id}> \➡ /вступить {user.steam_id}\n'
                                                          f'\🔸 <@{user.discord_id}>#2 \➡ /вступить {user.second_steam_id}',
                                              color=settings.BOT_COLOR)
                        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                        embed.timestamp = datetime.datetime.utcnow()

                        await ctx.author.send(embed=embed)
                except:
                    pass
        else:
            embed = discord.Embed(title='Системное сообщение \⚙',
                                  description=f'\🔸 **`@user`** обязательный аргумент, который отсутствует.\n'
                                              f'\🔸 Нужно упомянуть пользователя, для работы с этой командой.')

            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.author.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            try:
                models.User.objects.filter(discord_id=before.id).update(user=f'{after.name}#{after.discriminator}')
            except:
                pass
        if before.discriminator != after.discriminator:
            try:
                models.User.objects.filter(discord_id=before.id).update(user=f'{after.name}#{after.discriminator}')
            except:
                pass
