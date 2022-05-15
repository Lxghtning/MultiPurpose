import nextcord
from nextcord.ext import commands
import aiosqlite
from nextcord import Embed
import humanfriendly
from datetime import datetime 

class Automoderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = None
        self.bot.loop.create_task(self.db_connect())

    async def db_connect(self):
        await self.bot.wait_until_ready()
        self.db = await aiosqlite.connect("D:\\MultiPurpose-Nextcord\\Moderation\\warn_database.db")
    

    async def get_user(self, user_id):
        cursor = await self.db.cursor()
        await cursor.execute("SELECT * FROM counts WHERE user_id = ?",(user_id,))
        res = await cursor.fetchone()
        if res:
            return res
        else:
            return "no"

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):

        cursor = await self.db.cursor()
        if message.author.guild.permissions.administrator != True:
            user = await self.get_user(message.author.id)
            if (len([l for l in message.content if l.isupper()])) >= 5:
                await message.delete()
                if user == "no":
                    await cursor.execute("INSERT INTO counts(user_id, count) VALUES(?,?)",(message.author.id, 1))
                    await self.db.commit()
                else:
                    await cursor.execute("UPDATE counts SET count = count + 1 WHERE user_id = ?",(message.author.id,))
                    await self.db.commit()
                
                if user[1] >= 5 and user[1] <= 9:
                    try:
                        time = humanfriendly.parse_timespan()
                        await message.author.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time))
                        await message.channel.send(f'{message.author.mention} was muted for 10 mins as your automod count is {user[1]} and you have violated a rule..')
                        try:
                            await message.author.send(f"You were muted in {message.guild.name} for 10 mins as your automod count is {user[1]} and you have violated a rule.")
                        except:
                            pass
                    except:
                        await message.channel.send("Automod Error:- Member already muted.")
                embed=Embed(description=f"{message.author.mention} **There were too many capital letters in your sentence/message({(len([l for l in message.content if l.isupper()]))}).**\n\n**Increased the warn counter by 1.**\n\n**Note:- 5 warns count results in a mute,**\n**10 in a kick**\n**20 in a ban.**")
                embed.set_author(name=message.author, icon_url = message.author.display_avatar.url)
                embed.set_thumbnail(url=message.guild.icon.url)
                await message.channel.send(embed=embed)
        else:
            pass


def setup(bot):
    bot.add_cog(Automoderation(bot))