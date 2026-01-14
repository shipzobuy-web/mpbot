from disnake.ext import commands
from core.config import Config  # <- new config from env

def manager():
    def predicate(ctx):
        return ctx.author.id in Config.MANAGERS
    return commands.check(predicate)
