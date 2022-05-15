from calendar import c
import nextcord
from nextcord.ext import commands, menus
from nextcord import Embed, Member, User
import humanfriendly
from datetime import datetime, time
import datetime as dt
import aiohttp
import asyncio
from io import BytesIO
import aiosqlite
from nextcord.ui import Button, View
from run import categs
from Views.ticket import Ticket_View




def convert(time):
    pos = ["s","m","h"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        COLOUR = 0xFF0000
        self.db=None
        self.bot.loop.create_task(self.warn_db_connect())

    async def warn_db_connect(self):
        await self.bot.wait_until_ready()
        self.db = await aiosqlite.connect("D:\\MultiPurpose-Nextcord\\Moderation\\warn_database.db")
        
    @commands.command(description="Kick's a mentioned member")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:nextcord.Member,*,reason="Sorry, we decided to kick you out"):
        "Kick a mentioned member"
        if member.top_role >= ctx.author.top_role:
            return await ctx.send(f"{ctx.author.mention} **{member.name}#{member.discriminator}** is either higher than your role or in the same position as you!")
        else:
            await member.kick()
            e = Embed(description=f"{ctx.author.mention} ***kicked*** **{member.name}#{member.discriminator}** , **The reason given was :- {reason}**!!",colour=0xFF0000)
            await ctx.send(embed=e)

    @commands.command(description="Ban a mentioned member")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:nextcord.Member,*,reason="Sorry, we decided to ban you from our server"):
        "Ban a mentioned member"
        if member.top_role >= ctx.author.top_role:
            return await ctx.send(f"{ctx.author.mention} **{member.name}#{member.discriminator}** is either higher than your role or in the same position as you!")
        else:
            await member.ban()
            e = Embed(description=f"{ctx.author.mention} ***banned*** **{member.name}#{member.discriminator}** , **The reason given was :- {reason}**!",colour=0xFF0000)
            await ctx.send(embed=e)
    
    @commands.command(description="Timeout's a member")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member:nextcord.Member,timee,*,reason=None):
        "Timeout a member"
        if reason==None:
            reason = "No reason given"
        if member.top_role >= ctx.author.top_role:
            return await ctx.send(f"{ctx.author.mention} **{member.name}#{member.discriminator}** is either higher than your role or in the same position as you!")
        if reason == None:
            reason = "No Reason Provided"
        try:
            time = humanfriendly.parse_timespan(timee)
            await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time))
            await ctx.send(f'{member.mention} was muted for {timee} because of {reason}')
            try:
                await member.send(f"You were muted in {ctx.guild.name} for {timee} because of {reason}")
            except:
                await ctx.send(f"{member.name}#{member.discriminator} has their DM's closed!")
        except:
            await ctx.send("The member is already muted!")

    @commands.command(description="Untimeout's a member")
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member:nextcord.Member):
        "Untimeout a member"
        if member.top_role >= ctx.author.top_role:
            return await ctx.send(f"{ctx.author.mention} **{member.name}#{member.discriminator}** is either higher than your role or in the same position as you!")
        try:
            await member.edit(timeout=None)
            await ctx.send(f"{member.mention} was unmuted!")
        except:
            return await ctx.send(f'{member.mention} is not muted!')

    @commands.command(name='poll', description="Start's a poll")
    @commands.has_permissions(manage_messages=True)
    async def quickpoll(self, ctx, question, *options: str):
        """Start a poll"""
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 items!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = nextcord.Embed(title=question, description=''.join(description), color=nextcord.Colour(0xFF355E))
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await react_message.edit(embed=embed)


    @commands.command(name='tally', description="Tallies the result of a poll with the given message ID")
    async def tally(self, ctx, pid):
        """Tally the result of a poll with the given message ID"""
        poll_message = await ctx.message.channel.fetch_message(pid)
        if not poll_message.embeds:
            return
        embed = poll_message.embeds[0]
        if poll_message.author != self.bot.user:
            return
        if not embed.footer.text.startswith('Poll ID:'):
            return
        unformatted_options = [x.strip() for x in embed.description.split('\n')]
        opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
            else {x[:1]: x[2:] for x in unformatted_options}
        # check if we're using numbers for the poll, or x/checkmark, parse accordingly
        voters = [self.bot.user.id]  # add the bot's ID to the list of voters to exclude it's votes

        tally = {x: 0 for x in opt_dict.keys()}
        for reaction in poll_message.reactions:
            if reaction.emoji in opt_dict.keys():
                reactors = await reaction.users().flatten()
                for reactor in reactors:
                    if reactor.id not in voters:
                        tally[reaction.emoji] += 1
                        voters.append(reactor.id)

        output = 'Results of the poll for "{}":\n'.format(embed.title) + \
                '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
        await ctx.send(output)


    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def steal_url(self, ctx, url:str,*,name):
        """Add an emoji from another server to your server"""
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    img_or_gif = BytesIO(await r.read())
                    b_value = img_or_gif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await ctx.guild.create_custom_emoji(image=b_value, name=name)
                        if emoji.animated:
                            await ctx.send(f"**{ctx.author.name}#{ctx.author.discriminator}** created emoji <a:{name}:{emoji.id}>(\<a:{name}:{emoji.id}>) with name **{name}**!")
                        else:
                            await ctx.send(f"**{ctx.author.name}#{ctx.author.discriminator}** created emoji <:{name}:{emoji.id}>(\<:{name}:{emoji.id}>) with name **{name}**!")
                        await ses.close()
                    else:
                        await ctx.send(f'{r.status} response got while uploading the emojis')
                        await ses.close()
                except nextcord.HTTPException:
                    return await ctx.send('Large File Size!')

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def steal(self, ctx, emojii:nextcord.Emoji,*,name):
        """Add an emoji from another server to your server"""
        url = emojii.url
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    img_or_gif = BytesIO(await r.read())
                    b_value = img_or_gif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await ctx.guild.create_custom_emoji(image=b_value, name=name)
                        if emoji.animated:
                            await ctx.send(f"**{ctx.author.name}#{ctx.author.discriminator}** created emoji <a:{name}:{emoji.id}>(\<a:{name}:{emoji.id}>) with name **{name}**!")
                        else:
                            await ctx.send(f"**{ctx.author.name}#{ctx.author.discriminator}** created emoji <:{name}:{emoji.id}>(\<:{name}:{emoji.id}>) with name **{name}**!")
                        await ses.close()
                    else:
                        await ctx.send(f'{r.status} response got while uploading the emojis')
                        await ses.close()
                except nextcord.HTTPException:
                    return await ctx.send('Large File Size!')
    
    @commands.command(description="Delete an emoji from the server")
    @commands.has_permissions(manage_emojis=True)
    async def delem(self, ctx, emoji:nextcord.Emoji):
        "Delete an emoji from the server"
        try:
            await emoji.delete()
        except: 
            emb = Embed(description=f"**:x: Emoji not found!**", color = 0xFF0000)
            emb.timestamp = dt.datetime.now()
            if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
            else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
            await ctx.send(embed=emb)
            return 
        emb = Embed(description=f"**Emoji deleted**", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)

    @commands.command(description="Create a text channel")
    @commands.has_permissions(manage_channels=True)
    async def createtc(self, ctx, name:str):
        "Create a text channel" 
        await ctx.guild.create_text_channel(name=name)
        emb = Embed(description=f"**Text channel created with the name of** __*{name}*__!", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)

    @commands.command(description="Delete a mentioned text channel")
    @commands.has_permissions(manage_channels=True)
    async def deltc(self, ctx, name:nextcord.TextChannel):
        "Delete a mentioned text channel"
        await name.delete()
        emb = Embed(description=f"**Text channel with the name of** __*{name}*__ **was deleted!**", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)

                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)



    @commands.command(description="Edit the name of a text channel")
    @commands.has_permissions(manage_channels=True)
    async def edittc(self,ctx, name:nextcord.TextChannel,*,namechange):
        "Edit the name of a text channel"
        await name.edit(name=namechange)
        emb = Embed(description=f"**Text channel with the name of** *{name}* **was edited to** *{namechange}*!", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)

    @commands.command(description="Create a voice channel")
    @commands.has_permissions(manage_channels=True)
    async def createvc(self, ctx, name:str):
        "Create a voice channel" 
        await ctx.guild.create_voice_channel(name=name)
        emb = Embed(description=f"**Voice channel created with the name of** __*{name}*__!", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)

    @commands.command(description="Delete a voice channel")
    @commands.has_permissions(manage_channels=True)
    async def delvc(self, ctx, name:str):
        "Delete a voice channel"
        try:
            vc = nextcord.utils.get(ctx.guild.voice_channels, name=name)
        except:
            emb = Embed(description=f"**No Voice Channel found with the name of** *{name}*!", color = 0xFF0000)
            emb.timestamp = dt.datetime.now()
            if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
            else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
            await ctx.send(embed=emb)
            return 
        await vc.delete()
        emb = Embed(description=f"**Voice channel deleted!**", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)

    @commands.command(description="Edit the name of a voice channel")
    @commands.has_permissions(manage_channels=True)
    async def editvc(self,ctx, name,*,namechange):
        "Edit the name of a voice channel"
        try: 
            vc = nextcord.utils.get(ctx.guild.voice_channels, name=name)
        except:
            emb = Embed(description=f"**No Voice Channel found with the name of** *{name}*", color = 0xFF0000)
            emb.timestamp = dt.datetime.now()
            if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
            else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
            await ctx.send(embed=emb)
            return 
        await vc.edit(name=namechange)
        emb = Embed(description=f"**Voice channel with the name of** __*{name}*__ **was edited to** __*{namechange}*__!", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)

    @commands.command(description="Purge a mentioned amount of messages from the channel used in")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: 100):
        "Purge a mentioned amount of messages from the channel used in"
        await ctx.channel.purge(limit=limit)
    
    @commands.command(description="Add a role to a mentioned member")
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, role:nextcord.Role,*, member:nextcord.Member):
        "Add a role to a mentioned member"
        if member.top_role >= ctx.author.top_role:
            return await ctx.send(f"{ctx.author.mention} **{member.name}#{member.discriminator}** is either higher than your role or in the same position as you!")
        await member.add_roles(role)
        emb = Embed(description=f"**{member.name}#{member.discriminator} was given the {role} role!**", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)
    
    @commands.command(description="Remove a role from a mentioned member")
    @commands.has_permissions(manage_roles=True)
    async def removeroles(self, ctx,role:nextcord.Role,*, member:nextcord.Member):
        "Remove a role from a mentioned member"
        if member.top_role >= ctx.author.top_role:
            return await ctx.send(f"{ctx.author.mention} **{member.name}#{member.discriminator}** is either higher than your role or in the same position as you!")
        await member.remove_roles(role)
        emb = Embed(description=f"**{member.name}#{member.discriminator} was removed from the the {role} role!**", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)

    @commands.command(aliases=["delcateg"],description="Delete a category along with the channels inside it")
    @commands.has_permissions(manage_channels=True)
    async def delcategory(self, ctx, categid:int):
        "Delete a category along with the channels inside it"
        try: 
            categ = nextcord.utils.get(ctx.guild.categories, id=categid)
        except:
            emb = Embed(description=f"**No category found with the ID of** *{categid}*", color = 0xFF0000)
            emb.timestamp = dt.datetime.now()
            if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
            else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
            await ctx.send(embed=emb)
            return 
        channels = categ.channels
        for channel in channels:
            try:
                await channel.delete()
            except AttributeError:
                pass
        await categ.delete()
        emb = Embed(description=f"**Deleted the category with ID of** *{categid}*!", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)
    
    @commands.command(aliases=["sm"],description="Set the slowmode of the channel")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self,ctx, timeinp):
        "Set the slowmode of the channel"
        time=convert(timeinp)
        try:
            await ctx.channel.edit(slowmode_delay=time)
        except:
            return await ctx.send(f"{ctx.author.mention} you have given incorrect time input!")
        emb = Embed(description=f"**A slowmode of {timeinp} was set for this channel by {ctx.author.mention}!**", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)
        
    @commands.command(aliases=["sm-all"],description="Set the slowmode of all the channels of the server")
    @commands.has_permissions(manage_channels=True)
    async def slowmodeall(self,ctx, time):
        "Set the slowmode of all the channels of the server"
        timee=convert(time)
        try:
            for channels in ctx.guild.channels:
                await channels.edit(slowmode_delay=timee)
        except:
            return await ctx.send(f"{ctx.author.mention} you have given incorrect time input!")

        emb = Embed(description=f"**A slowmode of {time} was set for all the channels of the server** {ctx.author.mention}!", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)
    
    @commands.command(aliases=["l"],description="Lock the channel in which used in")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        "Lock the channel in which used in"
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        emb = Embed(description=f"**Locked channel!**", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)

    @commands.command(aliases=["ul"],description="Unlock the channel in which used in")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        "Unlock the channel in which used in"
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        emb = Embed(description=f"**Unlocked channel!**", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)

    @commands.command(aliases=["lock-all","l-all"],description="Lock the channel in which used in")
    @commands.has_permissions(manage_channels=True)
    async def lockall(self, ctx):
        "Lock all the channels of the server"
        for channels in ctx.guild.channels:
            await channels.set_permissions(ctx.guild.default_role, send_messages=False)
        emb = Embed(description=f"**Locked all the channels of the server!**", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)

    @commands.command(aliases=["unlock-all","ul-all"],description="Unlock the channel in which used in")
    @commands.has_permissions(manage_channels=True)
    async def unlockall(self, ctx):
        "Unlock all the channels of the server"
        for channels in ctx.guild.channels:
            await channels.set_permissions(ctx.guild.default_role, send_messages=True)
        emb = Embed(description=f"**Unlocked all the channels of the server!**", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)

        
    @commands.command(description="Remove a role from all of the members in that role")
    @commands.has_permissions(manage_roles=True)
    async def rall(self, ctx, role:nextcord.Role):
        "Remove a role from all of the members in that role"
        await ctx.send(f"Removing {role}")
        for members in role.members:
            await members.remove_roles(role)
            a=(len(role.members))
        emb = Embed(description=f"**Removed {role} from {a} members** ", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)

    @commands.command(description="Add a role to all members of the server")
    @commands.has_permissions(manage_roles=True)
    async def all(self, ctx, role:nextcord.Role):
        "Add a role to all members of the server"
        await ctx.send(f"Removing {role}")
        for members in role.members:
            await members.remove_roles(role)
            a=(len(role.members))
        emb = Embed(description=f"**Added {role} to {a} members!**", color = 0xFF0000)
        emb.timestamp = dt.datetime.now()
        if ctx.guild.icon:
                emb.set_thumbnail(url=ctx.guild.icon.url)
        else:
                emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticket(self, ctx, channel: nextcord.TextChannel=None):
        channel = channel or ctx.channel
        embed = nextcord.Embed()

        def check(msg):
            return msg.channel == ctx.channel and msg.author == ctx.author
        try:
            view=Ticket_View()
            await ctx.send("What should be the embed colour in hex code?Write `None` to skip, the color would be red from default!")
            msg = await self.bot.wait_for('message', check=check,  timeout=60)

            if msg.content.lower() == 'none':
                embed.color = nextcord.Color.red()
            else:
                try:
                    embed.colour = await commands.ColourConverter().convert(ctx, msg.content)
                except:
                    return await ctx.send("Invalid Hex Code Provided! Please re-do the command!")
            await ctx.send("Please enter title!")
            msg = await self.bot.wait_for('message',check = check,timeout= 60)
            embed.title = msg.content
            await ctx.send("Please enter description!")
            msg = await self.bot.wait_for('message',check = check, timeout = 60)
            embed.description = msg.content
            await ctx.send("Please enter the url or write `None` to skip!")
            msg = await self.bot.wait_for( 'message', check=check, timeout=60)
            if msg.content.lower() == 'none':
                await ctx.send("Alright the embed wouldnt have an image!")
            else:

                embed.set_image(url=msg.content)
            await ctx.send("Alright! Now enter the thumbnail's url or write `None` to skip!")
            msg = await self.bot.wait_for('message', check=check, timeout=60)
            if msg.content.lower() == 'none':
                await ctx.send("Alright there wouldn't be a thumbnail!")
            else:

                embed.set_thumbnail(url=msg.content)
            await ctx.send("Do you want the embed to have a footer?Write `None` to skip or `Yes` if you want it to have a footer!")
            msg = await self.bot.wait_for('message', check=check, timeout=60)
            if msg.content.lower() == 'none':
                await ctx.send("Embed has been sent.")
                await channel.send(embed=embed, view=view)
            else:
                await ctx.send("Please enter the footer's icon url or write `None` to skip!")
                msg = await self.bot.wait_for('message', check=check, timeout=60)
                if msg.content.lower() == 'none':
                    await ctx.send("There wouldnt be an icon in the footer!")
                else:
                    embed.set_footer(icon_url=msg.content)
                await ctx.send("Please enter the footer's Content!")
                msg = await self.bot.wait_for('message', check=check, timeout=60)
                await ctx.send("Embed has been sent.")
                embed.set_footer(text=msg.content)
                await channel.send(embed=embed,view=view)

        

        except asyncio.TimeoutError:
            await ctx.send("Timeout for responding!")
            return
        
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def embed(self, ctx, channel: nextcord.TextChannel):
        embed = nextcord.Embed()

        def check(msg):
            return msg.channel == ctx.channel and msg.author == ctx.author
        try:
            await ctx.send("What should be the embed colour in hex code?Write `None` to skip, the color would be red from default!")
            msg = await self.bot.wait_for('message', check=check,  timeout=60)

            if msg.content.lower() == 'none':
                embed.color = nextcord.Color.red()
            else:
                try:
                    embed.colour = await commands.ColourConverter().convert(ctx, msg.content)
                except:
                    return await ctx.send("Invalid Hex Code Provided! Please re-do the command!")
            await ctx.send("Please enter title!")
            msg = await self.bot.wait_for('message',check = check,timeout= 60)
            embed.title = msg.content
            await ctx.send("Please enter description!")
            msg = await self.bot.wait_for('message',check = check, timeout = 60)
            embed.description = msg.content
            await ctx.send("Please enter the url or write `None` to skip!")
            msg = await self.bot.wait_for( 'message', check=check, timeout=60)
            if msg.content.lower() == 'none':
                await ctx.send("Alright the embed wouldnt have an image!")
            else:

                embed.set_image(url=msg.content)
            await ctx.send("Alright! Now enter the thumbnail's url or write `None` to skip!")
            msg = await self.bot.wait_for('message', check=check, timeout=60)
            if msg.content.lower() == 'none':
                await ctx.send("Alright there wouldn't be a thumbnail!")
            else:

                embed.set_thumbnail(url=msg.content)
            await ctx.send("Do you want the embed to have a footer?Write `None` to skip or `Yes` if you want it to have a footer!")
            msg = await self.bot.wait_for('message', check=check, timeout=60)
            if msg.content.lower() == 'none':
                await ctx.send("Embed has been sent.")
                await channel.send(embed=embed)
            else:
                await ctx.send("Please enter the footer's icon url or write `None` to skip!")
                msg = await self.bot.wait_for('message', check=check, timeout=60)
                if msg.content.lower() == 'none':
                    await ctx.send("There wouldnt be an icon in the footer!")
                else:
                    embed.set_footer(icon_url=msg.content)
                await ctx.send("Please enter the footer's Content!")
                msg = await self.bot.wait_for('message', check=check, timeout=60)
                if msg.content.lower() == 'none':
                    await ctx.send("Foooter content cant be `None`! Please use the `-embed` command again!")
                    return

                else:
                    await ctx.send("Embed has been sent.")
                    embed.set_footer(text=msg.content)
                    await channel.send(embed=embed)

        

        except asyncio.TimeoutError:
            await ctx.send("Timeout for responding!")
            return

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def ssetup(self,ctx):
        """Sets up server stats"""
        categ = await ctx.guild.create_category("📊 SERVER STATS 📊")
        overwrites = {
            ctx.guild.default_role : nextcord.PermissionOverwrite(connect = False),
            ctx.guild.me : nextcord.PermissionOverwrite(connect = True)
        }
        categs.append(categ.id)
        await categ.create_voice_channel(f"MEMBER COUNT - {str(ctx.guild.member_count)}", overwrites=overwrites)
        await ctx.send(f"Successfully set up server stats.")



def setup(bot):
    bot.add_cog(Moderation(bot))