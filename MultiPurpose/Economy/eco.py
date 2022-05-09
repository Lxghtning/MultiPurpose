import nextcord 
from nextcord.ext import commands, menus
import aiosqlite
import asyncio
from nextcord import Embed
import datetime
import numpy 
from games import hangman, twenty, minesweeper, tictactoe, wumpus
import random
from Views.confirm import Confirm
from Views.Battle import Battle

words = ['conversation', 'bowtie', 'skateboard', 'penguin', 'hospital', 'player', 'kangaroo', 
		'garbage', 'whisper', 'achievement', 'flamingo', 'calculator', 'offense', 'spring', 
		'performance', 'sunburn', 'reverse', 'round', 'horse', 'nightmare', 'popcorn', 
		'hockey', 'exercise', 'programming', 'platypus', 'blading', 'music', 'opponent', 
		'electricity', 'telephone', 'scissors', 'pressure', 'monkey', 'coconut', 'backbone', 
		'rainbow', 'frequency', 'factory', 'cholesterol', 'lighthouse', 'president', 'palace', 
		'excellent', 'telescope', 'python', 'government', 'pineapple', 'volcano', 'alcohol', 
		'mailman', 'nature', 'dashboard', 'science', 'computer', 'circus', 'earthquake', 'bathroom', 
		'toast', 'football', 'cowboy', 'mattress', 'translate', 'entertainment', 'glasses', 
		'download', 'water', 'violence', 'whistle', 'alligator', 'independence', 'pizza', 
		'permission', 'board', 'pirate', 'battery', 'outside', 'condition', 'shallow', 'baseball', 
		'lightsaber', 'dentist', 'pinwheel', 'snowflake', 'stomach', 'reference', 'password', 'strength', 
		'mushroom', 'student', 'mathematics', 'instruction', 'newspaper', 'gingerbread', 
		'emergency', 'lawnmower', 'industry', 'evidence', 'dominoes', 'lightbulb', 'stingray', 
		'background', 'atmosphere', 'treasure', 'mosquito', 'popsicle', 'aircraft', 'photograph', 
		'imagination', 'landscape', 'digital', 'pepper', 'roller', 'bicycle', 'toothbrush', 'newsletter']  

images =   ['```\n   +---+\n   O   | \n  /|\\  | \n  / \\  | \n      ===```',   
			'```\n   +---+ \n   O   | \n  /|\\  | \n  /    | \n      ===```', 
			'```\n   +---+ \n   O   | \n  /|\\  | \n       | \n      ===```', 
			'```\n   +---+ \n   O   | \n  /|   | \n       | \n      ===```', 
			'```\n   +---+ \n   O   | \n   |   | \n       | \n      ===```', 
			'```\n   +---+ \n   O   | \n       | \n       | \n      ===```', 
			'```\n  +---+ \n      | \n      | \n      | \n     ===```']


