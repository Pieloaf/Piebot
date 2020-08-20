import discord
from discord.ext import commands
import json


class Colours(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.colourname = None
        self.footer = """\n\n__Setting Colour Variants__
+colour [name] [hex] [emoji]

__Finish__
+cancel -> this will quit the colour set up
+setcolour -> this will complete the colour menu setup"""

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def colour(self, ctx):
        if not self.colourname:
            try:
                ctx.message.content.split()[1]
            except IndexError:
                await ctx.send(
                    "Please enter a colour name e.g. `+colour green`")
                return
            else:
                self.colourname = (' ').join(ctx.message.content.split()[1:])

            with open('./config.json', 'r') as json_file:
                self.data = json.load(json_file)
            self.data["roles"]["colour"][self.colourname] = {
                "shades": {},
                "message": None
            }
            self.variants = ""

            self.header = f"**Colour Menu Set Up**\nColour Name: **{self.colourname}**\n\n__Colour Variants Added__"
            self.setup = await ctx.send(f"{self.header}{self.footer}")
            return
        elif len(ctx.message.content.split()[1:]) != 3:
            await ctx.send(
                "To set colour variants, please use the correct format: +colour [name] [hex] [emoji]\nUse +setcolour to finish set up\nUse +cancel to cancel setup"
            )
            return
        else:
            await self.addcolvar(ctx.message.content.split()[1:])
            await self.setup.edit(
                content=f"{self.header}{self.variants}{self.footer}")

    async def addcolvar(self, attrs):
        self.data["roles"]["colour"][self.colourname]["shades"][attrs[0]] = {
            "value": attrs[1],
            "emoji": attrs[2],
            "role": None
        }
        self.variants = self.variants + '\n-> ' + attrs[0] + ' ' + attrs[
            2] + " ✓"

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def cancel(self, ctx):
        del self.data["roles"]["colour"][self.colourname]

        await self.setup.delete()
        self.setup = self.variants = self.colourname = None

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def setcolour(self, ctx):
        if not self.colourname:
            await ctx.send(
                "No colour currently being set. Please start colour set up with `+colour [name]`"
            )
            return

        embed = discord.Embed(colour=discord.Colour(0xef283f), )
        fieldval = ""
        for colour, info in self.data["roles"]["colour"][
                self.colourname]["shades"].items():
            role = await ctx.guild.create_role(
                name=f"{colour}",
                colour=discord.Colour(int(info["value"].strip('#'), 16)))
            positions = {role: len(ctx.guild.roles) - 2}
            await ctx.guild.edit_role_positions(positions=positions)
            info["role"] = role.id
            emoji = info["emoji"]
            fieldval = fieldval + f"{emoji} :: {role.mention}\n"

        embed.add_field(name=self.colourname, value=fieldval, inline=False)
        msg = await ctx.send(embed=embed)
        self.data["roles"]["colour"][self.colourname]["message"] = {
            "id": msg.id,
            "channel": msg.channel.id
        }
        for colour, info in self.data["roles"]["colour"][
                self.colourname]["shades"].items():
            await msg.add_reaction(info["emoji"])
        with open('./config.json', 'w') as json_file:
            json.dump(self.data, json_file)
        await self.setup.delete()
        self.setup = self.variants = self.colourname = None


def setup(bot):
    bot.add_cog(Colours(bot))
