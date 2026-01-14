from turtle import title
import disnake, asyncio
from disnake.ext import commands
from core.Database import Backups
from core.files import Data


class BotInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="botinfo",
        description="Check the bots status, latency and much more"
    )
    async def server_info(self, inter: disnake.CommandInteraction):
        config = Data("config").json_read()
        bot_name = self.bot.user.name
        emb = disnake.Embed(title=f"**About {bot_name}**", color=disnake.Color.from_rgb(r=255, g=255, b=255), description=f"{bot_name} Protects your Server from Mass-Mention and Webhook raids. See how the bot performs and how many users it's currently protecting!")
        emb.set_author(name=bot_name, icon_url=self.bot.user.display_avatar.url)
        emb.add_field(name="Version", inline=True, value=config["version"])
        emb.add_field(name="Servers", inline=True, value=len(self.bot.guilds))
        emb.add_field(name="Users", inline=True, value=len(self.bot.users))
        emb.add_field(name="Library", inline=True, value=f"{disnake.__name__} v{disnake.__version__}")
        emb.add_field(name="Creator", inline=True, value=config["creator"])
        emb.add_field(name="Ping", inline=True, value=f"{round(self.bot.latency * 1000)}ms")

        return await inter.send(embed=emb)


def setup(bot):
    bot.add_cog(BotInfo(bot))
