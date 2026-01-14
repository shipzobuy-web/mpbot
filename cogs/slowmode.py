import disnake
from disnake.ext import commands

from core.Database.Modules import Module

class Slowmode(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="slowmode",
        description="Set the slowmode delay for the channel.",
        options=[
            disnake.Option(
                name="delay",
                description="Delay in seconds",
                type=disnake.OptionType.integer,
                min_value=0,
                max_value=21600,
                required=True
            )
        ],
        guild_ids=[862481678722793493]
    )
    async def slowmode(self, inter:disnake.CommandInteraction, delay:int):
        if Module(inter.guild_id, "modules").is_disabled("Moderation"):
            return await inter.send("This module is disabled!", ephemeral=True)
        if not inter.author.guild_permissions.manage_channels:
            return await inter.send("You need the `Manage Channels` permission to do this!", ephemeral=True)

        await inter.channel.edit(slowmode_delay=delay)
        return await inter.send(f"Set the slowmode delay to {delay} seconds!", ephemeral=True)

def setup(bot):
    bot.add_cog(Slowmode(bot))
