import discord
from discord.ext import commands
import asyncio
from discord.utils import get


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def song(self, ctx):
        user = ctx.author
        song = {}
        await ctx.message.delete()
        for activity in user.activities:
            if isinstance(activity, discord.Spotify):
                song['name'] = activity.title
                song['cover'] = activity.album_cover_url
                song['artists'] = str(', '.join(activity.artists))
                song['album'] = str(activity.album)
                song[
                    'link'] = f"https://open.spotify.com/track/{activity.track_id}"

        songEmbed = await self.spotifyEmbed(song, user)

        await ctx.send(embed=songEmbed)

    async def spotifyEmbed(self, song, user):
        embed = discord.Embed(colour=discord.Colour.from_rgb(30, 215, 96),
                              title=f"Song: {song['name']}",
                              url=song['link'])
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_thumbnail(url=song['cover'])
        embed.add_field(name="Artists:", value=song['artists'])
        embed.add_field(name=f"Album:", value=song['album'], inline=False)
        return embed


def setup(bot):
    bot.add_cog(Music(bot))