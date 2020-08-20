import discord
from discord.ext import commands
import json
from const import ModChannels, OtherChannels, warningMessage, warningReport


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome = self.bot.get_channel(OtherChannels["welcome"])

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        with open('./config.json', 'r') as json_file:
            self.data = json.load(json_file)

        await self.rulesManagement(message_id=payload.message_id)
        await self.colourManagement(message_id=payload.message_id,
                                    guild_id=payload.guild_id)

    async def rulesManagement(self, message_id):
        if message_id != self.data["rules"]["id"]:
            return
        else:
            self.data["rules"]["id"] = "None"
            with open('./config.json', 'w') as json_file:
                json.dump(self.data, json_file)

    async def colourManagement(self, message_id, guild_id):
        try:
            list((colour, info)
                 for colour, info in self.data["roles"]["colour"].items()
                 if message_id == info["message"]["id"])[0]
        except IndexError:
            pass
        else:
            toDel = list(
                (colour, info)
                for colour, info in self.data["roles"]["colour"].items()
                if message_id == info["message"]["id"])[0]
            for shade in (toDel[1]["shades"]):
                role = self.bot.get_guild(guild_id).get_role(
                    toDel[1]["shades"][shade]["role"])
                await role.delete()
            del self.data["roles"]["colour"][toDel[0]]

            with open('./config.json', 'w') as json_file:
                json.dump(self.data, json_file)
        return

    @commands.Cog.listener()
    async def on_member_join(self, memeber):
        if memeber.bot:
            return
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title="(^-^)/ Heyo!",
            description=
            f'Welcome to the server, {memeber.mention}! Be sure to read and agree to the rules to start chatting',
        )
        await self.welcome.send(embed=embed)


def setup(bot):
    bot.add_cog(Logs(bot))