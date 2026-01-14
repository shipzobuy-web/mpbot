import disnake
import validators
import requests
from disnake.ext import commands
from core.Database.Modules import Module
from core.config import Config  # <- new config from env

class PhishingDetection(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def check_link(self, url):
        if not validators.url(url):
            return False

        querystring = {"url": url}

        headers = {
            'x-rapidapi-host': "exerra-phishing-check.p.rapidapi.com",
            'x-rapidapi-key': Config.RAPIDAPI_KEY  # <- replaced from env
        }

        response = requests.get(
            "https://exerra-phishing-check.p.rapidapi.com/",
            headers=headers,
            params=querystring
        )

        return response.json()

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if isinstance(message.channel, disnake.DMChannel):
            return
        if Module(message.guild.id, "modules").is_disabled("AntiPhishing"):
            return

        for link in message.content.split(" "):
            CHECK = self.check_link(link)
            if CHECK and CHECK.get("isScam"):
                await message.delete()
                return await message.channel.send(
                    embed=disnake.Embed(
                        description=f"{message.author.mention}, it looks like you have sent a phishing link. Your message has therefore been deleted."
                    )
                )

def setup(bot):
    bot.add_cog(PhishingDetection(bot))
