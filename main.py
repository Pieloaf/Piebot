import discord
from discord.ext import commands
import os

TOKEN = 'NzQ2MDMyNTM4Mzk2NTI0NjE2.Xz6a8Q.ADF0Lt5AizkTu8g61MdEcL9aRe4'
bot = commands.Bot(command_prefix='+', help_command=None)

activityName = "Just Vibin\'"
activityType = discord.ActivityType(0)
activityObj = discord.Activity(name=activityName, type=activityType)


@bot.event
async def on_ready():
    print('Bot is now online')
    await bot.change_presence(status=discord.Status.online,
                              activity=activityObj)

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('const'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'loaded {filename}')


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        await ctx.author.send(
            "Error: Command not found. Use +help for a list valid of commands")
    raise error


bot.run(TOKEN)