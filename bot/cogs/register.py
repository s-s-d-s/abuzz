import discord
import datetime
import asyncio
from qbot import settings
from bot import models
from discord.ext import commands


class RegisterCog(commands.Cog):

    register_role_id = settings.REGISTER_ROLE_ID

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.bot.loop.create_task(self.check_registered())

    async def check_registered(self):
        while not self.bot.is_closed():
            try:
                guild = self.bot.get_guild(settings.GUILD_ID)
                register_role = guild.get_role(self.register_role_id)
                user = models.User.objects.filter(registered=False).first()
                register_user = discord.utils.get(guild.members, id=user.discord_id)

                await register_user.add_roles(register_role)

                user.registered = True
                user.save()

                embed = discord.Embed(title='Регистрация успешна \✅',
                                      description=f'\💠 Ваш Discord ID: {user.discord_id}\n'
                                                  f'\💠 Ваш Steam ID: {user.steam_id}',
                                      color=settings.BOT_COLOR)
                embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                embed.set_author(name=guild.name, icon_url=guild.icon_url)
                embed.timestamp = datetime.datetime.utcnow()

                await register_user.send(embed=embed)
                await asyncio.sleep(30)
            except:
                await asyncio.sleep(30)

    @commands.command(brief='Регистрация на сервере')
    async def reg(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(title='Регистрация \⚙',
                              description=f'\🔸 Посетите наш сайт и пройдите авторизацию на **steamcommunity.com** и **discord.com**.\n'
                                          f'\🔸 Со своей стороны мы получаем доступ к общедоступным данным: **Steam ID** и **Discord ID**.\n'
                                          f'[\➡ Нажмите здесь, чтобы зарегистрироваться \⬅](https://abuzz.life)',
                              color=settings.BOT_COLOR)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.author.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        ROLES = {
            '<:emoji_6:712739901539483658>': settings.REACTION_ROLE_ID,
        }
        if payload.message_id == settings.REACTION_MESSAGE_ID:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            member = discord.utils.get(message.guild.members, id=payload.user_id)
            try:
                emoji = str(payload.emoji)
                role = discord.utils.get(message.guild.roles, id=ROLES[emoji])
                if role in member.roles:
                    await member.remove_roles(role)
                else:
                    await member.add_roles(role)
                await message.remove_reaction(payload.emoji, member)
            except:
                pass
