import discord
import datetime
from qbot import settings
from bot import models
from discord.ext import commands


class QueueCog(commands.Cog):

    channel_queue = settings.CHANNEL_QUEUE
    channel_selection = settings.CHANNEL_SELECTION
    role_no_abuse = settings.ROLE_NO_ABUSE_ID
    role_one_flawless = settings.ROLE_ONE_FLAWLESS
    role_two_flawless = settings.ROLE_TWO_FLAWLESS
    role_three_flawless = settings.ROLE_THREE_FLAWLESS
    host_role_id = settings.HOST_ROLE_ID
    members_reactions = []

    def __init__(self, bot, capacity=300):
        self.bot = bot
        self.capacity = capacity

    @commands.Cog.listener()
    async def update_embed(self, channel_id, embed, type_msg: str):
        channel = self.bot.get_channel(channel_id)

        try:
            msg = models.Message.objects.get(message_type=type_msg)
            message = await channel.fetch_message(msg.message_id)
            await message.edit(embed=embed)
        except:
            if type_msg == '2':
                message = await channel.send('@here\n', embed=embed)
            else:
                message = await channel.send(embed=embed)
            msg = models.Message()
            msg.message_id = message.id
            msg.message_type = type_msg
            msg.save()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            models.Message.objects.get(message_id=message.id).delete()
            self.members_reactions.clear()
        except:
            pass

    def embed(self, ctx, title=None, description=None):
        embed = discord.Embed(title=title,
                              description=description,
                              color=settings.BOT_COLOR)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        return embed

    def queue_embed(self, ctx, title=None):
        """
        Создание ембеда для генерации очереди
        """
        queue = models.Queue.objects.order_by('id')
        queue_count = queue.count()
        queue_active = queue[:40]

        if title:
            title += f' ({queue_count}/{self.capacity})'

        if queue_active:
            queue_str = ''.join(f'{user[0]}. {user[1]}(<@{user[1].user.discord_id}>)\n' for user in enumerate(queue_active, start=1))
        else:
            queue_str = '_Очередь пустая..._'

        embed = discord.Embed(title=title,
                              description=queue_str,
                              color=settings.BOT_COLOR)
        embed.set_footer(text='После 40-го места вы не будете отображаться в очереди', icon_url=self.bot.user.avatar_url)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()

        return embed

    def get_roles(self, ctx):
        role_1 = ctx.guild.get_role(self.role_one_flawless)
        role_2 = ctx.guild.get_role(self.role_two_flawless)
        role_3 = ctx.guild.get_role(self.role_three_flawless)

        return role_1, role_2, role_3

    async def check_roles(self, user):
        role_1, role_2, role_3 = self.get_roles(user)

        if user in role_1.members:
            await user.remove_roles(role_1)
            await user.add_roles(role_2)
        elif user in role_2.members:
            await user.remove_roles(role_2)
            await user.add_roles(role_3)
        elif user in role_3.members:
            pass
        else:
            await user.add_roles(role_1)

    async def remove_roles(self, ctx):
        role_1, role_2, role_3 = self.get_roles(ctx)

        for member in role_1.members:
            await member.remove_roles(role_1)
        for member in role_2.members:
            await member.remove_roles(role_2)
        for member in role_3.members:
            await member.remove_roles(role_3)

    @commands.command(aliases=['J'], brief='Присоединение к очереди')
    async def j(self, ctx):
        await ctx.message.delete()

        current_channel = ctx.channel.id
        no_abuse = ctx.guild.get_role(self.role_no_abuse)
        role_3 = ctx.guild.get_role(self.role_three_flawless)

        try:
            user = models.User.objects.get(user=ctx.author)
            queue = models.Queue.objects.filter(user=user).exists()
            queue_count = models.Queue.objects.count()
        except:
            pass
        else:
            if queue_count >= self.capacity:
                title = f'{ctx.author.display_name} очередь полная'
            elif ctx.author in no_abuse.members:
                embed = self.embed(ctx,
                                   title='Системное сообщение \⚙',
                                   description=f'\🔸Вас лишили возможности заходить в очередь\n'
                                               f'\🔸Причина: **`🔕Без абуза`**')
                await ctx.author.send(embed=embed)
                title = f'{ctx.author.display_name} не в очереди'
            elif ctx.author in role_3.members:
                embed = self.embed(ctx,
                                   title='Системное сообщение \⚙',
                                   description=f'\🔸Вас лишили возможности заходить в очередь\n'
                                               f'\🔸Причина: лимит  количества \🍉 на неделю исчерпан')
                await ctx.author.send(embed=embed)
                title = f'{ctx.author.display_name} не в очереди'
            elif self.channel_queue != current_channel:
                embed = self.embed(ctx,
                                  title='Системное сообщение \⚙',
                                  description=f'\🔸 Пропишите команду **`$j`** в канал <#711315338142285825>.')
                await ctx.author.send(embed=embed)
                title = f'{ctx.author.display_name} не в очереди'
            elif queue is False:
                queue = models.Queue()
                queue.user = user
                queue.save()
                title = f'{ctx.author.display_name} был добавлен в очередь'
            else:
                title = f'{ctx.author.display_name} уже в очереди'

            embed = self.queue_embed(ctx, title=title)
            await self.update_embed(self.channel_queue, embed, '1')

    @commands.command(aliases=['L'], brief='Покинуть очередь')
    async def l(self, ctx):
        await ctx.message.delete()

        user = models.User.objects.get(user=ctx.author)
        queue = models.Queue.objects.filter(user=user).exists()

        if queue:
            models.Queue.objects.filter(user=user).delete()
            title = f'{ctx.author.display_name} вышел из очереди'
            await self.check_roles(ctx.author)
        else:
            title = f'{ctx.author.display_name} не в очереди'

        embed = self.queue_embed(ctx, title=title)
        await self.update_embed(self.channel_queue, embed, '1')

    @commands.command(aliases=['R'], usage='r @user', brief='Удаляет выделеных пользователей из очереди')
    @commands.has_permissions(manage_messages=True)
    async def r(self, ctx, *members: discord.Member):
        await ctx.message.delete()

        if members:
            title = ''
            for user in members:
                models.Queue.objects.filter(user__discord_id=user.id).delete()
                await self.check_roles(user)
                title = f'{user.display_name} был удален из очереди'
        else:
            embed = self.embed(ctx,
                               title='Системное сообщение \⚙',
                               description=f'\🔸 **`@user`** обязательный аргумент, который отсутствует.\n'
                                           f'\🔸 Нужно упомянуть пользователя, для работы с этой командой.')
            await ctx.author.send(embed=embed)
            title = 'Игроки в очереди'

        embed = self.queue_embed(ctx, title=title)
        await self.update_embed(self.channel_queue, embed, '1')

    @commands.command(aliases=['V'], brief='Просмотреть очередь')
    @commands.has_permissions(manage_messages=True)
    async def v(self, ctx):
        await ctx.message.delete()

        embed = self.queue_embed(ctx, title='Игроки в очереди')
        await self.update_embed(self.channel_queue, embed, '1')

    @commands.command(aliases=['E'], brief='Обнулить очередь')
    @commands.has_permissions(ban_members=True)
    async def e(self, ctx):
        await ctx.message.delete()

        models.Queue.objects.all().delete()
        embed = self.queue_embed(ctx, title='Очередь обнулена')
        await self.update_embed(self.channel_queue, embed, '1')
        await self.remove_roles(ctx)

    @commands.command(aliases=['P'], brief='Узнать позицию в очереди')
    async def p(self, ctx):
        await ctx.message.delete()

        try:
            user = models.Queue.objects.get(user__user=ctx.author)
            position = models.Queue.objects.filter(id__lte=user.id).count()

            embed = self.embed(ctx,
                               title='Системное сообщение \⚙',
                               description=f'\🔸 <@{user.user.discord_id}> позиция в очереди \➡ {str(position)}')
            await ctx.author.send(embed=embed)
        except:
            embed = self.embed(ctx,
                               title='Системное сообщение \⚙',
                               description=f'\🔸 Вы не в очереди!\n'
                                           f'\🔸 Пропишите команду **`$j`**, чтобы вступить в очередь в канале <#711315338142285825>.')
            await ctx.author.send(embed=embed)

    @commands.command(aliases=['T'], brief='Сбор на абуз через @here')
    @commands.has_permissions(manage_messages=True)
    async def t(self, ctx):
        await ctx.message.delete()

        channel = self.bot.get_channel(self.channel_selection)

        embed = self.embed(ctx,
                           title='Кто готов идти Осириса откликнитесь реакцией \🍉',
                           description=f'Если вы не в игре или без пропуска вас ждать не будут\❗')
        embed.set_footer(text='В начале недели берите пожалуйста пропуск Ярость', icon_url=self.bot.user.avatar_url)

        await self.update_embed(self.channel_selection, embed, '2')
        message = await channel.fetch_message(models.Message.objects.get(message_type='2').message_id)
        await message.add_reaction('🍉')
        await message.add_reaction('⚙')
        await message.add_reaction('🗑')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if self.bot.get_user(payload.user_id).bot:
            return

        try:
            guild = self.bot.get_guild(settings.GUILD_ID)
            user = self.bot.get_user(payload.user_id)
            host_role = discord.utils.get(guild.roles, id=self.host_role_id)
            channel = self.bot.get_channel(self.channel_selection)
            message_id = models.Message.objects.get(message_type='2')
            msg = await channel.fetch_message(message_id.message_id)
        except:
            pass
        else:
            if payload.message_id == message_id.message_id:
                if str(payload.emoji) == '🍉':

                    if not payload.user_id in self.members_reactions:
                        self.members_reactions.append(payload.user_id)
                    else:
                        await msg.remove_reaction('🍉', user)
                        self.members_reactions.remove(payload.user_id)

                    try:
                        models.Queue.objects.get(user__discord_id=payload.user_id)
                    except:
                        embed = discord.Embed(
                                           title='Системное сообщение \⚙',
                                           description=f'\🔸 Вы не в очереди!\n'
                                                       f'\🔸 Пропишите команду **`$j`**, чтобы вступить в очередь в канале <#711315338142285825>.',
                                            color=settings.BOT_COLOR)
                        embed.set_author(name=guild.name, icon_url=guild.icon_url)
                        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                        embed.timestamp = datetime.datetime.utcnow()

                        await user.send(embed=embed)
                        await msg.remove_reaction('🍉', user)

                if str(payload.emoji) == '⚙':

                    try:
                        queue = models.Queue.objects.filter(user__discord_id__in=self.members_reactions).first()
                        discord_id = queue.user.discord_id
                        steam_id = queue.user.steam_id
                        position = models.Queue.objects.filter(id__lte=queue.id).count()
                        recipient = self.bot.get_user(discord_id)
                    except:
                        pass
                    else:
                        if user in host_role.members:
                            embed = discord.Embed(title='Системное сообщение \⚙',
                                                  description=f'\🔸 Настала твоя очередь ждем тебя!\n'
                                                              f'\🔸 Нажмите на гиперссылку: [\➡ Зайти в очередь \⬅](https://discord.gg/StCbjbc)\n'
                                                              f'\🔸 Пригласил на абуз \➡ **{user.display_name}**',
                                                  color=settings.BOT_COLOR)
                            embed.set_author(name=guild.name, icon_url=guild.icon_url)
                            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                            embed.timestamp = datetime.datetime.utcnow()

                            await recipient.send(embed=embed)
                            await msg.remove_reaction('🍉', recipient)

                            embed = discord.Embed(title='Системное сообщение \⚙',
                                                  description=f'\🔸 Приглашение было выслано игроку \➡ <@{discord_id}>\n'
                                                              f'\🔸 **SteamID:** {steam_id}\n'
                                                              f'\🔸 **Позиция:** {position}',
                                                  color=settings.BOT_COLOR)
                            embed.set_author(name=guild.name, icon_url=guild.icon_url)
                            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                            embed.timestamp = datetime.datetime.utcnow()

                            await user.send(embed=embed)
                    await msg.remove_reaction('⚙', user)

                if str(payload.emoji) == '🗑':
                    if user in host_role.members:
                        self.members_reactions.clear()
                        await msg.delete()
                    else:
                        await msg.remove_reaction('🗑', user)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        if self.bot.get_user(payload.user_id).bot:
            return

        try:
            message_id = models.Message.objects.get(message_type='2')

            if payload.message_id == message_id.message_id:
                if str(payload.emoji) == '🍉':
                    self.members_reactions.remove(payload.user_id)
        except:
            pass

    @r.error
    @e.error
    @t.error
    @v.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.delete()

            embed = self.embed(ctx,
                               title='Системное сообщение \⚙',
                               description='\🔸 У вас не хватает прав на использования этой команды!')
            await ctx.author.send(embed=embed)
