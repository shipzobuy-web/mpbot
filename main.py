import disnake, os, textwrap, io, traceback

from contextlib import redirect_stdout

from core.files import Data
from core import checks

from disnake.ext import commands

config = Data("config").json_read()

bot = commands.Bot(command_prefix=config["prefix"], case_insensitive=True, help_command=None, intents=disnake.Intents.all())

def get_folders():
  return [i for i in [x for x in os.walk("cogs")][0][1] if i.find(".") == -1]

@bot.event
async def on_ready():
    print("Bot is ready!")

@checks.manager()
@bot.command()
async def eval(ctx : disnake.Interaction, body: str, hidden: bool):
    raw = False
    """Evaluates a code"""

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
        else:
            pass
      
    await ctx.followup.send("Code was executed successfully!")

@checks.manager()
@bot.command()
async def load(ctx, module):
    folders = get_folders()
    if module in folders:
      for file in [i for i in os.listdir(f"cogs/{module}") if i.endswith(".py")]:
          try:
              bot.load_extension(f"cogs.{folder}.{file[:-3]}")
              print(f"Loaded {file}")
          except Exception as e:
              print(f"######\nFailed to load {folder}.{file}: {e}\n######")
      return ctx.send(embed=disnake.Embeds(
        title="Loaded Directory",
        description=f"Loaded all cogs inside the `{module}` directory.",
        color=disnake.Color.green()
      ))
    try:
      bot.load_extension(f"cogs.{module}")
    except commands.ExtensionError as e:
      await ctx.send(f'{e.__class__.__name__}: {e}')
    else:
      embed=disnake.Embed(title=f"Loaded {str(module).capitalize()}", description=f"Successfully loaded cogs.{str(module).lower()}!", color=0x2cf818)
      await ctx.send(embed=embed)

@checks.manager()
@bot.command()
async def unload(ctx, *, module):
    folders = get_folders()
    if module in folders:
      for file in [i for i in os.listdir(f"cogs/{module}") if i.endswith(".py")]:
          try:
              bot.unload_extension(f"cogs.{folder}.{file[:-3]}")
              print(f"Loaded {file}")
          except Exception as e:
              print(f"######\nFailed to load {folder}.{file}: {e}\n######")
      return ctx.send(embed=disnake.Embeds(
        title="Unloaded Directory",
        description=f"Unloaded all cogs inside the `{module}` directory.",
        color=disnake.Color.red()
      ))
    try:
      bot.unload_extension(f"cogs.{module}")
    except commands.ExtensionError as e:
      await ctx.send(f'{e.__class__.__name__}: {e}')
    else:
      embed=disnake.Embed(title=f"Unloaded {str(module).capitalize()}", description=f"Successfully unloaded cogs.{str(module).lower()}!", color=0xeb1b2c)
      await ctx.send(embed=embed)

@checks.manager()
@bot.command(name='reload')
async def _reload(ctx, *, module):
    folders = get_folders()
    if module in folders:
      for file in [i for i in os.listdir(f"cogs/{module}") if i.endswith(".py")]:
          try:
              bot.reload_extension(f"cogs.{folder}.{file[:-3]}")
              print(f"Loaded {file}")
          except Exception as e:
              print(f"######\nFailed to load {folder}.{file}: {e}\n######")
      return ctx.send(embed=disnake.Embeds(
        title="Reloaded Directory",
        description=f"Reloaded all cogs inside the `{module}` directory.",
        color=disnake.Color.blurple()
      ))
    try:
      bot.reload_extension(f"cogs.{module}")
    except commands.ExtensionError as e:
      await ctx.send(f'{e.__class__.__name__}: {e}')
    else:
      embed=disnake.Embed(title=f"Reloaded {str(module).capitalize()}", description=f"Successfully reloaded cogs.{str(module).lower()}!", color=0x00d4ff)
      await ctx.send(embed=embed)

for file in [i for i in os.listdir("cogs") if i.endswith(".py")]:
    try:
        bot.load_extension(f"cogs.{file[:-3]}")
        print(f"Loaded {file}")
    except Exception as e:
        print(f"######\nFailed to load {file}: {e}\n######")

dirs = [i for i in [x for x in os.walk("cogs")][0][1] if i.find(".") == -1]

for folder in dirs:
  for file in [i for i in os.listdir(f"cogs/{folder}") if i.endswith(".py")]:
      try:
          bot.load_extension(f"cogs.{folder}.{file[:-3]}")
          print(f"Loaded {file}")
      except Exception as e:
          print(f"######\nFailed to load {folder}.{file}: {e}\n######")

bot.run(config["token"])
