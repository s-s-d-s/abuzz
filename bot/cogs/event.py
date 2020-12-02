# import discord
# from discord.ext import commands
#
#
# class OwlVote:
#
#     def __init__(self, bot, ctx, emojis, title, desc, count_accept, voting_time):
#         self.bot = bot
#         self.ctx = ctx
#         self.emojis = emojis
#         self.title = title
#         self.desc = desc
#         self.count_accept = count_accept
#         self.time_str = voting_time
#         self.message = None
#         self.votes = {
#             'accept': set(),
#         }
#
#     async def _add_reaction(self, message):
#         for emoji in self.emojis.values():
#             await message.add_reaction(emoji)
#
#     async def _delete_reaction(self, emoji, user):
#         try:
#             await self.message.remove_reaction(emoji, user)
#         except:
#             pass
#
#     async def edit_message(self):
#         accept_users = '\n'.join([member.mention for member in self.votes['accept']]) if self.votes[
#             'accept'] else '- - -'
#
#         embed = discord.Embed(title=f"Активность: {self.title}", description=f"Описание: {self.desc}", color=16254938)
#         embed.set_footer(text=f"Создатель: {self.ctx.author.display_name}", icon_url=self.ctx.author.avatar_url)
#         embed.add_field(name="Время:", value=f"{self.time_str}", inline=False)
#         embed.add_field(name=f"{str(self.emojis['accept'])} Приняли ({len(self.votes['accept'])}/{self.count_accept}):",
#                         value=f">>> {accept_users}", inline=True)
#         embed.set_author(name="Пользовательский ивент", icon_url=self.bot.user.avatar_url)
#
#         if self.message:
#             await self.message.edit(embed=embed)
#         else:
#             self.message = await self.ctx.send(f'@here\n', embed=embed)
#             await self._add_reaction(self.message)
#
#     async def run(self):
#         while True:
#             try:
#                 reaction, user = await self.bot.wait_for('reaction_add', check=lambda r, u: not u.bot and r.message.id == self.message.id)
#                 if reaction.emoji == self.emojis['accept']:
#                     if user in self.votes['accept']:
#                         self.votes['accept'].remove(user)
#                     elif len(self.votes['accept']) < self.count_accept:
#                         self.votes['accept'].add(user)
#                 await self._delete_reaction(reaction.emoji, user)
#                 await self.edit_message()
#             except Exception as error:
#                 print(f'Ошибка {error}')
#
#
# class CommandEvent(commands.Cog):
#
#     def __init__(self, bot):
#         self.bot = bot
#         self.bot.loop.create_task(self.initialy_emoji())
#
#     async def initialy_emoji(self):
#         await self.bot.wait_until_ready()
#         self.emojis = {
#             'accept': self.bot.get_emoji(738780406010347550),
#         }
#
#     @commands.command(name='event', brief='Создать ивент')
#     async def command_event(self, ctx):
#
#         await ctx.message.delete()
#
#         message_status = await ctx.author.send(embed=discord.Embed(title='**Укажите название активности**',
#                                                                    description='```Пример: Абуз Компета, Гамбита, Киллов```',
#                                                                    color=16254938))
#         message_title = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
#
#         await message_status.edit(embed=discord.Embed(title='**Укажите описание активности**',
#                                                       description='```Пример: на 100 киллов круг или ссылку на войс канал```', color=16254938))
#         message_description = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
#
#         await message_status.edit(embed=discord.Embed(title='**Укажите количество участников**',
#                                                       description='```К-во игроков на абуз (ввести цифру)```',
#                                                       color=16254938))
#         message_attendees = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
#
#         await message_status.edit(embed=discord.Embed(title='**Укажите время активности**',
#                                                       description='```Пример: сегодня в 20:00, завтра в 13:00, 24/07/2020 в 09:00```',
#                                                       color=16254938))
#         message_time = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
#
#         try:
#             vote = OwlVote(
#                 bot=self.bot,
#                 ctx=ctx,
#                 emojis=self.emojis,
#                 title=message_title.content,
#                 desc=message_description.content,
#                 count_accept=int(message_attendees.content),
#                 voting_time=message_time.content,
#             )
#
#         except Exception as error:
#             await ctx.author.send(embed=discord.Embed(title='**Ошибка в указанных данных**',
#                                                       description='```Корректно укажите к-во участников```',
#                                                       color=16254938))
#             return
#
#         await vote.edit_message()
#         await message_status.edit(embed=discord.Embed(title='**Инициализация активности**',
#                                                       description=f'[**Абуз успешно создана**]({vote.message.jump_url})',
#                                                       color=16254938))
#         await vote.run()
