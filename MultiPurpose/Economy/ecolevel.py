import nextcord
from nextcord.ext import commands
import aiosqlite
import math
import random
import asyncio
import io
from PIL import Image, ImageDraw, ImageFont


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

    async def make_rank_image(self, member: nextcord.Member, rank, level, xp, final_xp):

        if member.avatar is None:
            avatar = member.default_avatar.replace(format='png', size=512)
            avatar_bytes = io.BytesIO(await avatar.read())
        
        else:
            avatar = member.avatar.replace(format='png', size=512)
            avatar_bytes = io.BytesIO(await avatar.read())

        img = Image.new('RGB', (1000, 240))
        logo = Image.open(avatar_bytes).resize((200, 200))

        # Stack overflow helps :)
        bigsize = (logo.size[0] * 3, logo.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(logo.size, Image.ANTIALIAS)
        logo.putalpha(mask)
        ##############################
        img.paste(logo, (20, 20), mask=logo)

        # Black Circle
        draw = ImageDraw.Draw(img, 'RGB')
        draw.ellipse((152, 152, 208, 208), fill='#000')

        # Placing offline or Online Status
        # nextcord Colors (Online: '#43B581')
        draw.ellipse((155, 155, 205, 205), fill='#43B581')
        ##################################

        # Working with fonts
        big_font = ImageFont.FreeTypeFont('D:\\MultiPurpose-Nextcord\\ABeeZee-Regular-Font.otf', 60)
        medium_font = ImageFont.FreeTypeFont('D:\\MultiPurpose-Nextcord\\ABeeZee-Regular-Font.otf', 40)
        small_font = ImageFont.FreeTypeFont('D:\\MultiPurpose-Nextcord\\ABeeZee-Regular-Font.otf', 30)

        # Placing Level text (right-upper part)
        text_size = draw.textsize(f"{level}", font=big_font)
        offset_x = 1000-15 - text_size[0]
        offset_y = 5 
        draw.text((offset_x, offset_y), f"{level}", font=big_font, fill="#11ebf2")
        text_size = draw.textsize('LEVEL', font=small_font)

        offset_x -= 5 + text_size[0]
        offset_y = 35
        draw.text((offset_x, offset_y), "LEVEL", font=small_font, fill="#11ebf2")

        # Placing Rank Text (right upper part)
        text_size = draw.textsize(f"#{rank}", font=big_font)
        offset_x -= 15 + text_size[0]
        offset_y = 8
        draw.text((offset_x, offset_y), f"#{rank}", font=big_font, fill="#fff")

        text_size = draw.textsize("RANK", font=small_font)
        offset_x -= 5 + text_size[0]
        offset_y = 35
        draw.text((offset_x, offset_y), "RANK", font=small_font, fill="#fff")

        # Placing Progress Bar
        # Background Bar
        bar_offset_x = logo.size[0] + 20 + 100
        bar_offset_y = 160
        bar_offset_x_1 = 1000 - 50
        bar_offset_y_1 = 200
        circle_size = bar_offset_y_1 - bar_offset_y

        # Progress bar rect greyier one
        draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175")
        # Placing circle in progress bar

        # Left circle
        draw.ellipse((bar_offset_x - circle_size//2, bar_offset_y, bar_offset_x + circle_size//2, bar_offset_y + circle_size), fill="#727175")

        # Right Circle
        draw.ellipse((bar_offset_x_1 - circle_size//2, bar_offset_y, bar_offset_x_1 + circle_size//2, bar_offset_y_1), fill="#727175")

        # Filling Progress Bar

        bar_length = bar_offset_x_1 - bar_offset_x
        # Calculating of length
        # Bar Percentage (final_xp - current_xp)/final_xp

        # Some variables
        progress = (final_xp - xp) * 100/final_xp
        progress = 100 - progress
        progress_bar_length = round(bar_length * progress/100)
        pbar_offset_x_1 = bar_offset_x + progress_bar_length

        # Drawing Rectangle
        draw.rectangle((bar_offset_x, bar_offset_y, pbar_offset_x_1, bar_offset_y_1), fill="#11ebf2")
        # Left circle
        draw.ellipse((bar_offset_x - circle_size//2, bar_offset_y, bar_offset_x + circle_size//2, bar_offset_y + circle_size), fill="#11ebf2")
        # Right Circle
        draw.ellipse((pbar_offset_x_1 - circle_size//2, bar_offset_y, pbar_offset_x_1 + circle_size//2, bar_offset_y_1), fill="#11ebf2")


        def convert_int(integer):
            integer = round(integer / 1000, 2)
            return f'{integer}K'

        # Drawing Xp Text
        text = f"/ {convert_int(final_xp)} XP"
        xp_text_size = draw.textsize(text, font=small_font)
        xp_offset_x = bar_offset_x_1 - xp_text_size[0]
        xp_offset_y = bar_offset_y - xp_text_size[1] - 10
        draw.text((xp_offset_x, xp_offset_y), text, font=small_font, fill="#727175")

        text = f'{convert_int(xp)} '
        xp_text_size = draw.textsize(text, font=small_font)
        xp_offset_x -= xp_text_size[0]
        draw.text((xp_offset_x, xp_offset_y), text, font=small_font, fill="#fff")

        # Placing User Name
        text = member.display_name
        text_size = draw.textsize(text, font=medium_font)
        text_offset_x = bar_offset_x - 10
        text_offset_y = bar_offset_y - text_size[1] - 10
        draw.text((text_offset_x, text_offset_y), text, font=medium_font, fill="#fff")

        # Placing Discriminator
        text = f'#{member.discriminator}'
        text_offset_x += text_size[0] + 10
        text_size = draw.textsize(text, font=small_font)
        text_offset_y = bar_offset_y - text_size[1] - 10
        draw.text((text_offset_x, text_offset_y), text, font=small_font, fill="#727175")

        bytes = io.BytesIO()
        img.save(bytes, 'PNG')
        bytes.seek(0)
        return bytes
        
    

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
        bytes = await self.make_rank_image(member, rank, level, xp, final_xp)
        file = nextcord.File(bytes, 'rank.png')
        await ctx.send(file=file)


    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx):
        cursor = await self.db.cursor()
        await cursor.execute("SELECT level, xp, user_id FROM users ORDER BY xp DESC , level DESC")
        leaderboard = await cursor.fetchall()
        pages = []
        page_count = -(-len(leaderboard)//10) #will return 3 if users' length is 23
        for i in range(page_count):
            embed = nextcord.Embed(
                title = f"Rank Leaderboard | {ctx.guild.name}",
                colour = 0x003399
            )
            embed.set_footer(
                text = f"Page {i + 1}/{page_count}"
            )
            for rank, data in enumerate(leaderboard[i * 10:i * 10 + 10], start=i * 10 + 1):
                level = data[0]
                xp = data[1]
                user_id = (data[2])
                
                embed.add_field(
                name = f"#{rank} ",
                value = f"User: <@!{user_id}>\nLevel: {level}\nExperience: {xp}",
                inline = False)
            pages.append(embed)

        index = 0
        message = await ctx.send(embed=pages[0])
        emojis = ["◀️", "⏹️", "▶️"]
        for emoji in emojis:
            await message.add_reaction(emoji)
        while not self.client.is_closed():
            try:
                react, user = await self.client.wait_for(
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
def setup(bot):
    bot.add_cog(Levelling(bot))