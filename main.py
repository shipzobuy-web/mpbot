import disnake
import os
import textwrap
import io
import traceback
from contextlib import redirect_stdout
from disnake.ext import commands

from core import checks
from core.config import Config  # <- new config file from env

# Initialize bot
bot = commands.Bot(
    command_prefix=Config.PREFIX,
    case_insensitive=True,
    help_command=None,
    intents=disnake.Intents.all()
)

# Helper function to get all folders in "cogs"
def get_folders():
    return [i for i in [x for x in os.walk("cogs")][0][1] if i.find(".") == -1]

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}.")

# ------------------- COMMANDS -------------------

@checks.manager()
@bot.command()
async def eval(ctx: disnake.Interaction, body: str, hidden: bool = False):
    """Evaluates code"""
    raw = False
    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
    }
    env.update(globals())

    stdout = io.StringIO()
    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        if ret is None:
            if value:
                if raw:
                    await ctx.send(f"{value}")
                else:
                    await ctx.send(f'```py\n{value}\n```')

    await ctx.followup.send("Code was executed successfully!")

# Generic load/unload/reload commands
async def handle_module(ctx, module: str, action: str):
    folders = get_folders()
    if module in folders:
        for file in [i for i in os.listdir(f"cogs/{module}") if i.endswith(".py")]:
            try:
                getattr(bot, f"{action}_extension")(f"cogs.{module}.{file[:-3]}")
                print(f"{action.capitalize()}ed {file}")
            except Exception as e:
                print(f"######\nFailed to {action} {module}.{file}: {e}\n######")
        color_map = {"load": 0x2cf818, "unload": 0xeb1b2c, "reload": 0x00d4ff}
        return await ctx.send(embed=disnake.Embed(
            title=f"{action.capitalize()}ed Directory",
            description=f"{action.capitalize()}ed all cogs inside `{module}` directory.",
            color=color_map.get(action, 0x2cf818)
        ))
    try:
        getattr(bot, f"{action}_extension")(f"cogs.{module}")
    except commands.ExtensionError as e:
        await ctx.send(f'{e.__class__.__name__}: {e}')
    else:
        color_map = {"load": 0x2cf818, "unload": 0xeb1b2c, "reload": 0x00d4ff}
        embed = disnake.Embed(
            title=f"{action.capitalize()}ed {module.capitalize()}",
            description=f"Successfully {action}ed cogs.{module.lower()}!",
            color=color_map.get(action, 0x2cf818)
        )
        await ctx.send(embed=embed)

@checks.manager()
@bot.command()
async def load(ctx, module: str):
    await handle_module(ctx, module, "load")

@checks.manager()
@bot.command()
async def unload(ctx, module: str):
    await handle_module(ctx, module, "unload")

@checks.manager()
@bot.command(name='reload')
async def _reload(ctx, module: str):
    await handle_module(ctx, module, "reload")

# ------------------- LOAD ALL COGS -------------------

# Load single-file cogs in "cogs"
for file in [i for i in os.listdir("cogs") if i.endswith(".py")]:
    try:
        bot.load_extension(f"cogs.{file[:-3]}")
        print(f"Loaded {file}")
    except Exception as e:
        print(f"######\nFailed to load {file}: {e}\n######")

# Load folder cogs
for folder in get_folders():
    for file in [i for i in os.listdir(f"cogs/{folder}") if i.endswith(".py")]:
        try:
            bot.load_extension(f"cogs.{folder}.{file[:-3]}")
            print(f"Loaded {file}")
        except Exception as e:
            print(f"######\nFailed to load {folder}.{file}: {e}\n######")

# ------------------- RUN BOT -------------------
bot.run(Config.TOKEN)
