from turtle import title
import disnake, asyncio
from disnake.ext import commands
from core.Database import Backups
from core.files import Data


class InviteInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def autocomplete_invite_code(inter: disnake.ApplicationCommandInteraction, user_input: str):
        invites = []
        for invite in await inter.guild.invites():
            invites.append(invite.code)
        return invites

    @commands.slash_command(
        name="inviteinfo",
        description="Get information about a server invite"
    )
    async def invite_info(self, inter: disnake.CommandInteraction, code: str = commands.Param(autocomplete=autocomplete_invite_code)):
        invites = await inter.guild.invites()
        user_invite = None
        for invite in invites:
            if invite.code == code:
                user_invite = invite
        if user_invite is None:
            return await inter.send("This invite does not exist")
        emb = disnake.Embed(title=inter.guild.name, color=disnake.Color.from_rgb(r=255, g=255, b=255), description="About this Server Invite")
        emb.add_field(name="Inviter", inline=True, value=user_invite.inviter.name)
        emb.add_field(name="Channel", inline=True, value=user_invite.channel.mention)
        emb.add_field(name="Members", inline=True, value=len(inter.guild.members))
        return await inter.send(embed=emb)


def setup(bot):
    bot.add_cog(InviteInfo(bot))