class ShopList(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=5)


    async def format_page(self, menu, entries):
        embed = Embed(title="List of jobs available",colour=0xFF0000)
        for entry in entries:
            embed.add_field(name=entry[0], value=entry[1], inline=False)

        embed.set_footer(text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
        return embed

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.db = None
        self.bot.loop.create_task(self.connect_database())

    async def connect_database(self):
        self.db = await aiosqlite.connect('economy.db')

    COLOUR = 0xFF0000
    async def find_user(self, member):
        cursor = await self.db.cursor()
        await cursor.execute("SELECT * FROM users WHERE user_id =?",(member.id,))
        user = await cursor.fetchone()
        return user

    async def open_account(self, member, power):
        cursor = await self.db.cursor()
        await cursor.execute("INSERT INTO users (bal, user_id, power) VALUES(?,?,power)",(100,member.id,power))
        await self.db.commit()

    async def get_bank_data(self, member):
        cursor = await self.db.cursor()
        await cursor.execute('SELECT bank FROM users WHERE user_id=?',(member.id,))
        bank = await cursor.fetchone()
        return bank

    async def get_wallet_data(self, member):
        cursor = await self.db.cursor()
        await cursor.execute('SELECT bal FROM users WHERE user_id=?',(member.id,))
        bal = await cursor.fetchone()
        return bal 
    
    async def get_power(self, member):
        cursor = await self.db.cursor()
        await cursor.execute('SELECT power FROM users WHERE user_id=?',(member.id,))
        power = await cursor.fetchone()
        return power[0]

    @commands.command(aliases=["wallet","wal","balance"])
    async def bal(self, ctx, member:nextcord.Member=None):
        "Shows your or another members wallet balance"
        if member is None: 
            member = ctx.author
        
        user = await self.find_user(member)
        if user:
            bal = await self.get_wallet_data(member)
            bank = await self.get_bank_data(member)
            emb = Embed(title=f"Balance of {member.name}#{member.discriminator}",description=f"***Showing the balance of*** __*{member.name}#{member.discriminator}*__",color=self.COLOUR)
            emb.set_thumbnail(url=member.display_avatar.url)
            emb.add_field(name="Wallet Balance",value=bal[0])
            emb.add_field(name="Bank Balance",value=bank[0])
            await ctx.send(embed=emb)
        else:
            return await ctx.send(f"It seems that the member or you are new to this system :thinking: , use the __**?start**__ command to start your journey.")

    @commands.command()
    async def start(self, ctx):
        "Introduction to the game"
        user = await self.find_user(ctx.author)
        if user == None:
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            
            embed = Embed(title="Choose your power",description=f"{ctx.author.mention} Choose your power!!\n\n1. **Fire** <a:firepower:938321177821208647> - Fire Power..Estinguish your opponent's power with the thirst of your fire power\n\n2. **Water** <a:water:938320294756642836> - Clash powers and take over the world with floods of your water power.\n\n3. **Lightning** <a:lightning:938320294303633418> - Shock everyone with electricity of lightning!\n\n4. **Teleport** <a:teleport:938320293745815564> - Teleport and avoid all the attacks of other powers...!")
            embed.set_thumbnail(url=ctx.author.display_avatar.url)
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text=f"Enter the power number you wanna choose..You can not later change power's")
            await ctx.send(embed=embed)
            try:
                msg = await self.bot.wait_for('message',check=check,timeout=60)
            except asyncio.TimeoutError:
                return await ctx.send(f"{ctx.author.mention} your start process has timed out!")
            if msg.content == "1":
                await self.open_account(ctx.author, "fire")
            elif msg.content == "2":
                await self.open_account(ctx.author, "water")
            elif msg.content == "3":
                await self.open_account(ctx.author, "lightning")
            elif msg.content == "4":
                await self.open_account(ctx.author, "teleport")
            else:
                return await ctx.send(f"{ctx.author.mention} Incorrect Input provided.")
            emb = Embed(title=f"Starting {ctx.author.name}#{ctx.author.discriminator}'s journey", description=f"__***{ctx.author.name}#{ctx.author.discriminator}***__ **Welcome to the world of money.**\n\n*Here you can buy, sell, trade, rob, bankrob etc. different types of people**\n\n**You have been rewarded with** __*100 INR <a:ind:935452295594934312> money*__ **to start your journey with so spend wisely!**\n",color=self.COLOUR)
            emb.set_thumbnail(url=ctx.author.display_avatar.url)
            emb.set_image(url="https://bestanimations.com/media/india/341407292india-flag-waving-animated-gif-4.gif")
            await ctx.send(embed=emb)
        else:
            return await ctx.send(f"{ctx.author.mention} you have already begun your journey!")

    @commands.command()
    async def crime(self, ctx, member:nextcord.Member):
        "Perform a crime/rob a member"
        user = self.find_user(member)
        cursor = await self.db.cursor()
        if user:
            choice = random.choices(["yes","no"])
            if choice[0] == "yes":
                author = await self.get_wallet_data(ctx.author)
                member = await self.get_wallet_data(member)
                if int(author[0]) > 10000:
                    if int(member[0]) > 5000:
                        amount = random.choices([i for i in range(1,int(member[0]))])
                        await cursor.execute("UPDATE users SET bal = bal + ? WHERE user_id = ?",(int(amount[0]), ctx.author.id))
                        await cursor.execute("UPDATE users SET bal = bal - ? WHERE user_id = ?",(int(amount[0]), member.id))
                        await self.db.commit()
                        emb = Embed(description=f" Good Job __*{member.name}#{member.discriminator}*__ You ripped of {int(amount[0])} INR <a:ind:935452295594934312> from that guy.",color=self.COLOUR)
                        emb.set_thumbnail(url=member.display_avatar.url)
                        await ctx.send(embed=emb)
                    else: 
                        return await ctx.send(f"{ctx.author.mention} Breh the member (**{member.name}#{member.discriminator}**) is not even worth 5000 <a:ind:935452295594934312>, Lets leave that guy alone!")
                else:
                    return await ctx.send(f"{ctx.author.mention} You really wasted my time....Be worth 10k INR <a:ind:935452295594934312> with the necessary supplies needed to be able to rob someone!")
            else:
                author = await self.get_wallet_data(ctx.author)
                member = await self.get_wallet_data(member)
                if int(author[0]) > 10000:
                    if int(member[0]) > 5000:
                        amount = random.choices([i for i in range(1,int(member[0]))])
                        await cursor.execute("UPDATE users SET bal = bal - ? WHERE user_id = ?",(int(amount[0]), ctx.author.id))
                        await cursor.execute("UPDATE users SET bal = bal + ? WHERE user_id = ?",(int(amount[0]), member.id))
                        await self.db.commit()
                        emb = Embed(description=f"__*{member.name}#{member.discriminator}*__ Damn..You were caught and you paid a total fine of {int(amount[0])} INR <a:ind:935452295594934312> ",color=self.COLOUR)
                        emb.set_thumbnail(url=member.display_avatar.url)
                        await ctx.send(embed=emb)
                    else: 
                        return await ctx.send(f"{ctx.author.mention} Breh the member (**{member.name}#{member.discriminator}**) is not even worth 5000 <a:ind:935452295594934312>, Lets leave that guy alone!")
                else:
                    return await ctx.send(f"{ctx.author.mention} You really wasted my time....Be worth 10k INR <a:ind:935452295594934312> with the necessary supplies neededto be able to rob someone!")

        else:
            return await ctx.send(f"It seems that the member or you are new to this system :thinking: , use the __**?start**__ command to start your journey.")

    @commands.command(aliases=["dep"])
    async def deposit(self,ctx,amount:int):
        user=await self.find_user(ctx.author)
        if user:
            cursor = await self.db.cursor()
            bank = await self.get_wallet_data(ctx.author)
            if bank[0] >= amount:
                await cursor.execute("UPDATE users SET bal = bal - ?, bank = bank + ? WHERE user_id = ?",(amount,ctx.author.id,))
                await self.db.commit()
                e = Embed(description=f"{ctx.author.mention} you deposited {amount} to your bank.",color = self.COLOUR)
                await ctx.send(embed=e)
            else:
                return await ctx.send(f"{ctx.author.mention} Damn Bro, Kids like you..OOF! Don't you have common sense that you cannot deposit more than what you have in your wallet? ")
        else:
            return await ctx.send(f"It seems that you are new to this system :thinking: , use the __**?start**__ command to start your journey.")


    @commands.command(aliases=["with"])
    async def withdraw(self,ctx,amount:int):
        user=await self.find_user(ctx.author)
        if user:
            cursor = await self.db.cursor()
            bank = await self.get_bank_data(ctx.author)
            if bank[0] >= amount:
                await cursor.execute("UPDATE users SET bal = bal + ?, bank = bank - ? WHERE user_id = ?",(amount,ctx.author.id,))
                await self.db.commit()
                e = Embed(description=f"{ctx.author.mention} you withdrew {amount} from your bank.",color = self.COLOUR)
                await ctx.send(embed=e)
            else:
                return await ctx.send(f"{ctx.author.mention} Dude use your common sense...You can not withdraw more than what you have? DUH!")
        else:
            return await ctx.send(f"It seems that you are new to this system :thinking: , use the __**?start**__ command to start your journey.")


    @commands.command()
    async def boss(self, ctx):
        user = await self.find_user(ctx.author)
        cursor = await self.db.cursor()
        if user:
            await cursor.execute("SELECT level FROM userlevel WHERE user_id=?",(ctx.author.id,))
            level = await cursor.fetchone()
        
            await cursor.execute("SELECT user_id FROM hp WHERE user_id = ?",(ctx.author.id,))
            user = await cursor.fetchone()
            if user==None:
                userhp = 100      
                bosshp = 100
                await cursor.execute("INSERT INTO hp (user_id,boss_hp,user_hp) VALUES (?,?,?)",(ctx.author.id,userhp,bosshp))
                await self.db.commit()
                embed = Embed(title="Boss Fight",description=f"\n```Boss fight```\n\n",color=self.COLOUR)
                embed.set_thumbnail(url=ctx.author.display_avatar.url)
                embed.add_field(name=f"{ctx.author.name}#{ctx.author.discriminator}",value=f"{userhp}")
                embed.add_field(name=f"Naruto Boss",value=f"{bosshp}")
                await ctx.send(embed=embed,view=Battle(self.db))
            else:
                return await ctx.send(f"{ctx.author.mention} you already have a boss match in progress")
        else:
            return await ctx.send(f"It seems that you are new to this system :thinking: , use the __**?start**__ command to start your journey.")

    @commands.command()
    async def bankrob(self,ctx, member:nextcord.Member):
        user = await self.find_user(ctx.author)
        if user:
            cursor = await self.db.cursor()
            membank = await self.get_bank_data(ctx.author)
            bal = await self.get_wallet_balance(ctx.author)
        else:
            return await ctx.send(f"It seems that the member or you are new to this system :thinking: , use the __**?start**__ command to start your journey.")
    
    @commands.command(name="path-1")
    async def path1(self, ctx):
        user = await self.find_user(ctx.author)
        if user:
            power = await self.get_power(ctx.author)
            cursor = await self.db.cursor()
            await cursor.execute("SELECT user_id FROM hp WHERE user_id = ?",(ctx.author.id,))
            user = await cursor.fetchone()
            if user==None:
                userhp = 100      
                bosshp = 100
                await cursor.execute("INSERT INTO hp (user_id,boss_hp,user_hp) VALUES (?,?,?)",(ctx.author.id,userhp,bosshp))
                await self.db.commit()
                embed = Embed(title="Soldier",description=f"\n```Fight against Lynx```\n\n",color=self.COLOUR)
                embed.set_thumbnail(url=ctx.author.display_avatar.url)
                embed.add_field(name=f"{ctx.author.name}#{ctx.author.discriminator}",value=f"{userhp}")
                embed.add_field(name=f"Lynx Soldier",value=f"{bosshp}")
                await ctx.send(embed=embed,view=Battle(self.db))
            else:
                return await ctx.send(f"{ctx.author.mention} you already have a boss match in progress")
        else:
            return await ctx.send(f"It seems that the member or you are new to this system :thinking: , use the __**?start**__ command to start your journey.")  


            

def setup(bot):
    bot.add_cog(economy(bot))