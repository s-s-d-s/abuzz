from bot import cogs
from qbot import settings
from discord.ext import commands

discord_token = settings.DISCORD_TOKEN
PREFIX = settings.DISCORD_PREFIX

bot = commands.Bot(command_prefix=PREFIX)

bot.add_cog(cogs.ConsoleCog(bot))
bot.add_cog(cogs.HelpCog(bot))
bot.add_cog(cogs.RegisterCog(bot))
bot.add_cog(cogs.QueueCog(bot))
bot.add_cog(cogs.ModerationCog(bot))
bot.add_cog(cogs.LevelSystemCog(bot))
bot.add_cog(cogs.Block(bot))
bot.add_cog(cogs.Channel(bot))
bot.add_cog(cogs.Joining(bot))
bot.add_cog(cogs.Messanger(bot))
bot.add_cog(cogs.Monitoring(bot))
bot.add_cog(cogs.Voice(bot))

bot.run(discord_token)
