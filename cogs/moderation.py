import discord
from discord.ext import commands
import os
import re
from const import ModChannels, warningReport, warningMessage, secondWarning, secondWarningReport
import json


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.colourname = None

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def reload(self, ctx, extension):
        self.bot.reload_extension(f'cogs.{extension}')

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def reloadAll(self, ctx):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.bot.reload_extension(f'cogs.{filename[:-3]}')
                print(f'loaded {filename}')

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def delete(self, ctx):
        toDelete = int(ctx.message.content.split()[1])
        async for msg in ctx.channel.history(limit=toDelete + 1):
            await msg.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        badWords = re.search(r"(fag|retar|dyke|nigg|cunt)\w*", message.content)
        if badWords is not None:
            await self.WordsModeration(message)
        # await self.bot.process_commands(message)

    async def WordsModeration(self, message):
        with open('./config.json', 'r') as json_file:
            self.data = json.load(json_file)
        await message.delete()
        if not message.author.name in self.data["warnings"]:
            await message.author.send(warningMessage)
            await self.bot.get_channel(ModChannels['warnings']).send(
                warningReport.format(message.author, message.content))
            self.data["warnings"].append(message.author.name)
        else:
            await message.author.send(secondWarning)
            await self.bot.get_channel(ModChannels['warnings']).send(
                secondWarningReport.format(message.author, message.content))
        with open('./config.json', 'w') as json_file:
            json.dump(self.data, json_file)
        return


def setup(bot):
    bot.add_cog(Moderation(bot))