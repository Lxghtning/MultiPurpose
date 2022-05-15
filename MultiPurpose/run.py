from asyncio import tasks
import nextcord
from nextcord.ext import commands, menus, tasks
import aiosqlite
import random
import asyncio
import numpy as np
import json
import re
import requests
from Views.ticket import Close, Ticket_View
from nextcord import Embed
from datetime import datetime
from Views.staff_view import staffView
from PIL import Image, ImageDraw, ImageFont
import io


categs = []

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(staffView())
            self.add_view(Ticket_View())
            self.add_view(Close())

            self.persistent_views_added = True

        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        checkforvideos.start()



bot=Bot(command_prefix=commands.when_mentioned_or('!'), intents=nextcord.Intents.all())
bot.remove_command('help')
# bot.load_extension('Views.help')
bot.load_extension('Help_command.help_cmd')
bot.load_extension('Moderation.ModerationCmds')
bot.load_extension('Tourney Manager.tourneytext')
bot.load_extension('Economy.ecodefault')
bot.load_extension('Economy.ecolevel')
# bot.load_extension('Level_Up_System.level')
# bot.load_extension('Crosschat.crosschat')
# bot.load_extension('Music.musicdefault')
# bot.load_extension('StaffApps.staff_apply')
bot.load_extension('Music.musc')
bot.load_extension("Misc.misc")
bot.load_extension('Slash_Commands.slashcmds')
bot.load_extension('Errors.error_handler')
bot.load_extension('Moderation.modmail')
bot.load_extension('jishaku')
bot.load_extension('Misc.meme')
# bot.load_extension('Moderation.Automod')

def convert(time):
  pos = ["s","m","h","d"]

  time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}

  unit = time[-1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2

  return val * time_dict[unit]

async def setup():
    await bot.wait_until_ready()
    bot.dab = await aiosqlite.connect("inviteData.db")
    await bot.dab.execute("CREATE TABLE IF NOT EXISTS totals (guild_id int, inviter_id int, normal int, left int, fake int, PRIMARY KEY (guild_id, inviter_id))")
    await bot.dab.execute("CREATE TABLE IF NOT EXISTS invites (guild_id int, id string, uses int, PRIMARY KEY (guild_id, id))")
    await bot.dab.execute("CREATE TABLE IF NOT EXISTS joined (guild_id int, inviter_id int, joiner_id int, PRIMARY KEY (guild_id, inviter_id, joiner_id))")
    
    # fill invites if not there
    for guild in bot.guilds:
        for invite in await guild.invites(): # invites before bot was added won't be recorded, invitemanager/tracker don't do this
            await bot.dab.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses) VALUES (?,?,?)", (invite.guild.id, invite.id, invite.uses))
            await bot.dab.execute("INSERT OR IGNORE INTO totals (guild_id, inviter_id, normal, left, fake) VALUES (?,?,?,?,?)", (guild.id, invite.inviter.id, 0, 0, 0))
                                 
    await bot.dab.commit()

async def update_totals(member):
    invites = await member.guild.invites()

    c = datetime.today().strftime("%Y-%m-%d").split("-")
    c_y = int(c[0])
    c_m = int(c[1])
    c_d = int(c[2])

    async with bot.dab.execute("SELECT id, uses FROM invites WHERE guild_id = ?", (member.guild.id,)) as cursor: # this gets the old invite counts
        async for invite_id, old_uses in cursor:
            for invite in invites:
                if invite.id == invite_id and invite.uses - old_uses > 0: # the count has been updated, invite is the invite that member joined by
                    if not (c_y == member.created_at.year and c_m == member.created_at.month and c_d - member.created_at.day < 7): # year can only be less or equal, month can only be less or equal, then check days
                        print(invite.id)
                        await bot.dab.execute("UPDATE invites SET uses = uses + 1 WHERE guild_id = ? AND id = ?", (invite.guild.id, invite.id))
                        await bot.dab.execute("INSERT OR IGNORE INTO joined (guild_id, inviter_id, joiner_id) VALUES (?,?,?)", (invite.guild.id, invite.inviter.id, member.id))
                        await bot.dab.execute("UPDATE totals SET normal = normal + 1 WHERE guild_id = ? AND inviter_id = ?", (invite.guild.id, invite.inviter.id))

                    else:
                        await bot.dab.execute("UPDATE totals SET normal = normal + 1, fake = fake + 1 WHERE guild_id = ? and inviter_id = ?", (invite.guild.id, invite.inviter.id))

                    return
    


