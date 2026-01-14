from turtle import title
import disnake, asyncio
from disnake.ext import commands
from core.Database import Backups


class ServerInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.slash_command(
        name="serverinfo",
        description="Check the server information and stats",
    )
    async def server_info(self, inter: disnake.CommandInteraction):
        guild = inter.guild
        emb = disnake.Embed(title="**About this server**", color=disnake.Color.from_rgb(r=255, g=255, b=255))
        emb.set_author(name=guild.name, icon_url=guild.icon.url if guild.icon else None)
        emb.add_field(name="Owner", inline=True, value=guild.owner.mention)
        emb.add_field(name="Roles", inline=True, value=len(guild.roles))
        emb.add_field(name="Channels", inline=True, value=len(guild.channels))
        emb.add_field(name="Members", inline=True, value=len(guild.members))
        emb.add_field(name="Creation Date", inline=True, value=guild.created_at.strftime("%a, %d %b %Y"))

        return await inter.send(embed=emb)


def setup(bot):
    bot.add_cog(ServerInfo(bot))
