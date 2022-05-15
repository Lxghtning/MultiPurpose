import nextcord
from nextcord.ext import commands
import aiosqlite
import math
import random
import aiohttp
import io
from easy_pil import *


class Levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = None
        self.bot.loop.create_task(self.connect_database())

    async def connect_database(self):
        self.db = await aiosqlite.connect('database.db')

    async def find_or_insert_user(self, member: nextcord.Member):
        # user_id, guild_id, xp, level
        cursor = await self.db.cursor()
        await cursor.execute('Select * from users where user_id = ?', (member.id,))
        result = await cursor.fetchone()
        if result is None:
            result = (member.id, member.guild.id, 0, 0)
            await cursor.execute('Insert into users values(?, ?, ?, ?)', result)
            await self.db.commit()

        return result

    def calculate_xp(self, level):
        return 100 * (level ** 2)

    def calculate_level(self, xp):
        # Sqrt => value ** 0.5
        return round(0.1 * math.sqrt(xp))


    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot is True or message.guild is None:
            return

        result = await self.find_or_insert_user(message.author)

        user_id, guild_id, xp, level = result
        xp += random.randint(1, 7)
        
        if self.calculate_level(xp) > level:
            level += 1
            # 1,000
            await message.channel.send(f"Congratulations, {message.author.mention} You are now at {level:,} level.")

        cursor = await self.db.cursor()
        await cursor.execute('Update users set xp=?, level=? where user_id=? and guild_id=?', (xp, level, user_id, guild_id))
        await self.db.commit()


        
        

    @commands.command()
    async def rank(self, ctx: commands.Context, member: nextcord.Member=None):
        member = member or ctx.author
        cursor = await self.db.cursor()
        user = await self.find_or_insert_user(member)
        user_id, guild_id, xp, level = user
        await cursor.execute("Select Count(*) from users where xp > ? and guild_id=?", (xp, guild_id))
        result = await cursor.fetchone()
        rank = result[0] + 1
        final_xp = self.calculate_xp(level + 1)
        async with ctx.typing():
            def convert_int(integer):
                integer = round(integer / 1000, 2)
                return f'{integer}K'

            background = Editor(Canvas((900,300),color="#141414"))
            profile_picture = await load_image_async(str(member.display_avatar.url))
            profile = Editor(profile_picture).resize((150,150)).circle_image()
            
            poppins = Font.poppins(size=40)
            poppins_small = Font.poppins(size=30)

            card_right_shape = [(600,0),(750,300),(900,300),(900,0)]

            background.polygon(card_right_shape,color="#FFFFFF")
            background.paste(profile,(30,30))

            background.rectangle((30,220),width=650, height=40, color="#FFFFFF")
            background.bar((30,220), max_width = 650, height=40, percentage=xp/1000,color="#282828")

            background.text((200,40), f"{member.name}#{member.discriminator}", font=poppins, color="#FFFFFF")

            background.rectangle((200,100),width=350, height=2, fill="#FFFFFF")

            background.text(
                (200,130),
                f"LEVEL - {level} | XP - {xp}/{convert_int(final_xp)}",
                font = poppins_small, color="#FFFFFF"
            )



            file=nextcord.File(fp=background.image_bytes, filename="rank_card.png")
            await ctx.send(file=file)



def setup(bot):
    bot.add_cog(Levelling(bot))