@bot.event
async def on_member_join(member):
    bytes = await create_welcome_card(member)
    file = nextcord.File(bytes, 'welcome.png')
    await update_totals(member)
    await bot.dab.commit()
    try:
        categ = nextcord.utils.get(member.guild.categories, id=categs[len(categs) - 1])
        chan = categ.channels
        for channels in chan:
            await channels.delete()
        overwrites = {
            member.guild.default_role : nextcord.PermissionOverwrite(connect = False),
            member.guild.me : nextcord.PermissionOverwrite(connect = True)
        }
        await categ.create_voice_channel(f"MEMBER COUNT - {str(member.guild.member_count)}--", overwrites=overwrites)
    except IndexError:
        pass
    channel = nextcord.utils.get(member.guild.channels, id=759490894968913972)
    cur = await bot.dab.execute("SELECT inviter_id FROM joined WHERE guild_id = ? and joiner_id = ?", (member.guild.id, member.id))
    res = await cur.fetchone()
    if res is None:
        inviter = "Unknown"
    else:
        inviter = f"<@{res[0]}>"
    await channel.send(file=file)

async def create_welcome_card(member):

    if member.avatar is None:
        avatar = member.default_avatar.replace(format='png', size=512)
        avatar_bytes = io.BytesIO(await avatar.read())
        
    else:
        avatar = member.avatar.replace(format='png', size=512)
        avatar_bytes = io.BytesIO(await avatar.read())

    

    welc = "WELCOME"
    user_name = member.name
    discriminator = f"#{member.discriminator}"

    background = Image.open("D:\\MultiPurpose-Nextcord\WELCOME.png")
    logo = Image.open(avatar_bytes).resize((200, 200)).convert("RGBA")

    bigsize = (logo.size[0] * 3, logo.size[1] * 3)
    mask = Image.new("L", bigsize, 0)


    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, 255)



    mask = mask.resize(logo.size, Image.ANTIALIAS)
    logo.putalpha(mask)

    background.paste(logo, (420, 80), mask=logo)


    draw = ImageDraw.Draw(background)

    welco = ImageFont.FreeTypeFont("D:\\Oswald-SemiBold.ttf", 90)
    big_font = ImageFont.FreeTypeFont("D:\\Oswald-SemiBold.ttf", 90)
    medium_font = ImageFont.truetype("D:\\Oswald-SemiBold.ttf", 50)
    small_font = ImageFont.FreeTypeFont("D:\\Oswald-SemiBold.ttf", 40)

    


    text_size = draw.textsize(user_name, font=medium_font)
    offset_x = 620 - text_size[0]
    offset_y = 380
    draw.text((offset_x, offset_y), user_name, font=medium_font, fill="#FFFFFF")

    offset_x += text_size[0] + 5
    offset_y += 30
    draw.text((offset_x, offset_y), discriminator, font=small_font, fill="#FFFFFF")

    text_size = draw.textsize(welc, font=welco)
    offset_x = 720 - 15 - text_size[0]
    offset_y = 280
    draw.text((offset_x, offset_y), welc, font=welco, fill="#FFFFFF")

    bytes = io.BytesIO()
    background.save(bytes, 'PNG')
    bytes.seek(0)
    return bytes

        
@bot.event
async def on_member_remove(member):


    cur = await bot.dab.execute("SELECT inviter_id FROM joined WHERE guild_id = ? and joiner_id = ?", (member.guild.id, member.id))
    res = await cur.fetchone()
    if res is None:
        return 
    categ = nextcord.utils.get(member.guild.categories, id=categs[len(categs) - 1])
    chan = categ.channels
    for channels in chan:
        await channels.delete()
    overwrites = {
        member.guild.default_role : nextcord.PermissionOverwrite(connect = False),
        member.guild.me : nextcord.PermissionOverwrite(connect = True)
	}
    await categ.create_voice_channel(f"MEMBER COUNT - {str(member.guild.member_count)}", overwrites=overwrites)

    inviter = res[0]
    
    await bot.dab.execute("DELETE FROM joined WHERE guild_id = ? AND joiner_id = ?", (member.guild.id, member.id))
    await bot.dab.execute("DELETE FROM totals WHERE guild_id = ? AND inviter_id = ?", (member.guild.id, member.id))
    await bot.dab.execute("UPDATE totals SET left = left + 1 WHERE guild_id = ? AND inviter_id = ?", (member.guild.id, inviter))
    await bot.dab.commit()

