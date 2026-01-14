from modulefinder import Module
import disnake
from datetime import datetime
from disnake.ext import commands, tasks

class AntiRaid(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.last_join = {}
        self.count = {}
        self.reset_detect.start()

    @tasks.loop(seconds=30, reconnect=True)
    async def reset_detect(self):
        self.last_join = {}
        self.count = {}
    
    @commands.Cog.listener()
    async def on_member_join(self, member:disnake.Member):
        if Module(member.guild.id, "modules").is_disabled("AntiRaid"): return
        if not member.guild in self.last_join:
            self.last_join[member.guild] = datetime.utcnow()
            self.count[member.guild] = 0

        else:
            if (datetime.utcnow()-self.last_join[member.guild]).seconds <= 10 and self.count[member.guild] > 6:
                raid_members = [m for m in member.guild.members if m.joined_at >= self.last_join]
                for member in raid_members:
                    await member.ban(reason="Raid", delete_message_days=7)

            elif (datetime.utcnow()-self.last_join[member.guild]).seconds > 10:
                self.last_join[member.guild] = datetime.utcnow()

    @commands.Cog.listener()
    async def on_message(self, message:disnake.Message):
        if isinstance(message.channel, disnake.DMChannel) or message.author.guild_permissions.manage_guild or message.author.bot: return

        if len(message.mentions) >= 5:
            await message.delete()
            return await message.channel.send(embed=disnake.Embed(
                description=f"{message.author} has mass-pinged, therefore their message has been deleted."
            ))

    
def setup(bot):
    bot.add_cog(AntiRaid(bot))