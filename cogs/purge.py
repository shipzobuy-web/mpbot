from turtle import title
import disnake, asyncio
from disnake.ext import commands
from core.Database import Backups
from core.Database.Modules import Module
from core.files import Data


class ConfirmView(disnake.ui.View):
    def __init__(self, delete_amount):
        super().__init__(timeout=300)
        self.delete_amount = delete_amount
        self.accepted = False

    @disnake.ui.button(label="Confirm", style=disnake.ButtonStyle.green)
    async def confirm_purge(self, guild: disnake.Guild, inter: disnake.MessageInteraction):
        self.accepted = True

        if isinstance(inter.channel, disnake.TextChannel):
            await inter.channel.purge(limit=self.delete_amount)
        self.stop()


class Purge(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="purge",
        description="Bulk delete messages",
        options=[
            disnake.Option(
                name="amount",
                description="Amount of messages to delete",
                type=disnake.OptionType.integer,
                required=True,
                min_value=1,
                max_value=100
            )
        ]
    )
    async def purge(self, inter: disnake.CommandInteraction, amount: int):
        if Module(inter.guild_id, "modules").is_disabled("Moderation"):
            return await inter.send("This module is disabled!", ephemeral=True)
        if not inter.author.guild_permissions.manage_messages:
            return inter.send("You need the `Manage Messages` permission to do this!", ephemeral=True)

        emb = disnake.Embed(title="Are you sure?", description=f"You are about to delete {amount} messages in this channel.")
        view = ConfirmView(delete_amount=amount+1)
        await inter.send(embed=emb, view=view)
        await view.wait()
        if not view.accepted:
            return await inter.edit_original_message(content="Canceled message purge.", embed=None, view=None)


def setup(bot):
    bot.add_cog(Purge(bot))
