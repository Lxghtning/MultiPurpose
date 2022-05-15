import nextcord
from nextcord.ext import commands, menus
import asyncio
import challonge
import aiosqlite
from nextcord import Embed
from Views.confirm import Confirm

my_username = '_Lxghtning'
my_api_key = 'W43AOHwes2zSDKm4AVoJPlHEe1nqigaP7IBgarJr'

class Tourney(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(aliases=["tournaments","mytournaments","my-tourneys","tourney","my-tournaments"])
    async def tourneys(self, ctx):
        """Shows all of your tournaments."""
        async with ctx.typing():
            my_user = await challonge.get_user(my_username, my_api_key)
            my_tournaments = await my_user.get_tournaments()
            embed = Embed()
            for t in my_tournaments:
                embed.add_field(name="Tourney Name",value=t.name)
                embed.add_field(name="Tourney Url",value=t.full_challonge_url)
            await ctx.send(embed=embed)

    @commands.command(aliases=["create-tourney","createtourney","ct"])
    async def create(self, ctx):
        "Starts the process to create a tournament."
        async with ctx.typing():
            try:
                await ctx.send(f"Please enter the name of the tournament.")
                msg = await self.bot.wait_for('message',check = lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout=60)
                name=msg.content
                await ctx.send(f"Please enter the URL of the tournament.")
                msg = await self.bot.wait_for('message',check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel, timeout=60)
                url=msg.content
            except asyncio.TimeoutError:
                return await ctx.send(f"{ctx.author.mention} This process has timed out. If you want to create a tournament then please use the command again.")
            my_user = await challonge.get_user(my_username, my_api_key)
            try:
                new_tournament = await my_user.create_tournament(name=name,
                                                        url=url)
            except challonge.APIException:
                return await ctx.send(f"Hey {ctx.author.name} it seems that the tournament URL you provided has already been taken. Please try a new URL.")
            
    
    @commands.command(aliases=["del-tourney","delete","deltourney"])
    async def destroy(self, ctx, name):
        """Deletes a tourney completely. This process is not un-doable."""
        view=Confirm()
        if view.value == None:
            return await ctx.send(f"{ctx.author.mention} This process has timed out.")
        elif view.value:
            async with ctx.typing():
                try:
                    my_user = await challonge.get_user(my_username, my_api_key)
                    tourney = await my_user.get_tournament(url=name)
                    await my_user.destroy_tournament(tourney)
                    await ctx.send(f"Deleted.")
                except challonge.APIException:
                    return await ctx.send(f"Tournament not found.")
        else:
            return await ctx.send(f"Process has been cancelled.")

    
    @commands.command()
    async def reg(self, ctx):
        async with ctx.typing():
            try:
                await ctx.send(f"Please enter the name of the tournament you wish to register for.")
                msg = await self.bot.wait_for('message',check = lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout=60)
                tourney_name=msg.content
                await ctx.send(f"Please enter your display name for the tournament.")
                msg = await self.bot.wait_for('message',check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel, timeout=60)
                display_name=msg.content
            except asyncio.TimeoutError:
                return await ctx.send(f"{ctx.author.mention} This process has timed out. If you want to register then please use the command again.")
            my_user = await challonge.get_user(my_username, my_api_key)
            try:
                tourney = await my_user.get_tournament(url=tourney_name)
            except:
                return await ctx.send("No such tournament has been found.")
            await tourney.add_participant(display_name=display_name)
            await ctx.send(f"Added.")
    
    @commands.command()
    async def start(self, ctx, name):
        async with ctx.typing():
            my_user = await challonge.get_user(my_username, my_api_key)
            tourney = await my_user.get_tournament(url=name)
            await tourney.start()
            await ctx.send(f"The tournament has been started.")
            
    @commands.command()
    async def winner(self, ctx, pname,score,*,name):
        async with ctx.typing():
            
            my_user = await challonge.get_user(my_username, my_api_key)
            new_tournament = await my_user.get_tournament(url=name)
            matches = await new_tournament.get_matches()
            await matches[0].report_winner(pname, score)


    @commands.command()
    async def unreg(self, ctx, name,*,pname):
        async with ctx.typing():
            my_user = await challonge.get_user(my_username, my_api_key)
            tourney = await my_user.get_tournament(url=name)
            

def setup(bot):
    bot.add_cog(Tourney(bot))