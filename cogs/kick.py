from turtle import title
import disnake, asyncio
from disnake.ext import commands
from core.Database import Backups
from core.Database.Modules import Module
from core.files import Data


class Kick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="kick",
        description="Kick a user",
        options=[
            disnake.Option(
                name="user",
                description="User to kick",
                type=disnake.OptionType.user,
                required=True
            )
        ]
    )
    async def kick(self, inter: disnake.CommandInteraction, user: disnake.Member, reason: str=None):
        if Module(inter.guild_id, "modules").is_disabled("Moderation"):
            return await inter.send("This module is disabled!", ephemeral=True)

        if not inter.author.guild_permissions.kick_members:
            return await inter.send("You need the `Kick Members` permission to do this!", ephemeral=True)

        emb = disnake.Embed(title="Kicked", description=f"You have been kicked in {inter.guild.name} for the reason: {reason}", color=disnake.Color.yellow())
        await user.send(embed=emb)
        await user.kick(reason=reason)
        return await inter.send(f"{inter.user.mention} has been kicked")


def setup(bot):
    bot.add_cog(Kick(bot))
