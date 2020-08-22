from discord.ext import commands
import discord
import json
from const import OtherChannels, liveMessage, serverId, pieLive, pieloaf
from datetime import datetime, timedelta


class Streaming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.onCoolDown = []

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        afterStreamingAct = [
            activity for activity in after.activities
            if activity.type == discord.ActivityType.streaming
        ]

        beforeStreamingAct = [
            activity for activity in before.activities
            if activity.type == discord.ActivityType.streaming
        ]

        if not beforeStreamingAct and afterStreamingAct:

            isOnCoolDown = [
                item for item in self.onCoolDown if item[0] == after.id
            ]

            if isOnCoolDown:
                item = isOnCoolDown[0]
                if datetime.now < item[1]:
                    return
                else:
                    self.onCoolDown.remove(item)

            if after.id != pieloaf:
                messageContent = liveMessage.format(
                    afterStreamingAct[0].twitch_name, afterStreamingAct[0].url)
            else:
                messageContent = pieLive

            if afterStreamingAct[0].platform == 'Twitch':
                streamEmbed = await self.streamNotify(
                    streamAct=afterStreamingAct[0], after=after)
                await self.bot.get_channel(OtherChannels['goingLive']
                                           ).send(content=messageContent,
                                                  embed=streamEmbed)

        elif [beforeStreamingAct] and not [afterStreamingAct]:
            self.onCoolDown.append(
                (after.id, datetime.now + timedelta(minutes=30)))

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