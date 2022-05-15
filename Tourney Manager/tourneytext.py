import nextcord
from nextcord.ext import commands, menus
import random
import aiosqlite
from Views.confirm import Confirm
from nextcord.ext.commands import Context
import asyncio
from nextcord import Embed, Member

class TourneyMenu(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=10)

    async def format_page(self, menu, entries):
        embed = Embed(title="Tournament Details", color=0xFF0000)

        for entry in entries:
            embed.add_field(name=f"User Details", value=f"**User Mention** - <@{entry[0]}>\n\n**Team Name** - **{entry[1]}**", inline=False)


        embed.set_footer(text=f"Page {menu.current_page + 1}/{self.get_max_pages()}")
        return embed

class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = None
        self.bot.loop.create_task(self.connect_database())

    async def connect_database(self):
        self.db = await aiosqlite.connect('D:\\MultiPurpose-Nextcord\\Tourney Manager\\tournament.db')

    @commands.command(aliases=["createtourney","create-tourney"])
    @commands.has_permissions(administrator=True)
    async def create(self, ctx: Context):
        cursor = await self.db.cursor()
        try:
            await ctx.send("Please enter the name of the tournament to be created.")
            msg = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 60)
            if msg.content == "cancel" or msg.content ==  "abort":
                return await ctx.send(f"Process successfully aborted.")
            else:
                tourney_name = msg.content
            await ctx.send("How many slots of teams should be able to enter the tournament?")
            msg = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 60)
            if msg.content == "cancel" or msg.content ==  "abort":
                return await ctx.send(f"Process successfully aborted.")
            else:
                slots = msg.content
                try:
                    if int(slots) <= 0:
                        return await ctx.send(f"Slots can't be in negative integers or `0`.")
                except:
                    return await ctx.send(f"Slots should be a number.")
        except asyncio.TimeoutError:
            return await ctx.send(f"{ctx.author.mention} The process was neither aborted nor did you replied in 60 seconds, Hence it was timed out.")

        await cursor.execute("INSERT INTO tourneys (user_id, tourney_name, slots) VALUES(?,?,?)",(ctx.author.id, tourney_name, int(slots)))
        await self.db.commit()
        embed = Embed(title="Created a tournament",description=f"\n\n```A tournament was created```\n\n**Responsible admin** - {ctx.author}\n\n**Tournament Name** - {tourney_name}\n\n**Number of slots** - {slots}",color=0xFF0000)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_author(name=ctx.author,icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["reg"])
    async def register(self, ctx: Context):
        cursor = await self.db.cursor()
        try:
            await ctx.send(f"Please enter tournament name you want to register for.")
            msg = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 60)
            if msg.content == "cancel" or msg.content ==  "abort":
                return await ctx.send(f"Process successfully aborted.")
            else:
                tourney_name = msg.content
            await cursor.execute("SELECT * FROM tourneys WHERE tourney_name = ?",(tourney_name,))
            tourney = await cursor.fetchone()
            if tourney == None:
                return await ctx.send(f"{ctx.author.mention} Unfortunately there is no such tournament with the name of {tourney_name}. Please use the command again to register for a valid tournament.")
            else:
                slots = tourney[2]
                await cursor.execute("SELECT team_name FROM users WHERE tourney_name = ?",(tourney_name,))
                res = await cursor.fetchone()
                try:
                    team_len = len(res)
                    print(slots, team_len)
                    if slots <= team_len:
                        return await ctx.send(f"{ctx.author.mention} It seems that the slots of this tournament is full.")
                except TypeError:
                    await ctx.send(f"Please enter the team name.")
                    msg = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 60)
                    if msg.content == "cancel" or msg.content ==  "abort":
                        return await ctx.send(f"Process successfully aborted.")
                    else:
                        team_name = msg.content
                    await ctx.send("Please enter the player details.")
                    msg = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 60)
                    if msg.content == "cancel" or msg.content ==  "abort":
                        return await ctx.send(f"Process successfully aborted.")
                    else:
                        for index, item in enumerate(msg.mentions):
                            for members in ctx.guild.members:
                                if members == item:
                                    if members.bot: 
                                        return await ctx.send(f"One of the players mentioned was a bot. Process successfully aborted...")
                                    else:
                                        await cursor.execute("SELECT * FROM users WHERE user_id = ? AND tourney_name = ?",(members.id,tourney_name))
                                        res = await cursor.fetchone()
                                        if res == None:
                                            await cursor.execute("INSERT INTO users (user_id, team_name, tourney_name) VALUES(?,?,?)",(members.id, team_name, tourney_name))
                                            await self.db.commit()
                                        else:
                                            return await ctx.send(f"{members.mention} is already registered for the {res[1]} team in this tournament. Process successfully aborted.")
                        await ctx.send(f"Successfully registered {team_name} into {tourney_name}.")

                else:
                    await ctx.send(f"Please enter the team name.")
                    msg = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 60)
                    if msg.content == "cancel" or msg.content ==  "abort":
                        return await ctx.send(f"Process successfully aborted.")
                    else:
                        team_name = msg.content
                    await ctx.send("Please enter the player details.")
                    msg = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 60)
                    if msg.content == "cancel" or msg.content ==  "abort":
                        return await ctx.send(f"Process successfully aborted.")
                    else:
                        for index, item in enumerate(msg.mentions):
                            for members in ctx.guild.members:
                                
                                if members == item:
                                    if members.bot: 
                                        return await ctx.send(f"One of the players mentioned was a bot. Process successfully aborted...")
                                    else:
                                        await cursor.execute("SELECT * FROM users WHERE user_id = ? AND tourney_name = ?",(members.id,tourney_name))
                                        res = await cursor.fetchone()
                                        if res == None:
                                            await cursor.execute("INSERT INTO users (user_id, team_name, tourney_name) VALUES(?,?,?)",(members.id, team_name, tourney_name))
                                            await self.db.commit()
                                            await ctx.send(f"Successfully registered {team_name} into {tourney_name}.")
                                        else:
                                            return await ctx.send(f"{members.mention} is already registered for the {res[1]} team in this tournament. Process successfully aborted.")

                        await ctx.send(f"Successfully registered {team_name} into {tourney_name}.")                        
        except asyncio.TimeoutError:
            return await ctx.send(f"{ctx.author.mention} The process was neither aborted nor did you replied in 60 seconds, Hence it was timed out.")

    @commands.command(aliases=['unreg-team',"unregister-team","unregteam"])
    @commands.has_permissions(administrator=True) 
    async def unregister_team(self, ctx):
        view=Confirm()
        e = Embed(description="**Are you sure you want to unregister?**")
        e.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=e,view=view)
        await view.wait()
        cursor = await self.db.cursor()
        if view.value is None:
            return await ctx.send(f"{ctx.author.mention} You have timed out")
        elif view.value:
            try:
                await ctx.send(f"Please enter the team name.")
                msg = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 60)
                if msg.content == "cancel" or msg.content == "abort":
                    return await ctx.send(f"Process successfully aborted.")
                else:
                    team_name = msg.content
                await ctx.send(f"Please enter the tournament name to unregister from.")
                msg = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 60)
                if msg.content == "cancel" or msg.content == "abort":
                    return await ctx.send(f"Process successfully aborted.")
                else:
                    tourney_name = msg.content
            except asyncio.TimeoutError:
                return await ctx.send(f"{ctx.author.mention} The process was neither aborted nor did you replied in 60 seconds, Hence it was timed out.")
            try:    
                await cursor.execute(f"DELETE FROM users WHERE tourney_name = ? AND team_name = ?",(tourney_name, team_name))
                await self.db.commit()
                await ctx.send(f"Successfully unregistered {team_name} from {tourney_name}.")
            except:
                return await ctx.send(f"No such team/tournament exists in the database.")
        else:
            return await ctx.reply("Process successfully cancelled.")

    @commands.command(aliases=['unreg-player',"unregister-player","unregplayer"])
    @commands.has_permissions(administrator=True)
    async def unregister_players(self, ctx):
        view=Confirm()
        e = Embed(description="**Are you sure you want to unregister?**")
        e.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=e,view=view)
        await view.wait()
        cursor = await self.db.cursor()
        if view.value is None:
            return await ctx.send(f"{ctx.author.mention} You have timed out")
        elif view.value:
            try:
                await ctx.send(f"Please enter the team name.")
                msg = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 60)
                if msg.content == "cancel" or msg.content == "abort":
                    return await ctx.send(f"Process successfully aborted.")
                else:
                    team_name = msg.content
                await ctx.send(f"Please mention the player.")
                msg = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 60)
                if msg.content == "cancel" or msg.content == "abort":
                    return await ctx.send(f"Process successfully aborted.")
                else:
                    for index, item in enumerate(msg.mentions):
                            for members in ctx.guild.members:
                                if members == item:
                                    if members.bot: 
                                        return await ctx.send(f"One of the players mentioned was a bot. Process successfully aborted...")
                                    else:
                                        await cursor.execute("DELETE FROM users WHERE user_id = ? AND team_name = ?",(members.id,team_name))
                                        await self.db.commit()
                                        await ctx.send(f"Successfully unregister the player(s) from the tournament.")
            except asyncio.TimeoutError:
                return await ctx.send(f"{ctx.author.mention} The process was neither aborted nor did you replied in 60 seconds, Hence it was timed out.")
        else:
            return await ctx.reply("Process successfully cancelled.")

    @commands.command(aliases=['unreg'])
    async def unregister(self, ctx):
        view=Confirm()
        e = Embed(description="**Are you sure you want to unregister?**")
        e.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=e,view=view)
        await view.wait()
        cursor = await self.db.cursor()
        if view.value is None:
            return await ctx.send(f"{ctx.author.mention} You have timed out")
        elif view.value:
            await cursor.execute("DELETE FROM users WHERE user_id = ?",(ctx.author.id,))
            await self.db.commit()
            await ctx.send(f"Successfully unregistered.")
        else:
            return await ctx.reply("Process successfully cancelled.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def brackets(self, ctx,tourney_name:str,*, num:int):
        cursor= await self.db.cursor()
        letters = [i for i in range(1,1000)]
        couples = []
        await cursor.execute("SELECT team_name FROM users WHERE tourney_name = ? ORDER BY RANDOM() LIMIT ?",(tourney_name,num+num))
        teams = await cursor.fetchall()
        for l in range(0, len(teams), 2):
            couples.append((teams[l], teams[l+1]))

        a= "\n\n".join(f"**{letters[l]}. {item[0][0]} vs {item[1][0]}**" for l, item in enumerate(couples))

        await ctx.send(a)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def tdelete(self, ctx, tourney_name):
        view=Confirm()
        await view.wait()
        if view.value is None:
            return await ctx.send(f"{ctx.author.mention} this process has timed out.")
        elif view.value:
            cursor = await self.db.cursor()
            try:
                await cursor.execute("DELETE FROM tourneys WHERE tourney_name=?",(tourney_name,))
                await self.db.commit()
            except:
                return await ctx.send(f"No tournament found with the name of {tourney_name}")
            try:
                await cursor.execute("DELETE FROM users WHERE tourney_name = ?",(tourney_name,))
                await self.db.commit()
            except:
                pass
            await ctx.send("The tournament has been deleted.")
        else:
            return await ctx.send(f"Process has been cancelled.")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def show(self, ctx, tourney_name):
        cursor = await self.db.cursor()
        await cursor.execute("SELECT * FROM tourneys WHERE tourney_name = ?",(tourney_name,))
        res = await cursor.fetchone()
        if res is not None:
            await cursor.execute("SELECT * FROM users WHERE tourney_name = ?",(tourney_name,))
            user_res = await cursor.fetchall()
        else:
            return await ctx.send(f"No tournament found with the name of {tourney_name}.")
        pages = menus.ButtonMenuPages(
        source=TourneyMenu(user_res),
        clear_buttons_after=True,
        )
        await pages.start(ctx)

def setup(bot):
    bot.add_cog(Tournament(bot))