@bot.event
async def on_invite_create(invite):
    await bot.dab.execute("INSERT OR IGNORE INTO totals (guild_id, inviter_id, normal, left, fake) VALUES (?,?,?,?,?)", (invite.guild.id, invite.inviter.id, invite.uses, 0, 0))
    await bot.dab.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses) VALUES (?,?,?)", (invite.guild.id, invite.id, invite.uses))
    await bot.dab.commit()
    
@bot.event
async def on_invite_delete(invite):
    await bot.dab.execute("DELETE FROM invites WHERE guild_id = ? AND id = ?", (invite.guild.id, invite.id))
    await bot.dab.commit()

@bot.event
async def on_guild_join(guild): # add new invites to monitor
    for invite in await guild.invites():
        await bot.dab.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses) VAlUES (?,?,?)", (guild.id, invite.id, invite.uses))
        
    await bot.dab.commit()
    
@bot.event
async def on_guild_remove(guild): # remove all instances of the given guild_id
    await bot.dab.execute("DELETE FROM totals WHERE guild_id = ?", (guild.id,))
    await bot.dab.execute("DELETE FROM invites WHERE guild_id = ?", (guild.id,))
    await bot.dab.execute("DELETE FROM joined WHERE guild_id = ?", (guild.id,))

    await bot.dab.commit()

@bot.command()
async def invites(ctx, member: nextcord.Member=None):
    if member is None: member = ctx.author

    # get counts
    cur = await bot.dab.execute("SELECT normal, left, fake FROM totals WHERE guild_id = ? AND inviter_id = ?", (ctx.guild.id, member.id))
    res = await cur.fetchone()
    if res is None:
        normal, left, fake = 0, 0, 0

    else:
        normal, left, fake = res

    total = normal - (left + fake)
    
    em = nextcord.Embed(
        title=f"Invites for {member.name}#{member.discriminator}",
        colour=nextcord.Colour.orange())
    em.add_field(
        name="Total",
        value=total,
        inline=False
    )
    em.add_field(
        name="Normal",
        value=normal,
        inline=True
    )
    em.add_field(
        name="Left",
        value=left,
        inline=True
    )
    em.add_field(
        name="Fake",
        value=fake,
        inline=False
    )

    await ctx.send(embed=em)

@bot.command(name="lb-inv")
async def _lbinv(ctx):

        aa = await bot.dab.execute("SELECT normal, inviter_id FROM totals ORDER BY normal DESC")
        leaderboard = await aa.fetchall()
        print(leaderboard)
        pages = []
        page_count = -(-len(leaderboard)//10) #will return 3 if users' length is 23
        for i in range(page_count):
            embed = nextcord.Embed(
                title = f"Leaderboard | {ctx.guild.name}",
                colour = 0x003399
            )
            embed.set_footer(
                text = f"Page {i + 1}/{page_count}"
            )
            for rank, data in enumerate(leaderboard[i * 10:i * 10 + 10], start=i * 10 + 1):
                print(data)
                inv = data[0]
                inviter_id = (data[1])

                embed.add_field(
                name = f"#{rank}",
                value = f"User: <@!{inviter_id}>\n\nInvites: {inv}",
                inline = False)
            pages.append(embed)

        index = 0
        message = await ctx.send(embed=pages[0])
        emojis = ["◀️", "⏹", "▶️"]
        for emoji in emojis:
            await message.add_reaction(emoji)
        while not bot.is_closed():
                try:
                    react, user = await bot.wait_for(
                        "reaction_add",
                        timeout = 60.0,
                        check = lambda r, u: r.emoji in emojis and u.id == ctx.author.id and r.message.id == message.id
                    )
                    if react.emoji == emojis[0] and index > 0:
                        await message.remove_reaction(emoji, user)
                        index -= 1
                    elif react.emoji == emojis[2] and index < len(pages) - 1:
                        await message.remove_reaction(emoji, user)
                        index += 1
                    elif react.emoji == emojis[1]:

                        await message.clear_reactions()
                        break

                    await message.edit(embed=pages[index])
                except asyncio.TimeoutError:
                    await message.clear_reactions()
                    break

class MyEmbedDescriptionPageSource(menus.ListPageSource):
    def __init__(self, data, r):
        super().__init__(data, per_page=20)
        self.r = r

    async def format_page(self, menu, names):

        embed = Embed(title=f"Members in role {self.r.name}, {len(self.r.members)} Member Count", description="\n".join(names))

        embed.set_footer(text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
        return embed


@bot.command()
@commands.has_permissions(administrator=True)
async def inrole(ctx, r_id:int):
    print(r_id)
    g=bot.get_guild(921667897447813192)
    r = g.get_role(r_id)
    names = [f"{m.name}#{m.discriminator}" for m in r.members]

    pages = menus.ButtonMenuPages(
        source=MyEmbedDescriptionPageSource(names, r),
        disable_buttons_after=True,
    )
    await pages.start(ctx)

async def ch_pr():
    await bot.wait_until_ready()
    statuses = ["to !help", "DM to Contact Staff","Arka SMP Team Of Noobs","E-GIRLS ARE RUINING MY LIFE"]
    
    while not bot.is_closed():
        status = random.choice(statuses)
        if status == "Music":
            await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening,name=status))
        else:
            await bot.change_presence(activity=nextcord.Game(name=status))

        await asyncio.sleep(5)
