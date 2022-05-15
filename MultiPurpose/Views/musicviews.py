import nextcord
import wavelink
from wavelink.ext import spotify
import aiohttp
from nextcord import Embed
from nextcord.ext import menus       

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

class MusicView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(emoji="⏯️",style=nextcord.ButtonStyle.green, custom_id="______resume_________",row=0)
    async def __resume__(self, button, interaction):
        if interaction.user.voice:
            try:
                player : wavelink.Player = interaction.guild.voice_client
            except:
                return await interaction.channel.send(f"{interaction.author.mention} You are not in a voice channel.",delete_after=5)
            if player.is_playing() and not player.is_paused():
                await player.pause()
                await interaction.channel.send(f"Player has been paused.",delete_after=5)
            elif player.is_paused() and not player.is_playing():
                await player.resume()
                await interaction.channel.send(f"Player has been resumed.",delete_after=5)

        else:
            return await interaction.channel.send(f"{interaction.author.mention} you are not in a voice channel",delete_after=5)

    @nextcord.ui.button(emoji="▶️",style=nextcord.ButtonStyle.primary, custom_id="______skip_________",row=0)
    async def __skip__(self, button, interaction):

        if interaction.user.voice:
            player : wavelink.Player = interaction.guild.voice_client
                
            try:
                if not player.is_paused() and player.is_playing():
                    
                    next_sound = player.queue.get()
                    await player.stop()
                    await player.play(next_sound)
                    await interaction.send(f"Currently playing {next_sound}",delete_after=5)
                else:
                    return await interaction.channel.send(f"Not playing any music right now.",delete_after=5)
            except wavelink.QueueEmpty:
                return await interaction.channel.send(f"Queue is empty.",delete_after=5)
        else:
            return await interaction.send(f"{interaction.author.mention} you are not in a voice channel",delete_after=5)

    @nextcord.ui.button(emoji="🚫",style=nextcord.ButtonStyle.red, custom_id="____leave_______", row=0)
    async def ____leave__(self, button, interaction):
        if interaction.user.voice:
            if interaction.guild.voice_client:
                player : wavelink.Player = interaction.guild.voice_client
                
                try:
                    player.queue.clear()
                except:
                    pass
                try:
                    await player.stop()
                except:
                    pass

                try:
                    await player.msg.delete()
                except:
                    pass
                await interaction.guild.voice_client.disconnect(force=False)
                await interaction.channel.send(f"Disconnected from voice channel.",delete_after=5)
            else:
                return await interaction.response.send_message(f"Bot is not in a voice channel.",ephemeral=True)
        else:
            return await interaction.response.send_message(f"You are not in a voice channel.",ephemeral=True)

    @nextcord.ui.button(emoji="🎶", style=nextcord.ButtonStyle.gray, custom_id = "________lyr_______", row=0)
    async def __lyr___(self, button, interaction):
        if interaction.user.voice:
            player : wavelink.Player = interaction.guild.voice_client
            if player.is_playing() and not player.is_paused():
                title = player.track.title
                async with aiohttp.ClientSession() as session:
                        async with session.get(f"https://some-random-api.ml/lyrics?title={title}") as response:
                                data = await response.json()
                                try:
                                    lyrics = data['lyrics']
                                except KeyError:
                                    return await interaction.response.send_message(data['error'])

                                if len(lyrics) > 2048:
                                    lyrics = lyrics[:2048]
                                emb = nextcord.Embed(title = f"{title}" , description = f"{lyrics}",color = 0xFF0000)
                                emb.set_thumbnail(url=player.track.thumbnail)
                                await interaction.channel.send(embed=emb)
                await session.close()
            else:
                return await interaction.response.send_message(f"Not playing any music currently.", ephemeral=True)
        else:
            return await interaction.response.send_message(f"{interaction.user.mention} You are not connected to a voice channel.",  ephemeral=True)


    @nextcord.ui.button(emoji="🎹",style=nextcord.ButtonStyle.gray, custom_id = "______eq_p________",row=1)
    async def __eq_p_(self, button, interaction):
        if interaction.user.voice:
            player : wavelink.Player = interaction.guild.voice_client
            if not player.is_paused() and player.is_playing():
                await player.set_filter(wavelink.Filter(interaction.guild.voice_client.filter, equalizer=wavelink.Equalizer.piano()))
                await interaction.channel.send(f"Successfully set the equaliser of the player to **Piano**.",delete_after=5)
            else:
                return await interaction.response.send_message("Not playing any music right now.",ephemeral=True)
        else:
            return await interaction.response.send_message("You are not in a voice channel.",ephemeral=True)

    @nextcord.ui.button(emoji="⚡",style=nextcord.ButtonStyle.gray, custom_id = "______eq_b________",row=1)
    async def __eq_b_(self, button, interaction):
        if interaction.user.voice:
            player : wavelink.Player = interaction.guild.voice_client
            if not player.is_paused() and player.is_playing():
                await player.set_filter(wavelink.Filter(interaction.guild.voice_client.filter, equalizer=wavelink.Equalizer.boost()))
                await interaction.channel.send(f"Successfully set the equaliser of the player to **Boost**.",delete_after=5)
            else:
                return await interaction.response.send_message("Not playing any music right now.",ephemeral=True)
        else:
            return await interaction.response.send_message("You are not in a voice channel.",ephemeral=True)

    @nextcord.ui.button(emoji="🎼",style=nextcord.ButtonStyle.gray, custom_id = "______eq_f________",row=1)
    async def __eq_f_(self, button, interaction):
        if interaction.user.voice:
            player : wavelink.Player = interaction.guild.voice_client
            if not player.is_paused() and player.is_playing():
                await player.set_filter(wavelink.Filter(interaction.guild.voice_client.filter, equalizer=wavelink.Equalizer.flat()))
                await interaction.channel.send(f"Successfully set the equaliser of the player to **Flat**.",delete_after=5)
            else:
                return await interaction.response.send_message("Not playing any music right now.",ephemeral=True)
        else:
            return await interaction.response.send_message("You are not in a voice channel.",ephemeral=True)

    @nextcord.ui.button(emoji="🎸",style=nextcord.ButtonStyle.gray, custom_id = "______eq_m________",row=1)
    async def __eq_m_(self, button, interaction):
        if interaction.user.voice:
            player : wavelink.Player = interaction.guild.voice_client
            if not player.is_paused() and player.is_playing():
                await player.set_filter(wavelink.Filter(interaction.guild.voice_client.filter, equalizer=wavelink.Equalizer.metal()))
                await interaction.channel.send(f"Successfully set the equaliser of the player to **Metal**.",delete_after=5)
            else:
                return await interaction.response.send_message("Not playing any music right now.",ephemeral=True)
        else:
            return await interaction.response.send_message("You are not in a voice channel.",ephemeral=True)

    @nextcord.ui.button(emoji="⏩",style=nextcord.ButtonStyle.gray, custom_id = "______seek________",row=2)
    async def __seek__(self, button, interaction):
        if interaction.user.voice:
            player : wavelink.Player = interaction.guild.voice_client
            if not player.is_paused() and player.is_playing():
                await player.seek(((5*1000)+(player.position*1000)))
                await interaction.channel.send('Successfully seeked 5 seconds.',delete_after = 5)
            else:
                return await interaction.response.send_message("Not playing any music right now.",ephemeral=True)
        else:
            return await interaction.response.send_message("You are not in a voice channel.",ephemeral=True)

    @nextcord.ui.button(emoji="⬆️",style=nextcord.ButtonStyle.gray, custom_id = "______volume_up________",row=2)
    async def __volume_up__(self, button, interaction):
        if interaction.user.voice:
            player : wavelink.Player = interaction.guild.voice_client
            if not player.is_paused() and player.is_playing():
                if player.volume < 1000:
                    await player.set_volume(player.volume + 10)
                    await interaction.channel.send(f'Successfully set the player volume to {player.volume}',delete_after = 5)
                else:
                    return await interaction.response.send_message('Player volume cannot be increased further.',ephemeral=True)
            else:
                return await interaction.response.send_message("Not playing any music right now.",ephemeral=True)
        else:
            return await interaction.response.send_message("You are not in a voice channel.",ephemeral=True)

    @nextcord.ui.button(emoji="⬇️",style=nextcord.ButtonStyle.gray, custom_id = "______volume_down________",row=2)
    async def __volume_down__(self, button, interaction):
        if interaction.user.voice:
            player : wavelink.Player = interaction.guild.voice_client
            if not player.is_paused() and player.is_playing():
                if player.volume <= 1000 and player.volume != 0:
                    await player.set_volume(player.volume - 10)
                    await interaction.channel.send(f'Successfully set the player volume to {player.volume}',delete_after = 5)
                else:
                    return await interaction.response.send_message('Player volume cannot be decreased further.',ephemeral=True)
            else:
                return await interaction.response.send_message("Not playing any music right now.",ephemeral=True)
        else:
            return await interaction.response.send_message("You are not in a voice channel.",ephemeral=True)


    @nextcord.ui.button(emoji="📃",style=nextcord.ButtonStyle.gray, custom_id = "______queue________",row=2)
    async def __queue__(self, button, interaction):
        if interaction.user.voice:
            player : wavelink.Player = interaction.guild.voice_client
            try:
                pages = menus.ButtonMenuPages(
                        source=SoundEmbed([player.queue]),
                        
                )

                await pages.start(player.ctx)


            except wavelink.QueueEmpty:
                return await interaction.response.send_message("The queue is empty.",ephemeral=True)
        else:
            return await interaction.response.send_message("You are not in a voice channel.",ephemeral=True)


