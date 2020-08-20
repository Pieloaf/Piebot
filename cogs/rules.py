import discord
from discord.ext import commands
import json
from const import serverId


class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rules(self, ctx):
        with open('./config.json', 'r') as json_file:
            self.data = json.load(json_file)

        try:
            await ctx.message.attachments[0].save('rules.txt')
        except IndexError:
            await ctx.send(
                "Please attach a text file of the rules (one rule per line)")
        else:
            with open('./rules.txt', 'r') as rules_file:
                rules = "\u2022 " + rules_file.read().replace(
                    "\n", "\n\n\u2022 ")

            self.embed = discord.Embed(
                colour=discord.Colour.blue(),
                title="Please Read and Agree to the Rules",
            )
            self.embed.set_thumbnail(url=self.bot.get_guild(serverId).icon_url)
            self.embed.add_field(name="Rules:", value=rules)
            self.embed.add_field(
                name="React to the message to agree to the rules",
                value="Thank you ❤️",
                inline=False)

            if self.data["rules"]["id"] == "None":
                message = await ctx.send(embed=self.embed)
                await message.add_reaction('✅')
                self.data["rules"]["id"] = message.id
                self.data["rules"]["channel"] = message.channel.id
                with open('./config.json', 'w') as json_file:
                    json.dump(self.data, json_file)
            else:
                message = await self.bot.get_channel(
                    self.data["rules"]["channel"]
                ).fetch_message(int(self.data["rules"]["id"]))
                await message.edit(embed=self.embed)


def setup(bot):
    bot.add_cog(Rules(bot))
