from discord.ext import commands


class ConsoleCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @property
    def startup_banner(self):
        bot_name = self.bot.user.name
        return '\n-> Logged in as {0}'.format(bot_name)

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.startup_banner)
        print('-> Bot is online!\n')
