from turtle import title
import disnake, asyncio
from disnake.ext import commands
from core.Database import Backups
from core.files import Data


class Invite(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="invite",
        description="Gives you the invite for the Bot and the Bots Support Server"
    )
    async def server_info(self, inter: disnake.CommandInteraction):
        config = Data("config").json_read()
        bot_name = self.bot.user.name
        emb = disnake.Embed(title=f"**Invite {bot_name}**", color=disnake.Color.from_rgb(r=255, g=255, b=255), description=f"{bot_name} Protects your Server from Mass-Mention and Webhook raids. See how the bot performs and how many users it's currently protecting!")
        emb.set_author(name=bot_name, icon_url=self.bot.user.display_avatar.url)
        emb.add_field(name=f"Add {bot_name}", inline=True, value=f"[Invite](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=applications.commands%20bot)")
        emb.add_field(name=f"Join {bot_name} Community", inline=True, value=f"[Join]({config['support_server']})")

        return await inter.send(embed=emb)


def setup(bot):
    bot.add_cog(Invite(bot))
