from discord.ext import commands
import discord
import json
from const import OtherChannels, liveMessage, serverId


class Streaming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not [
                activity for activity in before.activities
                if activity.type == discord.ActivityType.streaming
        ] and [
                activity for activity in after.activities
                if activity.type == discord.ActivityType.streaming
        ]:
            streamAct = [
                activity for activity in after.activities
                if activity.type == discord.ActivityType.streaming
            ]

            if streamAct[0].platform == 'Twitch':
                streamEmbed = await self.streamNotify(streamAct=streamAct[0],
                                                      after=after)
                await self.bot.get_channel(OtherChannels['goingLive']).send(
                    content=liveMessage.format(streamAct[0].twitch_name,
                                               streamAct[0].url),
                    embed=streamEmbed)
            else:
                print(streamAct[0].platform)
                print(type(streamAct[0].platform))

    async def streamNotify(self, streamAct, after):
        embed = discord.Embed(colour=discord.Colour.from_rgb(145, 71, 255),
                              title=streamAct.name,
                              url=streamAct.url)
        embed.set_author(name=streamAct.twitch_name, icon_url=after.avatar_url)
        embed.set_thumbnail(url=after.avatar_url)
        embed.add_field(name="Game", value=streamAct.game)
        embed.set_image(
            url=
            f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{streamAct.twitch_name}-320x180.jpg"
        )
        return embed


def setup(bot):
    bot.add_cog(Streaming(bot))