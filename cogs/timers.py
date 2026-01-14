from disnake.ext import tasks, commands
from core.Database import Backups, GuildCache

class Timers(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.auto_backup.start()
        self.cache_guilds.start()

    @tasks.loop(hours=12, reconnect=True)
    async def auto_backup(self):
        await self.bot.wait_until_ready()
        backups = Backups()
        for guild in self.bot.guilds: backups.save(guild)

        print("Guilds backed up!")

    @tasks.loop(seconds=60, reconnect=True)
    async def cache_guilds(self):
        await self.bot.wait_until_ready()
        await GuildCache().cache(self.bot.guilds, self.bot)
        
        print("Guilds were cached!")

def setup(bot):
    bot.add_cog(Timers(bot))