bot.loop.create_task(ch_pr())

async def setupgw():
    await bot.wait_until_ready()
    bot.dtb = await aiosqlite.connect("gw.db")

class Giveaway(nextcord.ui.View):
    def __init__(self, db):
        self.db=db
        super().__init__(timeout=None)


    @nextcord.ui.button(emoji="🎉", style=nextcord.ButtonStyle.green)
    async def receive(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user = await self.db.execute("SELECT * FROM users WHERE msg_id = ? AND user_id = ?",(interaction.message.id,interaction.user.id))
        user_id = await user.fetchone()

        if user_id == None:
            await self.db.execute("INSERT INTO users (user_id, msg_id) VALUES (?,?)",(interaction.user.id, interaction.message.id))
            await self.db.commit()
            await interaction.response.send_message('You have entered the giveaway successfully!', ephemeral=True)            

        else:
            await self.db.execute("DELETE FROM users WHERE user_id = ? and msg_id = ?",(interaction.user.id, interaction.message.id))
            await self.db.commit()
            await interaction.response.send_message('Removed your entry from the giveaway!', ephemeral=True)



def convert(time):
  pos = ["s","m","h","d"]

  time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}

  unit = time[-1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2

  return val * time_dict[unit]



@bot.command(aliases=["reminder","bonk"])
async def remind(ctx, time:str,*,content:str):
    timee = convert(time)
    await ctx.send(f"Set reminder for {time} for you, Content - {content}!")
    await asyncio.sleep(timee)
    await ctx.send(f"{ctx.author.mention} BONK!! Reminder for you - {content}")

@bot.command()
@commands.has_permissions(administrator=True)
async def gstart(ctx, channel: nextcord.TextChannel):
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    try:
        await ctx.send("What would be the prize of the giveaway?")
        msg = await bot.wait_for('message', check=check, timeout=60)
        prize = msg.content
        await ctx.send("How long would the giveaway last?")
        msg = await bot.wait_for('message', check=check,timeout=60)
        timee = msg.content  
        time = convert(timee)
        if time == -1:
            await ctx.send(f"You didn't answer with a proper unit. Use (s|m|h|d) next time!")
            return
        elif time == -2:
            await ctx.send(f"The time just be an integer. Please enter an integer next time.")
            return    
        await ctx.send("Enter the time that will show in the embed.")
        msg = await bot.wait_for('message', check=check,timeout=60)
        time2 = msg.content        
        await ctx.send("Who is hosting the giveaway?")
        msg = await bot.wait_for('message', check=check,timeout=60)
        hoster = msg.content
        embed = Embed(description=f"```Giveaway Time```\n\n**Giveaway By :tada:** - *{hoster}*\n\n **Prize** - *{prize}* :trophy:\n\n**Ends at** - *{time2}* :clock1:", colour=0xf4ee52)
        msg = await channel.send(embed=embed, view=Giveaway(bot.dtb))

    except asyncio.TimeoutError:
        return await ctx.send(f"{ctx.author.mention} This process has timed out!")

    await asyncio.sleep(time)
    try:
        userfetch = await bot.dtb.execute("SELECT user_id FROM users WHERE msg_id = ?",(msg.id,))
        users = await userfetch.fetchall()
        winner = random.choices(users)

        await channel.send(f"<@{(winner[0])[0]}> has won the giveaway of {prize}!")
    except:
        pass

@bot.command()
@commands.has_permissions(administrator=True)
async def reroll(ctx, msg: int):
    try:
        userfetch = await bot.dtb.execute("SELECT user_id FROM users WHERE msg_id = ?",(msg,))
        users = await userfetch.fetchall()
    except:
        return await ctx.send("No giveaway hosted with that message ID!")
    winner = random.choices(users)
    await ctx.send(f"<@{(winner[0][0])}> has won the giveaway!")

@bot.command()
@commands.has_permissions(administrator=True)
async def gend(ctx, msg:int):
    try:
        userfetch = await bot.dtb.execute("SELECT user_id FROM users WHERE msg_id = ?",(msg,))
        users = await userfetch.fetchall()
    except:
        return await ctx.send("No giveaway hosted with that message ID!")
    winner = random.choices(users)
    await ctx.send(f"<@{(winner[0])[0]}> has won the giveaway!")

@bot.command()
@commands.has_permissions(administrator=True)
async def gdel(ctx, msg:int):
    try:
        await bot.dtb.execute("DELETE FROM users WHERE msg_id = ?",(msg,))
        await bot.dtb.commit()
 
    except:
        return await ctx.send("No giveaway hosted with that message ID.")

    await ctx.send("Deleted giveaway.")

async def make(user, game):
    invite = await user.voice.channel.create_invite(
        reason="Play game",
        unique=False,
        target_type=nextcord.InviteTarget.embedded_application,
        target_application_id=game,
    )
    return invite.url

GUILDS = [921667897447813192, 843120245908176896, 911617189595979857, 946284164020326440]


    
@bot.command()
async def fm(ctx, channel: nextcord.TextChannel=None):
    channel = channel or ctx.channel
    messages = await channel.history(oldest_first=True,limit=1).flatten()
    e = Embed(description=f"```The first message of {channel.name}```",color=0xFF0000)
    e.add_field(name="Author",value=messages[0].author,inline=False)
    e.add_field(name="Message ID",value=messages[0].id,inline=True)
    e.add_field(name="Content",value=messages[0].content,inline=False)
    e.add_field(name="Author ID",value=messages[0].author.id,inline=True)
    e.add_field(name="Message Link",value=f"[Jump](https://discord.com/channels/{ctx.guild.id}/{channel.id}/{messages[0].id})")
    e.set_thumbnail(url=ctx.guild.icon.url)
    e.timestamp = datetime.now()
    e.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=e)

