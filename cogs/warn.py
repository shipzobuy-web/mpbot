from optparse import Option
from turtle import title
import disnake, asyncio
from disnake.ext import commands
from core.Database import Backups
from core.Database.Modules import Module
from core.files import Data


class Warn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="warn",
        description="Issue a warning to a user",
        options=[
            disnake.Option(
                name="user",
                type=disnake.OptionType.user,
                required=True,
                description="User to warn"
            )
        ]
    )
    async def warn(self, inter: disnake.CommandInteraction, user: disnake.Member, reason: str=None):
        if Module(inter.guild_id, "modules").is_disabled("Moderation"):
            return await inter.send("This module is disabled!", ephemeral=True)

        if not inter.author.guild_permissions.manage_guild:
            return await inter.send("You need the `Manage Guild` permission to do this!", ephemeral=True)
            
        emb = disnake.Embed(title="Warning", description=f"You have been warned in {inter.guild.name} for the reason: {reason}", color=disnake.Color.yellow())
        await user.send(embed=emb)
        return await inter.send(f"{inter.user.mention} has been warned")


def setup(bot):
    bot.add_cog(Warn(bot))
