import disnake, asyncio
from disnake.ext import commands
from core.Database import Backups
from core.Database.Modules import Module

class BackupView(disnake.ui.View):
    def __init__(self):
        super().__init__()

    async def restore_backup(self, guild:disnake.Guild):
        backup = Backups().get_one(_id=str(guild.id))

        if not backup: return

        def fetch_category(categoryName):
            for category in guild.categories:
                if category.name == categoryName:
                    return category

        for item in (guild.channels+guild.roles):
            try:
                await item.delete()
                await asyncio.sleep(.3)
            except: continue
        
        await guild.edit(name=backup["name"])

        for role in backup["roles"]:
            if role["position"] == 0:
                await guild.default_role.edit(permissions=disnake.Permissions(role["permissions"]), mentionable=role["mentionable"], hoist=role["hoist"])
                continue

            await guild.create_role(
                name=role["name"],
                hoist=role["hoist"],
                mentionable=role["mentionable"],
                color=disnake.Color(role["color"]),
                permissions=disnake.Permissions(role["permissions"])
            )
        
        for channel in backup["channels"]:
            overwrites = {}

            for ow in channel["overwrites"]:
                if ow["type"] == "role":
                    try:
                        target = next(role for role in guild.roles if role.name == ow["name"])
                    except StopIteration:
                        continue
                else:
                    target = guild.get_member(int(ow["id"]))
                if not target: continue

                overwrites[target] = disnake.PermissionOverwrite.from_pair(disnake.Permissions(ow["allow"]), disnake.Permissions(ow["deny"]))

            if channel["type"] == "category":
                await guild.create_category(
                    name=channel["name"],
                    overwrites=overwrites
                )
            elif channel["type"] == "text":
                await guild.create_text_channel(
                    name=channel["name"],
                    category=fetch_category(channel["category"]),
                    overwrites=overwrites,
                    topic=channel["topic"],
                    nsfw=channel["nsfw"],
                    slowmode_delay=channel["slowmode"]
                )
            elif channel["type"] == "voice":
                await guild.create_voice_channel(
                    name=channel["name"],
                    category=fetch_category(channel["category"]),
                    overwrites=overwrites,
                    bitrate=channel["bitrate"],
                    user_limit=channel["limit"]
                )
        


    
    @disnake.ui.button(label="Create a Backup", style=disnake.ButtonStyle.blurple, custom_id="CreateButton")
    async def create_backup_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        msg = await inter.channel.send("Creating backup...")
        Backups().save(inter.guild)
        await msg.delete()
        await inter.send("Backup created!")
        self.stop()
    
    @disnake.ui.button(label="Restore from Backup", style=disnake.ButtonStyle.red, custom_id="RestoreButton")
    async def restore_backup_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.send("Restoring backup...")
        await self.restore_backup(inter.guild)
        self.stop()

class ServerRestore(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.slash_command(
        name="server-restore",
        description="Manage the server's backup state",
    )
    async def server_restore(self, inter:disnake.CommandInteraction):
        if Module(inter.guild_id, "modules").is_disabled("Backups"):
            return await inter.send("This module is disabled!", ephemeral=True)

        guild = inter.guild
        member = inter.author
        if guild.owner_id != member.id:
            return await inter.send(content="You're not allowed to run this command. Only the owner may restore server backups.", ephemeral=True)
        
        return await inter.send(embed=disnake.Embed(
            title="Server Restore",
            description="Server Restore allows you to create a backup of your server. In case your server gets nuked, you can easily restore the channels and roles!",
            color=disnake.Color.blue()
        ), view=BackupView())
    
def setup(bot):
    bot.add_cog(ServerRestore(bot))