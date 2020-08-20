import discord
from discord.ext import commands
import json
from const import bakerRole


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = payload.message_id
        guild = self.bot.get_guild(payload.guild_id)

        if payload.user_id == self.bot.user.id:
            return

        with open('./config.json', 'r') as json_file:
            self.data = json.load(json_file)

        if message == self.data["rules"]["id"]:
            await payload.member.add_roles(guild.get_role(bakerRole))

        for colour, info in self.data["roles"]["colour"].items():
            if message == info["message"]["id"]:
                await self.managecolour(payload, colour)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message = payload.message_id
        guild = self.bot.get_guild(payload.guild_id)
        if payload.user_id == self.bot.user.id:
            return

        with open('./config.json', 'r') as json_file:
            self.data = json.load(json_file)

        if message == self.data["rules"]["id"]:
            await guild.get_member(payload.user_id
                                   ).remove_roles(guild.get_role(bakerRole))

        for colour, info in self.data["roles"]["colour"].items():
            if message == info["message"]["id"]:
                await self.managecolour(payload, colour, give=False)

    async def managecolour(self, payload, colour, give=True):
        guild = self.bot.get_guild(payload.guild_id)
        for key, val in self.data["roles"]["colour"][colour]["shades"].items():
            if val["emoji"] == str(payload.emoji):
                reacted = key

        if give == True:
            for role in payload.member.roles:
                for values in self.data["roles"]["colour"].values():
                    for info in values["shades"].values():
                        if role.id == info["role"]:
                            remove = await self.bot.get_channel(
                                values["message"]["channel"]
                            ).fetch_message(values["message"]["id"])
                            await payload.member.remove_roles(role)
                            await remove.remove_reaction(
                                info["emoji"], payload.member)

            await payload.member.add_roles(
                guild.get_role(self.data["roles"]["colour"][colour]["shades"]
                               [reacted]["role"]))

        else:
            await guild.get_member(payload.user_id).remove_roles(
                guild.get_role(self.data["roles"]["colour"][colour]["shades"]
                               [reacted]["role"]))

        with open('./config.json', 'w') as json_file:
            json.dump(self.data, json_file)


def setup(bot):
    bot.add_cog(Reactions(bot))
