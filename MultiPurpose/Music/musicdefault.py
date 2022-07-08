import nextcord
from nextcord.ext import menus, commands
from nextcord import Embed
import wavelink
from wavelink.ext import spotify
from datetime import datetime as dt

class SoundEmbed(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=5)

    async def format_page(self, menu, names):

        embed = Embed(title=f"Queue",colour=0xFF0000)
        i=1
        for name in names:
            for queue_items in name:
                embed.add_field(name=i,
                value=f"```{queue_items}```",
                inline=False)
                i+=1
    
        embed.set_footer(text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
        return embed




class Music(commands.Cog):
    """Music cog to hold Wavelink related commands and listeners."""

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
                                            spotify_client=spotify.SpotifyClient(client_id= "ur id", client_secret= "ur secret"))

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node: <{node.identifier}> is ready!')

    @commands.Cog.listener()
    async def on_wavelink_track_end(self,player: wavelink.Player, track:wavelink.YouTubeTrack, reason):
        ctx = player.reply
            
        try:
            song = player.queue.get()
            await player.play(song)
            duration=f'{(track.duration/60):.2f}'.replace(".",":")
            embed = Embed(title="Currently Playing",description=f"```py\n{track.title}```",colour=0xFF0000)
            ##embed.timestamp = dt.datetime.now()

            embed.add_field(name="Duration",
            value=f"{duration}")
            embed.add_field(name="Link",value=f"[Url of the video]({track.uri})")
            try:
                embed.add_field(name="Author",
                value=track.author)
            except:
                pass
            await ctx.send(embed=embed)
            
            
        except wavelink.QueueEmpty:
            pass
    
    

    @commands.command()
    async def queue(self, ctx):
        if ctx.author.voice:
            try:
                player : wavelink.Player = ctx.voice_client
            except:
                return await ctx.send(f"Not playing any music right now.") 
            
            names = [player.queue]

            pages = menus.ButtonMenuPages(
                    source=SoundEmbed(names),
                    disable_buttons_after=True,
            )
            await pages.start(ctx)
        else:
            return await ctx.send(f"{ctx.author.mention} you are not in a voice channel.")



    @commands.command()
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        if ctx.author.voice:
            if not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                vc: wavelink.Player = ctx.voice_client
                print (type(ctx.voice_client))
                print(type(search))
            vc.c = ctx
            vc.reply=ctx.channel
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel,self_deaf=True,self_mute=False)
            if not vc.is_paused() and not vc.is_playing():
                duration=f'{(search.duration/60):.2f}'.replace(".",":")
                embed = Embed(title="Currently Playing",description=f"```py\n{search.title}```",colour=0xFF0000)
                embed.timestamp = dt.now()
                embed.set_thumbnail(url=search.thumbnail)
                embed.add_field(name="Duration",
                value=f"{duration}")
                embed.add_field(name="Link",value=f"[Url of the video]({search.uri})")
                try:
                    embed.add_field(name="Author",
                    value=search.author)
                except:
                    pass
                await ctx.send(embed=embed)
                await vc.play(search)
            elif vc.is_playing():
                vc.queue.put(search)
                print(vc.queue)
                await ctx.send(f"{search} Added to the queue.")
        else:
            return await ctx.send(f"{ctx.author.mention} you are not in a voice channel")

    @commands.command()
    async def seek(self,ctx,num:int):
        if ctx.author.voice:
            try:
                player : wavelink.Player = ctx.voice_client
            except:
                return await ctx.send(f"{ctx.author.mention} Join a voice channel first.")
            
            curr_pos = player.position

            time = ((num*1000)+(curr_pos*1000))
            print(time)
            if not player.is_paused() and player.is_playing():
                await player.seek(time)
                await ctx.send(f"Successfully seeked {num} seconds")
            else:
                return await ctx.send(f"Not playing any music right now.")
        else:
            return await ctx.send(f"{ctx.author.mention} you are not in a voice channel.")

    @commands.command()
    async def pause(self,ctx):
        if ctx.author.voice:
            player : wavelink.Player = ctx.voice_client
            
            try:
                if not player.is_paused() and player.is_playing():
                    await player.pause()
                    await ctx.send(f"Player has been paused.")
                else:
                    return await ctx.send(f"Not playing any music right now.")
            except:
                return await ctx.send(f"{ctx.author.mention} Bot is not in a voice channel")
        else:
            return await ctx.send(f"{ctx.author.mention} you are not in a voice channel")
        
    @commands.command(aliases=["next"])
    async def skip(self, ctx):
        if ctx.author.voice:
            player : wavelink.Player = ctx.voice_client
                
            try:
                if not player.is_paused() and player.is_playing():
                    
                    next_sound = player.queue.get()
                    await player.stop()
                    await player.play(next_sound)
                    await ctx.send(f"Currently playing {next_sound}")
                else:
                    return await ctx.send(f"Not playing any music right now.")
            except:
                return await ctx.send(f"{ctx.author.mention} Bot is not in a voice channel")
        else:
                return await ctx.send(f"{ctx.author.mention} you are not in a voice channel")
    
    @commands.command(aliases=["eq","equalizer"])
    async def equaliser(self, ctx, preset):
        if ctx.author.voice:
            player : wavelink.Player = ctx.voice_client
            try:
                if not player.is_paused() and player.is_playing():
                    if preset.lower() == "boost":
                        await player.set_filter(wavelink.Filter(ctx.voice_client.filter, equalizer=wavelink.Equalizer.boost()))
                        await ctx.send(f"Equalizer set to **Boost**.")
                    elif preset.lower() == "flat":
                        await player.set_filter(wavelink.Filter(ctx.voice_client.filter, equalizer=wavelink.Equalizer.flat()))
                        await ctx.send(f"Equalizer set to **Flat**.")
                    elif preset.lower() == "piano":
                        await player.set_filter(wavelink.Filter(ctx.voice_client.filter, equalizer=wavelink.Equalizer.piano()))
                        await ctx.send(f"Equalizer set to **Piano**.")
                    elif preset.lower() == "metal":
                        await player.set_filter(wavelink.Filter(ctx.voice_client.filter, equalizer=wavelink.Equalizer.metal()))
                        await ctx.send(f"Equalizer set to **Metal**.")
                    else:
                        return await ctx.send(f"Not a valid preset.")
                else:
                    return await ctx.send(f"Not playing any music right now.")
            except:
                return await ctx.send(f"{ctx.author.mention} Bot is not in a voice channel")
        else:
            return await ctx.send(f"{ctx.author.mention} you are not in a voice channel")
            
    @commands.command()
    async def resume(self,ctx):
        if ctx.author.voice:
            try:
                player : wavelink.Player = ctx.voice_client
            except:
                return await ctx.send(f"{ctx.author.mention} You are not in a voice channel.")
            try:    
                await player.resume()
                await ctx.send(f"Player has been resumed.")
            except:
                return await ctx.send(f"No music is being played right now.")
        else:
            return await ctx.send(f"{ctx.author.mention} you are not in a voice channel")
        
    @commands.command(aliases=["con","connect"])
    async def join(self, ctx):
        try:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        except:
            return await ctx.send(f"{ctx.author.mention} you have to join a voice channel, you want the bot to join.")

    @commands.command(aliases=["discon","disconnect"])
    async def leave(self, ctx):
        if ctx.author.voice:
            if ctx.voice_client:
                player : wavelink.Player = ctx.voice_client
                
                try:
                    player.queue.clear()
                except:
                    pass
                try:
                    await player.stop()
                except:
                    pass
                await ctx.guild.voice_client.disconnect(force=False)

                await ctx.send(f"Disconnected from voice channel.")
            else:
                return await ctx.send(f"Bot is not in a voice channel.")
                
            
            
       

        else:
            return await ctx.send(f"{ctx.author.mention} You are not connected to a voice channel.")

    @commands.command(aliases=["vol"])
    async def volume(self,ctx,num:int):
        if ctx.author.voice:
            player : wavelink.Player = ctx.voice_client
            if 0 <= num <= 100:
                try:
                    await player.set_volume(num)
                except:
                    return await ctx.send(f"{ctx.author.mention} Not playing any music right now.")
            else:
                return await ctx.send(f"Volume inputted should be greater than or equal to 0 but less than or equal to 100.")
        else:
            return await ctx.send(f"{ctx.author.mention} You are not connected to a voice channel.")

    @commands.command()
    async def remove(self,ctx, remove:int):
        if ctx.author.voice:
            player : wavelink.Player = ctx.voice_client
            queue=player.queue
            try:
                del queue[remove - 1]
            except:
                return await ctx.send(f"There are no items in the queue at index {remove}.")

            await ctx.send(f"Removed Queued item from {remove} index.")
        else:
            return await ctx.send(f"{ctx.author.mention} You are not connected to a voice channel.")



def setup(bot):
    bot.add_cog(Music(bot))
