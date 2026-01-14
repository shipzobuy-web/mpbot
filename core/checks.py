from .files import Data
from disnake.ext import commands

config = Data("config").json_read()

def manager():
    def predicate(ctx):
        return ctx.author.id in config["managers"]
    return commands.check(predicate)