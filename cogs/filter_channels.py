import disnake, asyncio
from disnake.ext import commands
import validators
from core.Database.Modules import Module

class FilterChannels(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message:disnake.Message):
        if isinstance(message.channel, disnake.DMChannel) or message.author.bot: return
        if Module(message.guild.id, "modules").is_disabled("ContentProtect"): return

        channels = Module(message.guild.id, "channels").get()

        if not channels: return
        
        if "bot" in channels:
            if str(message.channel.id) in channels["bot"]:
                try:
                    bot_message: disnake.Message = await self.bot.wait_for(
                        "message",
                        check=lambda m: m.author.bot and m.channel.id == message.channel.id,
                        timeout=10
                    )
                    pass
                except asyncio.TimeoutError:
                    await message.delete()
                    return await message.channel.send(embed=disnake.Embed(
                        description=f"{message.author.mention} please make sure to chat in the respective channel."
                    ))
        
        if "youtube" in channels:
            if str(message.channel.id) in channels["youtube"]:
                if not "https://www.youtube.com/watch?v" in message.content:
                    await message.delete()
                    return await message.channel.send(embed=disnake.Embed(
                        description=f"{message.author.mention} please make sure to chat in the respective channel."
                    ))
        
        if "links" in channels:
            if str(message.channel.id) in channels["links"]:
                for word in message.content.split(" "):
                    if validators.url(word):
                        break
                else:
                    await message.delete()
                    return await message.channel.send(embed=disnake.Embed(
                        description=f"{message.author.mention} please make sure to chat in the respective channel."
                    ))
        
        if "media" in channels:
            if str(message.channel.id) in channels["media"]:
                if not message.attachments:
                    await message.delete()
                    return await message.channel.send(embed=disnake.Embed(
                        description=f"{message.author.mention} please make sure to chat in the respective channel."
                    ))
        

def setup(bot):
    bot.add_cog(FilterChannels(bot))