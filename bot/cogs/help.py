import discord
import datetime
from discord.ext import commands


class HelpCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color = 16254938
        self.bot.remove_command('help')

    def help_embed(self, ctx, title):
        embed = discord.Embed(title=title,
                              color=self.color)
        prefix = self.bot.command_prefix
        prefix = prefix[0] if prefix is not str else prefix

        for cog in self.bot.cogs:
            for cmd in self.bot.get_cog(cog).get_commands():
                if cmd.usage:
                    embed.add_field(name='`{0}{1}`'.format(prefix, cmd.usage),
                                    value='<a:a_emoji_15:755812942976647168> _{0}_'.format(cmd.brief),
                                    inline=False)
                else:
                    embed.add_field(name='`{0}{1}`'.format(prefix, cmd.name),
                                    value='<a:a_emoji_15:755812942976647168> _{0}_'.format(cmd.brief),
                                    inline=False)
                embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        game = discord.Game('Trials Of Osiris')
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=game)

    @commands.command(aliases=['H', 'help', 'HELP'], brief='Меню помощи')
    async def h(self, ctx):
        embed = self.help_embed(ctx, '__Команды бота__')
        await ctx.send(embed=embed)
        await ctx.message.delete()