@bot.command(name="estimate-prune")
async def esprune(ctx,day:int,*,role:nextcord.Role=None):
    if role == None:
        role = ctx.guild.default_role
    mem= await ctx.guild.estimate_pruned_members(days=day,roles=[role])
    await ctx.send(f"The estimated prune count is {mem} members")

@bot.command()
async def prune(ctx,day:int,*,role:nextcord.Role=None):
    if role == None:
        role = ctx.guild.default_role
    mem= await ctx.guild.estimate_pruned_members(days=day,roles=[role])
    await ctx.guild.prune_members(days=day, compute_prune_count=True, roles=[role], reason=None)
    await ctx.send(f"{mem} members were pruned.")

@bot.command(name="ping")
async def _ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")



@bot.command()
async def timer(ctx, timeInput,*, content):
    try:
        try:
            time = int(timeInput)
        except:
            convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
            time = int(timeInput[:-1]) * convertTimeList[timeInput[-1]]
        if time <= 0:
            await ctx.send("Timers don\'t go into negatives!")
            return
        if time >= 3600:
            message = await ctx.send(f"Timer: {time//3600} hours {time%3600//60} minutes {time%60} seconds")
        elif time >= 60:
            message = await ctx.send(f"Timer: {time//60} minutes {time%60} seconds")
        elif time < 60:
            message = await ctx.send(f"Timer: {time} seconds")
        while True:
            try:
                await asyncio.sleep(5)
                time -= 5
                if time >= 3600:
                    await message.edit(content=f"Timer: {time//3600} hours {time %3600//60} minutes {time%60} seconds")
                elif time >= 60:
                    await message.edit(content=f"Timer: {time//60} minutes {time%60} seconds")
                elif time < 60:
                    await message.edit(content=f"Timer: {time} seconds")
                if time <= 0:
                    await message.edit(content="Ended!")
                    await ctx.send(f"Timer has ended {content}")
                    break
            except:
                break
    except:
        await ctx.send(f"Alright, first you gotta let me know how I\'m gonna time **{timeInput}**....")

