from typing import List, Union
import disnake
from .Core import Database


class GuildCache(Database):
    def __init__(self):
        super().__init__("botCache", "guildCache")

    async def format_guild(self, guild: disnake.Guild):
        return {
            "name": guild.name,
            "icon": guild.icon.key if guild.icon else None,
            "description": guild.description,
            "member_count": guild.member_count,
            "ban_count": len(await guild.bans()),
            "invite_count": len(await guild.invites()),
            "channels": [{
                "id": str(channel.id),
                "name": channel.name,
                "type": channel.type.name
            } for channel in guild.channels],
            "roles": [{
                "id": str(role.id),
                "name": role.name,
                "permissions": role.permissions.value,
                "position": role.position
            } for role in guild.roles]
        }

    async def cache(self, guilds: List[disnake.Guild], bot):
        OLD = self.get()

        for guild in OLD:
            if not bot.get_guild(guild["_id"]):
                self.col.delete_one({
                    "_id": guild["_id"]
                })

        for guild in guilds:
            FORMATTED_GUILD = await self.format_guild(guild)
            if self.get_one(_id=str(guild.id)):
                self.col.update_one({
                    "_id": str(guild.id)
                }, {
                    "$set": {
                        **FORMATTED_GUILD
                    }
                })
            else:
                self.col.insert_one({
                    "_id": str(guild.id),
                    **FORMATTED_GUILD
                })


class Backups(Database):
    def __init__(self):
        super().__init__("Bot", "backups")

    def format_channel(self, channel: Union[disnake.TextChannel, disnake.VoiceChannel, disnake.CategoryChannel]):
        if not channel:
            return None

        overwrites = [{
            "type": "role" if isinstance(overwrite, disnake.Role) else "member",
            "allow": channel.overwrites[overwrite].pair()[0].value,
            "deny": channel.overwrites[overwrite].pair()[1].value,
            "id": str(overwrite.id),
            "name": str(overwrite.name)
        } for overwrite in channel.overwrites]

        DOC = {
            "name": channel.name,
            "category": channel.category.name if channel.category else None,
            "position": channel.position,
            "type": channel.type.name,
            "overwrites": overwrites
        }

        if isinstance(channel, disnake.TextChannel):
            DOC = {
                **DOC,
                "nsfw": channel.nsfw,
                "topic": channel.topic,
                "slowmode": channel.slowmode_delay,
            }
        elif isinstance(channel, disnake.VoiceChannel):
            DOC = {
                **DOC,
                "bitrate": channel.bitrate,
                "limit": channel.user_limit
            }

        return DOC

    def save(self, guild: disnake.Guild):
        DOC = {
            "name": guild.name,
            "channels": [self.format_channel(channel) for channel in guild.channels],
            "roles": [
                {
                    "color": role.color.value,
                    "name": role.name,
                    "hoist": role.hoist,
                    "position": role.position,
                    "mentionable": role.mentionable,
                    "permissions": role.permissions.value
                } for role in guild.roles if not role.managed
            ]
        }

        if not self.get_one(_id=str(guild.id)):
            self.col.insert_one({
                "_id": str(guild.id),
                **DOC
            })

        else:
            self.col.update_one({
                "_id": str(guild.id)
            }, {
                "$set": DOC
            })


class Rules(Database):
    def __init__(self):
        super().__init__("Bot", "rules")

    def default(self, guild: disnake.Guild, rule_title: str = "", rule_description: str = "", author_icon: str = "",
                author_name: str = "", color: str = "#000000", button_name: str = "", button_link: str = "",
                image_url: str = "", title:str = "", description:str = ""):
        self.col.insert_one({
            "_id": str(guild.id),
            "rules": [{"title": rule_title, "description": rule_description}] if rule_title != "" else [],
            "authorIcon": author_icon,
            "authorName": author_name,
            "color": color,
            "buttons": [{"label": button_name, "link": button_link}] if button_name != "" else [],
            "imageUrl": image_url,
            "title": title,
            "description": description
        })

    def add_rule(self, guild: disnake.Guild, rule_title: str, rule_description: str):
        if not self.get_one(_id=str(guild.id)):
            self.default(guild=guild, rule_title=rule_title, rule_description=rule_description)
        else:
            self.col.update_one({
                "_id": str(guild.id)
            }, {
                "$push": {
                    "rules": {"title": rule_title, "description": rule_description}
                }
            })

    def set_author(self, guild: disnake.Guild, author_icon: str, author_name: str):
        if not self.get_one(_id=str(guild.id)):
            self.default(guild=guild, author_icon=author_icon, author_name=author_name)
        else:
            self.col.update_one({
                "_id": str(guild.id)
            }, {
                "$set": {
                    "authorIcon": author_icon,
                    "authorName": author_name
                }
            })
        
    def set_title(self, guild: disnake.Guild, title: str, description: str):
        if not self.get_one(_id=str(guild.id)):
            self.default(guild=guild, title=title, description=description)
        else:
            self.col.update_one({
                "_id": str(guild.id)
            }, {
                "$set": {
                    "title": title,
                    "description": description
                }
            })

    def set_color(self, guild: disnake.Guild, color: str):
        if not self.get_one(_id=str(guild.id)):
            self.default(guild=guild, color=color)
        else:
            self.col.update_one({
                "_id": str(guild.id)
            }, {
                "$set": {
                    "color": color
                }
            })

    def add_button(self, guild: disnake.Guild, button_name: str, button_link: str):
        if not self.get_one(_id=str(guild.id)):
            self.default(guild=guild, button_name=button_name, button_link=button_link)
        else:
            self.col.update_one({
                "_id": str(guild.id)
            }, {
                "$push": {
                    "buttons": {"label": button_name, "link": button_link}
                }
            })

    def set_image(self, guild: disnake.Guild, image_url: str):
        if not self.get_one(_id=str(guild.id)):
            self.default(guild=guild, image_url=image_url)
        else:
            self.col.update_one({
                "_id": str(guild.id)
            }, {
                "$set": {
                    "imageUrl": image_url
                }
            })

    def get_rules(self, guild: disnake.Guild):
        if not self.get_one(_id=str(guild.id)):
            self.default(guild=guild)
            return {
                "_id": str(guild.id),
                "rules": [],
                "authorIcon": "",
                "authorName": "",
                "color": "#000000",
                "buttonName": "",
                "buttonLink": "",
                "imageUrl": ""
            }
        else:
            return self.col.find_one(_id=str(guild.id))
