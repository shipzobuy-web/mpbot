from turtle import title
import disnake, asyncio
from disnake.ext import commands
from core.Database import Backups
from core.Database.Modules import Module
from core.files import Data


class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="ban",
        description="Ban a user",
        options=[
            disnake.Option(
                name="user",
                description="User to ban",
                required=True,
                type=disnake.OptionType.user
            )
        ]
    )
    async def ban(self, inter: disnake.CommandInteraction, user: disnake.Member, reason: str=None):
        if Module(inter.guild_id, "modules").is_disabled("Moderation"):
            return await inter.send("This module is disabled!", ephemeral=True)
            
        if not inter.author.guild_permissions.ban_members:
            return await inter.send("You need the `Ban Members` permission to do this!", ephemeral=True)

        emb = disnake.Embed(title="Banned", description=f"You have been banned in {inter.guild.name} for the reason: {reason}", color=disnake.Color.yellow())
        await user.send(embed=emb)
        await user.ban(reason=reason)
        return await inter.send(f"{user.mention} has been banned")


def setup(bot):
    bot.add_cog(Ban(bot))