@tasks.loop(seconds=120)
async def checkforvideos():
  with open("youtubedata.json", "r") as f:
    data=json.load(f)
  
  #printing here to show
  print("Now Checking!")

  #checking for all the channels in youtubedata.json file
  for youtube_channel in data:
    print(f"Now Checking For {data[youtube_channel]['channel_name']}")
    #getting youtube channel's url
    channel = f"https://www.youtube.com/channel/{youtube_channel}"

    #getting html of the /videos page
    html = requests.get(channel+"/videos").text

    #getting the latest video's url
    #put this line in try and except block cause it can give error some time if no video is uploaded on the channel
    try:
      latest_video_url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()
    except:
      continue

    #checking if url in youtubedata.json file is not equals to latest_video_url
    if not str(data[youtube_channel]["latest_video_url"]) == latest_video_url:

      #changing the latest_video_url
      data[str(youtube_channel)]['latest_video_url'] = latest_video_url

      #dumping the data
      with open("youtubedata.json", "w") as f:
        json.dump(data, f)

      #getting the channel to send the message
      discord_channel_id = data[str(youtube_channel)]['notifying_discord_channel']
      discord_channel = bot.get_channel(int(discord_channel_id))

      #sending the msg in discord channel
      #you can mention any role like this if you want
      msg = f"@everone {data[str(youtube_channel)]['channel_name']} Just Uploaded A Video Or He is Live Go Check It Out: {latest_video_url}"
      #if you'll send the url discord will automaitacly create embed for it
      #if you don't want to send embed for it then do <{latest_video_url}>

      await discord_channel.send(msg)
      
#creating command to add more youtube accounds data in youtubedata.json file
#you can also use has_role if you don't want to allow everyone to use this command
@bot.command()
@commands.is_owner()
async def addytchannel(ctx, channel_id: str, *, channel_name: str):
  with open("youtubedata.json", "r") as f:
    data = json.load(f)
  
  data[str(channel_id)]={}
  data[str(channel_id)]["channel_name"]=channel_name
  data[str(channel_id)]["latest_video_url"]="none"

  #you can also get discord_channe id from the command 
  #but if the channel is same then you can also do directly
  data[str(channel_id)]["notifying_discord_channel"]="890293434856914964"

  with open("youtubedata.json", "w") as f:
    json.dump(data, f)

  await ctx.send("Added Your Account Data!")


@bot.command()
@commands.is_owner()
async def stop_notifying(ctx):
  checkforvideos.stop()
  await ctx.send("Stopped Notifying")

#you can also create this command to start notifying but we're gonna do so that everytime the bot goes online it will automaitacly starts notifying
@bot.command()
@commands.is_owner()
async def start_notifying(ctx):
  checkforvideos.start()
  await ctx.send("Now Notifying")

snipe_message_content = None
snipe_message_author = None
snipe_message_id = None

@bot.event
async def on_message_delete(message):

    global snipe_message_content
    global snipe_message_author
    global snipe_message_id

    snipe_message_content = message.content
    snipe_message_author = message.author.id
    snipe_message_id = message.id
    await asyncio.sleep(300)

    if message.id == snipe_message_id:
        snipe_message_author = None
        snipe_message_content = None
        snipe_message_id = None

@bot.command()
async def snipe(message):
    if snipe_message_content==None:
        await message.channel.send("There's nothing to snipe.")
    else:
        embed = nextcord.Embed(title="Latest Sniped Message",description=f"Author of the message- <@!{snipe_message_author}>\nMessage Content - {snipe_message_content}")
        embed.set_footer(text=f"Requested {message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar.url)
        await message.channel.send(embed=embed)
        return


bot.loop.create_task(setupgw())
bot.loop.create_task(setup())
bot.run('OTU4Njc5NjkzMzk2MTY0NjM4.YkQ2Cg.PwYtlYKuRqUt2nio1YBq7_ZMIsA')