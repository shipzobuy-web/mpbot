from turtle import title
import disnake, asyncio
from disnake.ext import commands
from core.Database import Rules
import validators

from core.Database.Modules import Module

class AddRuleModal(disnake.ui.Modal):
    def __init__(self) -> None:
        components = [
            disnake.ui.TextInput(
                label="Select a title",
                placeholder="Title of the rule",
                custom_id="rule_title",
                style=disnake.TextInputStyle.single_line,
                min_length=1,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Add a description",
                placeholder="Explain your rule. Be as detailed as possible!",
                custom_id="rule_description",
                style=disnake.TextInputStyle.paragraph,
                max_length=200,
            )
        ]
        super().__init__(title="Add Rule", custom_id="add_rule", components=components)

    async def callback(self, inter: disnake.ModalInteraction) -> None:

        Rules().add_rule(guild=inter.guild, rule_title=inter.text_values.get("rule_title"), rule_description=inter.text_values.get("rule_description"))
        emb = disnake.Embed(title="New rule has been added")
        await inter.send(embed=emb)

    async def on_error(self, error: Exception, inter: disnake.ModalInteraction) -> None:
        print(error)
        await inter.response.send_message("Oops, something went wrong.", ephemeral=True)

class RulesView(disnake.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @disnake.ui.button(label="Add Rule", style=disnake.ButtonStyle.blurple)
    async def add_rule(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(modal=AddRuleModal())
        self.stop()

    @disnake.ui.button(label="Set Title", style=disnake.ButtonStyle.blurple)
    async def set_title(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(
            title="Set Title",
            custom_id="set_title",
            components=[
                disnake.ui.TextInput(
                    label="Title",
                    placeholder="Title...",
                    custom_id="title",
                    style=disnake.TextInputStyle.single_line,
                    max_length=50
                ),
                disnake.ui.TextInput(
                    label="Description",
                    placeholder="Description",
                    custom_id="description",
                    style=disnake.TextInputStyle.multi_line,
                    max_length=500
                )
            ]
        )
        try:
            modal_inter: disnake.ModalInteraction = await self.bot.wait_for(
                "modal_submit",
                check=lambda i: i.custom_id == "set_title" and i.author.id == inter.author.id,
                timeout=300,
            )
            Rules().set_title(guild=inter.guild, title=modal_inter.text_values.get("title"), description=modal_inter.text_values.get("description"))
            await modal_inter.send(content="Title has been set!")
            self.stop()
        except asyncio.TimeoutError:
            await inter.send(content="Your modal timed out, please try again!")
            self.stop()

    @disnake.ui.button(label="Set Image", style=disnake.ButtonStyle.blurple)
    async def add_image(self, button: disnake.Button, inter: disnake.MessageInteraction):
        emb = disnake.Embed(title="Set an Image", description="Add your image per link or upload it!")
        await inter.send(embed=emb)

        def check(m: disnake.Message):
            return m.author.id == inter.user.id and m.channel.id == inter.channel_id

        msg: disnake.Message = await self.bot.wait_for(event="message", check=check)
        if len(msg.attachments) > 0:
            Rules().set_image(guild=inter.guild, image_url=msg.attachments[0].url)
        elif validators.url(msg.content):
            Rules().set_image(guild=inter.guild, image_url=msg.content)
        else:
            return await msg.channel.send(content="Please make sure you provided a valid URL that points to an image or uploaded a file!")
        await msg.channel.send(content="Image has been added!")

        self.stop()

    @disnake.ui.button(label="Set Author", style=disnake.ButtonStyle.blurple)
    async def add_author(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(
            title="Set Author",
            custom_id="add_author",
            components=[
                disnake.ui.TextInput(
                    label="Author Name",
                    placeholder="Name of the author",
                    custom_id="author_name",
                    style=disnake.TextInputStyle.single_line,
                    max_length=50
                ),
                disnake.ui.TextInput(
                    label="Author Icon Url",
                    placeholder="Url of the Author you want to put in",
                    custom_id="author_icon",
                    style=disnake.TextInputStyle.single_line,
                    max_length=500
                )
            ]
        )
        try:
            modal_inter: disnake.ModalInteraction = await self.bot.wait_for(
                "modal_submit",
                check=lambda i: i.custom_id == "add_author" and i.author.id == inter.author.id,
                timeout=300,
            )
            Rules().set_author(guild=inter.guild, author_icon=modal_inter.text_values.get("author_icon"), author_name=modal_inter.text_values.get("author_name"))
            await modal_inter.send(content="Author has been set!")
            self.stop()
        except asyncio.TimeoutError:
            await inter.send(content="Your modal timed out, please try again!")
            self.stop()

    @disnake.ui.button(label="Set Color", style=disnake.ButtonStyle.blurple)
    async def add_color(self, button: disnake.Button, inter: disnake.MessageInteraction):
        emb = disnake.Embed(title="Set Color", description="Send the hex value of the color (example: #ffb469)")
        await inter.send(embed=emb)

        def check(m: disnake.Message):
            return m.author.id == inter.user.id and m.channel.id == inter.channel_id

        msg: disnake.Message = await self.bot.wait_for('message', check=check)
        if not msg.content.startswith('#'):
            return await inter.channel.send(content="Your hex color needs to start with a #")
        if len(msg.content) != 7:
            return await inter.channel.send(content="Your hex value must be exactly 7 characters long! (example: #ffb469)")
        Rules().set_color(guild=inter.guild, color=msg.content.lstrip("#"))
        await inter.channel.send(content="Your color has been set to the rules!")
        self.stop()

    @disnake.ui.button(label="Add Button", style=disnake.ButtonStyle.blurple)
    async def add_button(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(
            title="Add Button",
            custom_id="add_button",
            components=[
                disnake.ui.TextInput(
                    label="Button Label",
                    placeholder="The Label to be printed on the Button",
                    custom_id="button_label",
                    style=disnake.TextInputStyle.single_line,
                    max_length=50
                ),
                disnake.ui.TextInput(
                    label="Button Url",
                    placeholder="Url the Button will lead to",
                    custom_id="button_url",
                    style=disnake.TextInputStyle.single_line,
                    max_length=500
                )
            ]
        )
        try:
            modal_inter: disnake.ModalInteraction = await self.bot.wait_for(
                "modal_submit",
                check=lambda i: i.custom_id == "add_button" and i.author.id == inter.author.id,
                timeout=300,
            )
            Rules().add_button(guild=inter.guild, button_name=modal_inter.text_values.get("button_label"), button_link=modal_inter.text_values.get("button_url"))
            await modal_inter.send(content="Button was added!")
        except asyncio.TimeoutError:
            await inter.send(content="Your modal timed out, please try again!")
        self.stop()


class SetRules(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="set-rules",
        description="Set up your server rules with ease and post them in the rules channel",
        guild_ids=[862481678722793493]
    )
    async def set_rules(self, inter: disnake.CommandInteraction):
        if Module(inter.guild_id, "modules").is_disabled("Rules"):
            return await inter.send("This module is disabled!", ephemeral=True)
        
        if not inter.author.guild_permissions.manage_guild:
            return await inter.send("You need the `Manage Guild` permission to do this!", ephemeral=True)

        emb = disnake.Embed(title="Add to your Rules", description="You can add a new rule, an image, an author and buttons to your embed!", color=disnake.Color.from_rgb(r=255, g=255, b=255))
        return await inter.send(embed=emb, view=RulesView(self.bot))

    @commands.slash_command(
        name="rules",
        description="Send the server rules",
        guild_ids=[862481678722793493]
    )
    async def send_rules(self, inter: disnake.CommandInteraction):
        if Module(inter.guild_id, "modules").is_disabled("Rules"):
            return await inter.send("This module is disabled!", ephemeral=True)

        rules = Module(inter.guild_id, "rules").get()

        if not rules: return await inter.send("Rules are not set up in the server!", ephemeral=True)
        
        rule_embed = disnake.Embed(
            title=rules["title"],
            description=rules["description"],
            color=disnake.Color(value=int(rules["color"], 16)),
        )

        if validators.url(rules["imageUrl"]):
            rule_embed.set_image(rules["imageUrl"])

        if rules["authorName"]:
            extra = {}
            if validators.url(rules["authorIcon"]):
                extra["icon_url"] = rules["authorIcon"]
            rule_embed.set_author(name=rules["authorName"], **extra)

        for rule in rules["rules"]:
            rule_embed.add_field(name=rule["title"], value=rule["description"], inline=False)

        components = []
        
        for button in rules["buttons"]:
            if validators.url(button["link"]):
                components.append(disnake.ui.Button(label=button["label"], url=button["link"], style=disnake.ButtonStyle.blurple))

        await inter.channel.send(embed=rule_embed, components=components)
        return await inter.send("Rules were sent!", ephemeral=True)



def setup(bot):
    bot.add_cog(SetRules(bot))
