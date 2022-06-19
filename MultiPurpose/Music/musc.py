import nextcord
from nextcord.ext import commands
import wavelink
from wavelink.ext import spotify
from nextcord.ext import menus
from nextcord import Embed 
import datetime
from Views.musicviews import MusicView
import asyncio
import aiohttp






class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        bot.loop.create_task(self.connect_nodes())

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=wavelink.Player, context=obj)
        elif isinstance(obj, nextcord.Guild):
            return self.wavelink.get_player(obj.id, cls=wavelink.Player)

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.bot,
                                            host= 'losingtime.dpaste.org',
                                            port= 2124,
                                            password= "SleepingOnTrains",
                                            spotify_client=spotify.SpotifyClient(client_id= "ur spotify client id", client_secret= "ur spotify client secret"))

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node: <{node.identifier}> is ready!')

    @commands.Cog.listener()
    async def on_wavelink_track_end(self,player: wavelink.Player, track:wavelink.YouTubeTrack, reason):
        msg = player.msg
        try:
            await msg.delete()
            song = player.queue.get()
            await player.play(song)
            
            
            
        except wavelink.QueueEmpty:
            pass


    @commands.Cog.listener()
    async def on_wavelink_track_start(self, player, track):
        ctx = player.reply
        duration=str(datetime.timedelta(seconds=track.duration))
        embed = Embed(title="Currently Playing",description=f"```py\n{track.title}```",colour=0xFF0000)


        embed.add_field(name="Duration",
        value=f"{duration}")
        embed.add_field(name="Link",value=f"[Url of the video]({track.uri})")
        try:
            embed.add_field(name="Author",
            value=track.author)
        except:
            pass


        msg = await ctx.send(embed=embed, view=MusicView())
        player.msg = msg
    



    @commands.command(aliases=["p"])
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        if ctx.author.voice:
            if not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                vc: wavelink.Player = ctx.voice_client
            vc.ctx = ctx
            vc.reply=ctx.channel
            
            if not vc.is_paused() and not vc.is_playing():
                duration=str(datetime.timedelta(seconds=search.duration))
                embed = Embed(title="Currently Playing",description=f"```py\n{search.title}```",colour=0xFF0000)

                embed.set_thumbnail(url=search.thumbnail)
                embed.add_field(name="Duration",
                value=f"{duration}")
                embed.add_field(name="Link",value=f"[Url of the video]({search.uri})")
                try:
                    embed.add_field(name="Author",
                    value=search.author)
                except:
                    pass
                await ctx.send(embed=embed, delete_after = 5)
                await vc.play(search)
            elif vc.is_playing():
                vc.queue.put(search)
                print(vc.queue)
                await ctx.send(f"{search} Added to the queue.")
        else:
            return await ctx.send(f"{ctx.author.mention} you are not in a voice channel")


    @commands.command()
    async def remove(self,ctx, remove:int):
        if ctx.author.voice:
            player : wavelink.Player = ctx.voice_client
            queue=player.queue
            try:
                del queue[remove - 1]
            except:
                return await ctx.send(f"There are no items in the queue at index {remove}")

            await ctx.send(f"Removed Queued item from {remove} index")
        else:
            return await ctx.send(f"{ctx.author.mention} You are not connected to a voice channel.")

    @commands.command()
    async def playlist(self, ctx, query):
        if ctx.author.voice:
            if not ctx.voice_client:
                player: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                player: wavelink.Player = ctx.voice_client
            player.reply = ctx.channel
            async with ctx.typing():
                if player.is_playing() and not player.is_paused():
                    async for track in spotify.SpotifyTrack.iterator(query=query, type=spotify.SpotifySearchType.playlist):
                        player.queue.put(track)
                elif not player.is_paused() and not player.is_playing():
                    async for track in spotify.SpotifyTrack.iterator(query=query, type=spotify.SpotifySearchType.playlist):
                        player.queue.put(track)
                    song = player.queue.get()
                    await player.play(song)
        else:
            return await ctx.send(f"{ctx.author.mention} You are not connected to a voice channel.")
        

            
    @commands.command(aliases=["con","connect"])
    async def join(self, ctx):
        try:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        except:
            return await ctx.send(f"{ctx.author.mention} you have to join a voice channel, you want the bot to join.")


def setup(bot):
    bot.add_cog(Music(bot))
