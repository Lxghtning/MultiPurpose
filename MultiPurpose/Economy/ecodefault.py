import nextcord
from nextcord.ext import commands
import aiosqlite
import random
import asyncio
import numpy as np
from nextcord import Embed


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.db=None
        self.bot.loop.create_task(self.initialize())

    async def initialize(self):
            await self.bot.wait_until_ready()
            self.bot.db = await aiosqlite.connect("D:\\new back up\\ecfornfx.db")
            cursor = await self.bot.db.cursor()

    

    async def get_bank_data(self,member):
        exa = await self.bot.db.execute("SELECT * FROM users WHERE user_id = ?",(member.id,))
        exdata = await exa.fetchone()
        return exdata

    async def get_shop_data(self,member):
        exsa = await self.bot.db.execute("SELECT * FROM shop WHERE user_id = ?",(member.id,))
        exsdata = await exsa.fetchone()
        return exsdata

    async def open_shop_account(self,member):
        ex_shop_data = await self.get_shop_data(member)
        if ex_shop_data == None:
            newusercursor = await self.bot.db.execute("INSERT INTO shop(user_id) VALUES(?)",(member.id,))
            await self.bot.db.commit()
            newusershopdata = await newusercursor.fetchone()

    async def open_account(self,member):
        exa = await self.bot.db.execute("SELECT * FROM users WHERE user_id = ?",(member.id,))
        exdata = await exa.fetchone()
        if exdata == None:
            newusercursor = await self.bot.db.execute("INSERT INTO users(bal,bank,user_id) VALUES(?,?, ?)",(500,0,member.id))
            await self.bot.db.commit()
            newuserdata = await newusercursor.fetchone()


    @commands.command(aliases=["dep"])
    async def deposit(self,ctx,*,amount:str):
        await self.open_account(ctx.author)
        data = await self.get_bank_data(ctx.author)
        if amount == "all" or amount == "max":
            amount = data[0]

        else:
            amount = int(amount)
        wallet_amount = data[1]
        wallet_amount = data[1]
        bal = data[0]
        if amount>bal:
            return await ctx.send("You dont have that much money in your account!")
        deposit_data = int(bal-amount)
        ndeposit_data = int(wallet_amount+amount)
        await self.bot.db.execute("UPDATE users SET bal = ?,bank = ? WHERE user_id=?",(deposit_data,ndeposit_data,ctx.author.id))
        await self.bot.db.commit()
        await ctx.send(f"Deposited {amount} to your bank!")

    @commands.command(aliases=["with"])
    async def withdraw(self,ctx,*,amount:str):
        await self.open_account(ctx.author)
        data = await self.get_bank_data(ctx.author)
        if amount == "all" or amount == "max":
            amount = data[1]

        else:
            amount = int(amount)

        wallet_amount = data[1]
        bal = data[0]
        if amount>wallet_amount:
            return await ctx.send("You dont have that much money in your account!")
        deposit_data = int(wallet_amount-amount)
        ndeposit_data = int(bal+amount)
        await self.bot.db.execute("UPDATE users SET bal = ?,bank = ? WHERE user_id=?",(ndeposit_data,deposit_data,ctx.author.id))
        await self.bot.db.commit()
        await ctx.send(f"Withdrew {amount} from your bank!")

    @commands.command(aliases=["bal", "balance"])
    async def wallet(self,ctx, member:nextcord.Member=None):
        if member == None:
            member = ctx.author
        await self.open_account(member)
        members = await self.get_bank_data(member)
        exa = await self.bot.db.execute("SELECT * FROM users WHERE user_id = ?",(member.id,))
        exdata = await exa.fetchone()
        bal = exdata[0]
        bank = exdata[1]
        user_id = exdata[2]
        embed = Embed(description=f"```Balance Of {member.name}#{member.discriminator}```\n\n",colour=0xFF006D)
        embed.add_field(name="\n\n`Wallet`",value=f"{bal} :coin:",inline=False)
        embed.add_field(name="\n\n`Bank`",value=f"{bank} :coin:",inline=False)
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

            
    @commands.command()
    @commands.cooldown(1,60,commands.BucketType.user)
    async def rob(self,ctx, member:nextcord.Member):
        await self.open_account(ctx.author)
        await self.open_account(member)

        passiveauthor = await self.bot.db.execute("SELECT * FROM passive WHERE user_id = ?",(ctx.author.id,))
        passivee = await self.bot.db.execute("SELECT * FROM passive WHERE user_id = ?",(member.id,))
        passiveauthordata = await passiveauthor.fetchone()
        passiveedata = await passivee.fetchone()
        if passiveauthordata:
            return await ctx.send(f"Hey {ctx.author.mention} you are in passive mode, if you wish to rob then turn that off!")
        elif passiveedata:
            return await ctx.send(f"Hey {member.name}#{member.discriminator} is in passive mode! Leave them alone!")
        else:
            a = await self.bot.db.execute("SELECT * FROM users WHERE user_id = ?",(member.id,))
            data = await a.fetchone()
            am = await self.bot.db.execute("SELECT * FROM users WHERE user_id = ?",(ctx.author.id,))
            datam = await am.fetchone()
            if data[0] < 250:
                return await ctx.send("Damn! That member is not even worth 250 :coin: lets leave him alone!")
            elif datam[0] <250:
                return await ctx.send("Damn! You must have atleast 250 :coin:! How do u wish to rob?")
            elif datam[0] < 250 and data[0] < 250:
                return await ctx.send("Damn! You and the person you wish to rob, self.both dont have atleast 250 :coin:!")
            else:

                    
                robop = ["no","yes"]
                s=random.choices(robop)
                r = s[0]

                
                if r == "no":
                    robcursor = await self.bot.db.execute("SELECT bal FROM users WHERE user_id=?",(member.id,))
                    robdata = await robcursor.fetchone()
                    robmemberbaldata = int(robdata[0])
                    robar = await self.bot.db.execute("SELECT bal FROM users WHERE user_id=?",(ctx.author.id,))
                    robauthor = await robar.fetchone()
                    robauthorbaldata = int(robauthor[0])
                    rr = [i for i in range(0,robauthorbaldata)]
                    robfinee = random.choices(rr)
                    robfine = int(robauthorbaldata - robfinee[0])
                    robloss = int(robmemberbaldata + robfinee[0])
                    await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(robfine,ctx.author.id))
                    await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(robloss,member.id))
                    await self.bot.db.commit()
                    await ctx.send(f"Haha! You got caught! You paid a total fine of {robfinee[0]} :coin:, Now you have {robfine} :coin:!")
                else:
                    robcursor = await self.bot.db.execute("SELECT bal FROM users WHERE user_id=?",(member.id,))
                    robdata = await robcursor.fetchone()
                    robmemberbaldata = int(robdata[0])
                    robar = await self.bot.db.execute("SELECT bal FROM users WHERE user_id=?",(ctx.author.id,))
                    robauthor = await robar.fetchone()
                    robauthorbaldata = int(robauthor[0])
                    rr = [i for i in range(0,robauthorbaldata)]
                    robfinee = random.choices(rr)
                    robfine = int(robauthorbaldata + robfinee[0])
                    robloss = int(robmemberbaldata - robfinee[0])
                    await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(robfine,ctx.author.id))
                    await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(robloss,member.id))
                    await self.bot.db.commit()
                    await ctx.send(f"Good Job! You looted a total of {robfinee[0]} :coin:, Now you have {robfine} :coin:!")
            
        
    @commands.command()
    @commands.cooldown(1,86400,commands.BucketType.user)
    async def passive(self,ctx):
        await self.open_account(ctx.author)
        passive = await self.bot.db.execute("SELECT * FROM passive WHERE user_id = ?",(ctx.author.id,))
        passivedata = await passive.fetchone()
        if passivedata == None:
            await self.bot.db.execute("INSERT INTO passive(user_id) VALUES(?)",(ctx.author.id,))
            await self.bot.db.commit()
            await ctx.send('Your passive setting is now True!')
        else: 
            await self.bot.db.execute("DELETE FROM passive WHERE user_id = ?",(ctx.author.id, ))
            await self.bot.db.commit()
            await ctx.send('Your passive setting is now False!')


    @commands.command()
    async def shop(self,ctx):
        await self.open_account(ctx.author)
        embed=Embed(title="Shop",description="Laptop:- 10,000 :coin:\n\nFishing Rod:- 10,000 :coin:\n\nShovel:- 7,500 :coin:\n\nHunting Rifle - 50,000 :coin:\n\nInstant Crown:- 100M :coin:",colour=0xFF006D)
        await ctx.send(embed=embed)

    def bot_owner(ctx):
        return ctx.author.id == 885006461002977280

    @commands.command(aliases=["add","addm"])
    @commands.check(bot_owner)
    async def addmoney(self,ctx,member:nextcord.Member=None,*, money: int):
        with open('moneylogs.txt','a') as f:
            f.write(f"\n{ctx.author.name}#{ctx.author.discriminator} gave {money} to {member.name}#{member.discriminator}")
            f.close()
        if member == None:
            member = ctx.author
        await self.open_account(member)
        data = await self.get_bank_data(member)
        final_money = int(data[0] + money)
        await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(final_money,member.id))
        await self.bot.db.commit()
        await ctx.send(f"Successfully added {money} :coin: to {member.name}#{member.discriminator}!")
        
    @commands.command(aliases=["rem"])
    @commands.check(bot_owner)
    async def removemoney(self,ctx,member:nextcord.Member=None,*, money: int):
        with open('moneylogs.txt','a') as f:
            f.write(f"\n{ctx.author.name}#{ctx.author.discriminator} removed {money} to {member.name}#{member.discriminator}")
            f.close()
        if member == None:
            member = ctx.author
        await self.open_account(member)
        data = await self.get_bank_data(member)
        final_money = int(data[0] - money)
        await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(final_money,member.id))
        await self.bot.db.commit()
        await ctx.send(f"Successfully remove {money} :coin: to {member.name}#{member.discriminator}!") 

    @commands.command()
    @commands.cooldown(1,900,commands.BucketType.user)
    async def beg(self,ctx):
        await self.open_account(ctx.author)
        bank_data = await self.get_bank_data(ctx.author)   
        beg_list = [i for i in range(1,200)] 
        beg_money = random.choices(beg_list)
        beg_money_data = int(bank_data[0] + beg_money[0])
        await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(beg_money_data,ctx.author.id))
        await self.bot.db.commit()
        await ctx.send(f"Hey poor begger take this {beg_money[0]} :coin:!")

    @commands.command(aliases=["notif"])
    @commands.check(bot_owner)
    async def notification(self,ctx):
        f = open('moneylogs.txt','r')
        a=(f.read())
        embed=Embed(description=f"```Notifications```\n\n{a}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)



    @commands.group(invoke_without_command=True)
    async def sell(self,ctx):
        await ctx.send("That item isn't there mate! For more info look into the items in your bag/inventory to get the list of items which you can sell")

    @sell.command(aliases=["fishrod"])
    async def fishingrod(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[3]:
            return await ctx.send(f"You dont have that many fishing rod(s) in your bag!")
        elif user_shop_data[3] >= 1:
            deploy_laptop_data = int(user_shop_data[3] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 5000) 
            await self.bot.db.execute("UPDATE shop SET fishing_rod = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} fishing rod(s) have been sold from your bag!")
        elif user_shop_data[3] == None:
            return await ctx.send(f"You dont have any fishing rod(s) in your bag!")

    @sell.command(aliases=["rifle"])
    async def gun(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[2]:
            return await ctx.send(f"You dont have that many gun(s) in your bag!")
        elif user_shop_data[2] >= 1:
            deploy_laptop_data = int(user_shop_data[2] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 25000) 
            await self.bot.db.execute("UPDATE shop SET gun = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} gun(s) have been sold from your bag!")
        elif user_shop_data[2] == None:
            return await ctx.send(f"You dont have any gun in your bag!")



    @sell.command()
    async def shovel(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[5]:
            return await ctx.send(f"You dont have that many shovel(s) in your bag!")
        elif user_shop_data[5] >= 1:
            deploy_laptop_data = int(user_shop_data[5] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 3750) 
            await self.bot.db.execute("UPDATE shop SET shovel = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} shovel(s) have been sold from your bag!")
        elif user_shop_data[5] == None:
            return await ctx.send(f"You dont have any shovel in your bag!")

    @sell.command()
    async def sheep(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[6]:
            return await ctx.send(f"You dont have that many sheep(s) in your bag!")
        elif user_shop_data[6] >= 1:
            deploy_laptop_data = int(user_shop_data[6] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 1000) 
            await self.bot.db.execute("UPDATE shop SET sheep = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} sheep(s) have been sold from your bag!")
        elif user_shop_data[6] == None:
            return await ctx.send(f"You dont have any sheep in your bag!")

    @sell.command()
    async def pig(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[7]:
            return await ctx.send(f"You dont have that many pig(s) in your bag!")
        elif user_shop_data[7] >= 1:
            deploy_laptop_data = int(user_shop_data[7] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 1000) 
            await self.bot.db.execute("UPDATE shop SET pig = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} pig(s) have been sold from your bag!")
        elif user_shop_data[7] == None:
            return await ctx.send(f"You dont have any pig(s) in your bag!")

    @sell.command()
    async def lion(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[9]:
            return await ctx.send(f"You dont have that many lion(s) in your bag!")
        elif user_shop_data[9] >= 1:
            deploy_laptop_data = int(user_shop_data[9] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 15000) 
            await self.bot.db.execute("UPDATE shop SET lion = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} lion(s) have been sold from your bag!")
        elif user_shop_data[9] == None:
            return await ctx.send(f"You dont have any lion(s) in your bag!")

    @sell.command()
    async def tiger(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[10]:
            return await ctx.send(f"You dont have that many tiger(s) in your bag!")
        elif user_shop_data[10] >= 1:
            deploy_laptop_data = int(user_shop_data[10] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 15000) 
            await self.bot.db.execute("UPDATE shop SET tiger = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} tiger(s) have been sold from your bag!")
        elif user_shop_data[10] == None:
            return await ctx.send(f"You dont have any tiger(s) in your bag!")

    @sell.command()
    async def dragon(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[11]:
            return await ctx.send(f"You dont have that many dragon(s) in your bag!")
        elif user_shop_data[11] >= 1:
            deploy_laptop_data = int(user_shop_data[11] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 100000) 
            await self.bot.db.execute("UPDATE shop SET dragon = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} dragon(s) have been sold from your bag!")
        elif user_shop_data[11] == None:
            return await ctx.send(f"You dont have any dragon(s) in your bag!")

    @sell.command()
    async def fish(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[12]:
            return await ctx.send(f"You dont have that many fish in your bag!")
        elif user_shop_data[12] >= 1:
            deploy_laptop_data = int(user_shop_data[12] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 1000) 
            await self.bot.db.execute("UPDATE shop SET fish = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} fish have been sold from your bag!")
        elif user_shop_data[12] == None:
            return await ctx.send(f"You dont have any fish in your bag!")

    @sell.command()
    async def fossil(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[20]:
            return await ctx.send(f"You dont have that many fossil(s) in your bag!")
        elif user_shop_data[20] >= 1:
            deploy_laptop_data = int(user_shop_data[20] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 200000) 
            await self.bot.db.execute("UPDATE shop SET fossils = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} fossil(s) have been sold from your bag!")
        if user_shop_data[20] == None:
            return await ctx.send(f"You dont have any fossil(s) in your bag!")

    @sell.command()
    async def moths(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[19]:
            return await ctx.send(f"You dont have that many moth(s) in your bag!")
        elif user_shop_data[19] >= 1:
            deploy_laptop_data = int(user_shop_data[19] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 500) 
            await self.bot.db.execute("UPDATE shop SET moths = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} moth(s) have been sold from your bag!")
        elif user_shop_data[19] == None:
            return await ctx.send(f"You dont have any moth(s) in your bag!")

    @sell.command()
    async def caterpillar(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if user_shop_data[18] == None:
            return await ctx.send(f"You dont have any caterpillar(s) in your bag!")
        elif amount > user_shop_data[18]:
            return await ctx.send(f"You dont have that many caterpillar(s) in your bag!")
        elif user_shop_data[18] >= 1:
            deploy_laptop_data = int(user_shop_data[18] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 500) 
            await self.bot.db.execute("UPDATE shop SET caterpillars = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} caterpillar(s) have been sold from your bag!")


    @sell.command()
    async def worms(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[17]:
            return await ctx.send(f"You dont have that many worm(s) in your bag!")
        elif user_shop_data[17] >= 1:
            deploy_laptop_data = int(user_shop_data[17] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 500) 
            await self.bot.db.execute("UPDATE shop SET worms = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} worm(s) have been sold from your bag!")
        elif user_shop_data[17] == None:
            return await ctx.send(f"You dont have any worm(s) in your bag!")

    @sell.command()
    async def legendaryfish(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[16]:
            return await ctx.send(f"You dont have that many legendary fish in your bag!")
        elif user_shop_data[16] >= 1:
            deploy_laptop_data = int(user_shop_data[16] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 75000) 
            await self.bot.db.execute("UPDATE shop SET legenda_fish = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} legendary fish have been sold from your bag!")
        elif user_shop_data[16] == None:
            return await ctx.send(f"You dont have any legendary fish in your bag!")

    @sell.command()
    async def shoes(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[15]:
            return await ctx.send(f"You dont have that many shoes in your bag!")
        elif user_shop_data[15] >= 1:
            deploy_laptop_data = int(user_shop_data[15] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 500) 
            await self.bot.db.execute("UPDATE shop SET shoes = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} shoes have been sold from your bag!")
        elif user_shop_data[15] == None:
            return await ctx.send(f"You dont have any shoes in your bag!")

    @sell.command()
    async def garbage(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[14]:
            return await ctx.send(f"You dont have that many garbage(s) in your bag!")
        elif user_shop_data[14] >= 1:
            deploy_laptop_data = int(user_shop_data[14] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 500) 
            await self.bot.db.execute("UPDATE shop SET garbage = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} garbage(s) have been sold from your bag!")
        elif user_shop_data[14] == None:
            return await ctx.send(f"You dont have any garbage(s) in your bag!")

    @sell.command(aliases=["rare fish"])
    async def rarefish(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[13]:
            return await ctx.send(f"You dont have that many rare fish in your bag!")
        elif user_shop_data[143] >= 1:
            deploy_laptop_data = int(user_shop_data[13] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 5000) 
            await self.bot.db.execute("UPDATE shop SET rarefish = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} rare fish have been sold from your bag!")
        elif user_shop_data[13] == None:
            return await ctx.send(f"You dont have any rare fish in your bag!")
    @sell.command()
    async def snake(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[8]:
            return await ctx.send(f"You dont have that many snake(s) in your bag!")
        elif user_shop_data[8] >= 1:
            deploy_laptop_data = int(user_shop_data[8] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 5000) 
            await self.bot.db.execute("UPDATE shop SET snake = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} snake(s) have been sold from your bag!")
        elif user_shop_data[8] == None:
            return await ctx.send(f"You dont have any snake(s) in your bag!")

    @sell.command(aliases=["lap"])
    async def laptop(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        user_shop_data = await self.get_shop_data(ctx.author)
        if amount > user_shop_data[1]:
            return await ctx.send(f"You dont have that many laptop(s) in your bag!")
        elif user_shop_data[1] >= 1:
            deploy_laptop_data = int(user_shop_data[1] - amount)
            user_buy_deploy_data = int(user_buy_data[0] + 500) 
            await self.bot.db.execute("UPDATE shop SET laptop = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} laptop(s) have been sold from your bag!")
        elif user_shop_data[1] == None:
            return await ctx.send(f"You dont have any laptop in your bag!")

    @commands.group(invoke_without_command=True)
    async def buy(self,ctx):
        await ctx.send("That item isn't there mate! For more info look into the shop command!")

    @buy.command(aliases=["rod", "fishrod"])
    async def fishingrod(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        if user_buy_data[0] >= 10000:
            user_shop_data = await self.get_shop_data(ctx.author)
            if user_shop_data[3] == None:
                deploy_laptop_data = int(amount)
            else:
                deploy_laptop_data = int(user_shop_data[3] + amount)
            user_buy_deploy_data = int(user_buy_data[0] - 10000) 
            await self.bot.db.execute("UPDATE shop SET fishing_rod = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} fishing rod(s) have been bought from the shop!")
        else:
            await ctx.send("You need to have atleast 10000 :coin: to buy a fishing rod!")

    @buy.command(aliases=["hunting rifle","gun"])
    async def rifle(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        if user_buy_data[0] >= 10000:
            user_shop_data = await self.get_shop_data(ctx.author)
            if user_shop_data[2] == None:
                deploy_laptop_data = int(amount)
            else:
                deploy_laptop_data = int(user_shop_data[2] + amount)
            user_buy_deploy_data = int(user_buy_data[0] - 10000) 
            await self.bot.db.execute("UPDATE shop SET gun = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} rifle(s) have been bought from the shop!")
        else:
            await ctx.send("You need to have atleast 10000 :coin: to buy a rifle!")


    @buy.command()
    async def shovel(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        if user_buy_data[0] >= 7500:
            user_shop_data = await self.get_shop_data(ctx.author)
            if user_shop_data[5] == None:
                deploy_laptop_data = int(amount)
            else:
                deploy_laptop_data = int(user_shop_data[5] + amount)
            user_buy_deploy_data = int(user_buy_data[0] - 7500) 
            await self.bot.db.execute("UPDATE shop SET shovel = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} shovel(s) have been bought from the shop!")
        else:
            await ctx.send("You need to have atleast 7500 :coin: to buy a shovel!")

    @buy.command(aliases=["lap"])
    async def laptop(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        if user_buy_data[0] >= 1000:
            user_shop_data = await self.get_shop_data(ctx.author)
            if user_shop_data[1] == None:
                deploy_laptop_data = int(amount)
            else:
                deploy_laptop_data = int(user_shop_data[1] + amount)
            user_buy_deploy_data = int(user_buy_data[0] - 1000) 
            await self.bot.db.execute("UPDATE shop SET laptop = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} laptop(s) have been bought from the shop!")
        else:
            await ctx.send("You need to have atleast 1000 :coin: to buy a laptop!")

    @buy.command()
    async def crown(self,ctx, amount=1):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_buy_data = await self.get_bank_data(ctx.author)
        if user_buy_data[0] >= 100000000:
            user_shop_data = await self.get_shop_data(ctx.author)
            if user_shop_data[4] == None:
                deploy_laptop_data = int(amount)
            else:
                deploy_laptop_data = int(user_shop_data[4] + amount)
            user_buy_deploy_data = int(user_buy_data[0] - 100000000) 
            await self.bot.db.execute("UPDATE shop SET crownj = ? WHERE user_id = ?",(deploy_laptop_data,ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_buy_deploy_data,ctx.author.id))
            await self.bot.db.commit()
            await ctx.send(f"{amount} Instant crown(s) have been bought from the shop!")
        else:
            await ctx.send("You need to have atleast 100M :coin: to buy a crown!")

    
        

    @commands.command(aliases=["pm"])
    @commands.cooldown(1,30,commands.BucketType.user)
    async def postmemes(self,ctx):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user_laptops_shop_data = await self.get_shop_data(ctx.author)
        user_laptops = user_laptops_shop_data[1]
        if user_laptops == None:
            await ctx.send("You need to buy a laptop from the shop to post memes!")
        else:
            await ctx.send("Which kind of meme do you want to publish?",view=Meme(ctx))

    @commands.command()
    async def bag(self,ctx,member:nextcord.Member=None):
        await self.open_shop_account(ctx.author)
        await self.open_account(ctx.author)
        if member == None:
            member = ctx.author 
        member_shop_data = await self.get_shop_data(member)
        embed = Embed(description=f"```Bag Of {member.name}#{member.discriminator}```\n\n• Laptop - {member_shop_data[1]}\n• Gun - {member_shop_data[2]}\n• Fishing Rod - {member_shop_data[3]}\n• Crown Jewel - {member_shop_data[4]}\n• Shovel - {member_shop_data[5]}\n• Sheep - {member_shop_data[6]}\n• Pig - {member_shop_data[7]}\n• Snake - {member_shop_data[8]}\n• Lion - {member_shop_data[9]}\n• Tiger - {member_shop_data[10]}\n• Dragon - {member_shop_data[11]}\n• Fish - {member_shop_data[12]}\n• Rare Fish - {member_shop_data[13]}\n• Garbage - {member_shop_data[14]}\n• Shoes - {member_shop_data[15]}\n• Legendary Fish - {member_shop_data[16]}\n• Worms - {member_shop_data[17]}\n• Caterpillar - {member_shop_data[18]}\n• Moths - {member_shop_data[19]}\n• Fossils - {member_shop_data[20]}",colour=0xFF006D)
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["fish"])
    @commands.cooldown(1,30,commands.BucketType.user)
    async def fishing(self,ctx):
        await self.open_shop_account(ctx.author)
        await self.open_account(ctx.author)


        hunt_shop_data = await self.get_shop_data(ctx.author)
        if hunt_shop_data[3] == None:
            return await ctx.send("You need a fishing rod to fish man! Buy it from the store (if you have money)!")
        elif hunt_shop_data[3] >=1:
            hunt_choices = ["fish","rarefish","legenda_fish","garbage","shoes"]
            possibilities_hunt = [0.2, 0.15 , 0.05 ,0.3, 0.3 ]
            hunt_random_choice = np.random.choice(hunt_choices,p=possibilities_hunt)

            hunt_responses = ["You caught a random animal","You were unlucky and didn't catch anything","You were trying to catch a fish and you fell into the river and lost your fishing rod , well atleast you didnt drown {removes rod from inv}"]
            hunt_response_choice = random.choices(hunt_responses)

            if hunt_response_choice[0] == "You were unlucky and didn't catch anything":
                return await ctx.send("You were unlucky and didn't catch anything!")
            elif hunt_response_choice[0] == "You were trying to catch a fish and you fell into the river and lost your fishing rod , well atleast you didnt drown {removes rod from inv}":
                new_rifle = int(hunt_shop_data[3] - 1)
                await self.bot.db.execute("UPDATE shop SET fishing_rod = ? WHERE user_id = ?",(new_rifle,ctx.author.id))
                await self.bot.db.commit()
                await ctx.send("You were trying to catch a fish and you fell into the river and lost your fishing rod! Well atleast you didnt drown!")
            else:
                if hunt_random_choice == "fish":
                    if hunt_shop_data[12] == None:
                        dragon = int(1)
                    else:
                        dragon  = int(hunt_shop_data[12] + 1)
                    await self.bot.db.execute("UPDATE shop SET fish = ? WHERE user_id = ?",(dragon,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("You went fishing and caught a fish!")
                elif hunt_random_choice == "rarefish":
                    if hunt_shop_data[13] == None:
                        tiget = int(1)
                    else:
                        tiget = int(hunt_shop_data[13] + 1)
                    await self.bot.db.execute("UPDATE shop SET rarefish = ? WHERE user_id = ?",(tiget,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("You went to the fish hunt and brought back a rarefish!")
                elif hunt_random_choice == "legenda_fish":
                    if hunt_shop_data[16] == None:
                        lion = int(1)
                    else:
                        lion = int(hunt_shop_data[16] + 1)
                    await self.bot.db.execute("UPDATE shop SET legenda_fish = ? WHERE user_id = ?",(lion,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("Damn! Nice luck! You got a legendary fish!")
                elif hunt_random_choice == "shoes":
                    if hunt_shop_data[15] == None:
                        snake = int(1)
                    else:
                        snake = int(hunt_shop_data[15] + 1)
                    await self.bot.db.execute("UPDATE shop SET shoes = ? WHERE user_id = ?",(snake,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("Here, take this used shoe :mans_shoe: !")
                elif hunt_random_choice == "garbage":
                    if hunt_shop_data[14] == None:
                        sheep = int(1)
                    else:
                        sheep = int(hunt_shop_data[14] + 1)
                    await self.bot.db.execute("UPDATE shop SET garbage = ? WHERE user_id = ?",(sheep,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("Take this hand of garbage in which you were born!")


    @commands.command(aliases=["dig"])
    @commands.cooldown(1,30,commands.BucketType.user)
    async def digging(self, ctx):
        await self.open_shop_account(ctx.author)
        await self.open_account(ctx.author)


        hunt_shop_data = await self.get_shop_data(ctx.author)
        if hunt_shop_data[5] == None:
            return await ctx.send("You need a shovel to dig man! Buy it from the store (if you have money)!")
        elif hunt_shop_data[5] >=1:
            hunt_choices = ["worms","caterpillars","garbage","snakes","moths","fossils"]
            possibilities_hunt = [0.2, 0.2 , 0.2 ,0.19, 0.2 , 0.01 ]
            hunt_random_choice = np.random.choice(hunt_choices,p=possibilities_hunt)

            hunt_responses = ["You caught a random animal","You were unlucky and didn't catch anything","YYour mom found you getting dirty and broke your shovel , well atleast she didnt hit you {removes shovel from inv}"]
            hunt_response_choice = random.choices(hunt_responses)

            if hunt_response_choice[0] == "You were unlucky and didn't catch anything":
                return await ctx.send("You were unlucky and didn't catch anything!")
            elif hunt_response_choice[0] == "Your mom found you getting dirty and broke your shovel , well atleast she didnt hit you {removes shovel from inv}":
                new_rifle = int(hunt_shop_data[5] - 1)
                await self.bot.db.execute("UPDATE shop SET shovel = ? WHERE user_id = ?",(new_rifle,ctx.author.id))
                await self.bot.db.commit()
                await ctx.send("Your mom found you getting dirty and broke your shovel! well atleast she didn't hit you!")
            else:
                if hunt_random_choice == "worms":
                    if hunt_shop_data[17] == None:
                        dragon = int(1)
                    else:
                        dragon = int(hunt_shop_data[17] + 1)
                    await self.bot.db.execute("UPDATE shop SET worms = ? WHERE user_id = ?",(dragon,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("You dug and brought a worm!")
                elif hunt_random_choice == "caterpillars":
                    if hunt_shop_data[18] == None:
                        tiget = int(1)
                    else:
                        tiget = int(hunt_shop_data[18] + 1)
                    await self.bot.db.execute("UPDATE shop SET caterpillars = ? WHERE user_id = ?",(tiget,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("You found a caterpillar!")
                elif hunt_random_choice == "garbage":
                    if hunt_shop_data[14] == None:
                        lion = int(1)
                    else:
                        lion = int(hunt_shop_data[14] + 1)
                    await self.bot.db.execute("UPDATE shop SET garbage = ? WHERE user_id = ?",(lion,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("Ew ! How were you so mad that you brought back garbage!")
                elif hunt_random_choice == "snakes":
                    if hunt_shop_data[8] == None:
                        snake = int(1)
                    else:
                        snake = int(hunt_shop_data[8] + 1)
                    await self.bot.db.execute("UPDATE shop SET snake = ? WHERE user_id = ?",(snake,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("You went to the woods and brought back a snake!")
                elif hunt_random_choice == "moths":
                    if hunt_shop_data[19] == None:
                        pig = int(1)
                    else:
                        pig = int(hunt_shop_data[19] + 1)
                    await self.bot.db.execute("UPDATE shop SET moths = ? WHERE user_id = ?",(pig,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("You found a moth!")
                elif hunt_random_choice == "fossils":
                    if hunt_shop_data[20] == None:
                        sheep = int(1)
                    else:
                        sheep = int(hunt_shop_data[20] + 1)
                    await self.bot.db.execute("UPDATE shop SET fossils = ? WHERE user_id = ?",(sheep,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("Damn! Your luck is good! You found some fossils that you brought back home and became famous!")


    @commands.command(aliases=["hunt"])
    @commands.cooldown(1,30,commands.BucketType.user)
    async def hunting(self,ctx):
        await self.open_shop_account(ctx.author)
        await self.open_account(ctx.author)


        hunt_shop_data = await self.get_shop_data(ctx.author)
        if hunt_shop_data[2] == None:
            return await ctx.send("You need a rifle to hunt man! Buy it from the store (if you have money)!")
        elif hunt_shop_data[2] >=1:
            hunt_choices = ["dragon","tiger","lion","snake","pig","sheep"]
            possibilities_hunt = [0.02, 0.09 , 0.09 ,0.2, 0.3 , 0.3 ]
            hunt_random_choice = np.random.choice(hunt_choices,p=possibilities_hunt)

            hunt_responses = ["You caught a random animal","You were unlucky and didn't catch anything","You tried to catch a lion and failed , you broke your hunting rifle well atleast ur alive {removes rifle from inv}"]
            hunt_response_choice = random.choices(hunt_responses)

            if hunt_response_choice[0] == "You were unlucky and didn't catch anything":
                return await ctx.send("You were unlucky and didn't catch anything!")
            elif hunt_response_choice[0] == "You tried to catch a lion and failed , you broke your hunting rifle well atleast ur alive {removes rifle from inv}":
                new_rifle = int(hunt_shop_data[2] - 1)
                await self.bot.db.execute("UPDATE shop SET gun = ? WHERE user_id = ?",(new_rifle,ctx.author.id))
                await self.bot.db.commit()
                await ctx.send("You tried to catch a lion and failed , you broke your hunting rifle! Well atleast ur alive!")
            else:
                if hunt_random_choice == "dragon":
                    if hunt_shop_data[11] == None:
                        dragon = int(1)
                    else:
                        dragon = int(hunt_shop_data[11] + 1)
                    await self.bot.db.execute("UPDATE shop SET dragon = ? WHERE user_id = ?",(dragon,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("Damn! Your luck is good! You just caught a dragon!")
                elif hunt_random_choice == "tiger":
                    if hunt_shop_data[10] == None:
                        tiget = int(1)
                    else:
                        tiget = int(hunt_shop_data[10] + 1)
                    await self.bot.db.execute("UPDATE shop SET tiger = ? WHERE user_id = ?",(tiget,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("You went to the hunt and brought back a tiger!")
                elif hunt_random_choice == "lion":
                    if hunt_shop_data[9] == None:
                        lion = int(1)
                    else:
                        lion = int(hunt_shop_data[9] + 1)
                    await self.bot.db.execute("UPDATE shop SET lion = ? WHERE user_id = ?",(lion,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("You brought back the king..LION!")
                elif hunt_random_choice == "snake":
                    if hunt_shop_data[8] == None:
                        snake = int(1)
                    else:
                        snake = int(hunt_shop_data[8] + 1)
                    await self.bot.db.execute("UPDATE shop SET snake = ? WHERE user_id = ?",(snake,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("You went to the woods and brought back a snake!")
                elif hunt_random_choice == "pig":
                    if hunt_shop_data[7] == None:
                        pig = int(1)
                    else:
                        pig = int(hunt_shop_data[7] + 1)
                    await self.bot.db.execute("UPDATE shop SET pig = ? WHERE user_id = ?",(pig,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("You went to hunt and brought back a pig!")
                elif hunt_random_choice == "sheep":
                    if hunt_shop_data[6] == None:
                        sheep = int(1)
                    else:
                        sheep = int(hunt_shop_data[6] + 1)
                    await self.bot.db.execute("UPDATE shop SET sheep = ? WHERE user_id = ?",(sheep,ctx.author.id))
                    await self.bot.db.commit()
                    await ctx.send("You have caught a sheep! Make sure to make woolen clothes!")


    @commands.command()
    @commands.cooldown(1,86400,commands.BucketType.user)
    async def daily(self,ctx):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user = await self.get_bank_data(ctx.author)
        money = random.choices([i for i in range(100,10000)])

        daily_amount = int(user[0] + money[0])
        await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(daily_amount,ctx.author.id))
        await self.bot.db.commit()
        embed = Embed(description=f"```{ctx.author.name}#{ctx.author.discriminator}```\nYour daily claim status:- You have got {money[0]} added to your wallet balance!", colour=0xFF006D)
        await ctx.send(embed=embed)


    @commands.command()
    @commands.cooldown(1,2629746,commands.BucketType.user)
    async def monthly(self,ctx):
        await self.open_account(ctx.author)
        await self.open_shop_account(ctx.author)
        user = await self.get_bank_data(ctx.author)
        money = random.choices([i for i in range(10000,50000)])
        daily_amount = int(user[0] + money[0])
        await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(daily_amount,ctx.author.id))
        await self.bot.db.commit()
        embed = Embed(description=f"```{ctx.author.name}#{ctx.author.discriminator}```\nYour monthly claim status:- You have got {money[0]} added to your wallet balance!", colour=0xFF006D)
        await ctx.send(embed=embed)

    @commands.command(name="lb-ec")
    async def lbec(self,ctx):
            cursor = await self.bot.db.cursor()
            await cursor.execute("SELECT bal, bank, user_id FROM users ORDER BY bal DESC , bank DESC")
            leaderboard = await cursor.fetchall()
            pages = []
            page_count = -(-len(leaderboard)//10) #will return 3 if users' length is 23
            for i in range(page_count):
                embed = nextcord.Embed(
                    title = f"Leaderboard | {ctx.guild.name}",
                    colour = 0xFF006D
                )
                embed.set_footer(
                    text = f"Page {i + 1}/{page_count}"
                )
                for rank, data in enumerate(leaderboard[i * 10:i * 10 + 10], start=i * 10 + 1):
                    level = data[0]
                    xp = data[1]
                    user_id = (data[2])

                    embed.add_field(
                    name = f"#{rank}",
                    value = f"**User**: <@!{user_id}>\n\n**Bal**: {level}\n\n**Bank**: {xp}\n\n",
                    inline = False)
                pages.append(embed)

            index = 0
            message = await ctx.send(embed=pages[0])
            emojis = ["◀️", "⏹", "▶️"]
            for emoji in emojis:
                await message.add_reaction(emoji)
            while not self.bot.is_closed():
                    try:
                        react, user = await self.bot.wait_for(
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

    @commands.command(aliases=["give"])
    async def send(self,ctx,amount:int,*,member:nextcord.Member):
        await self.open_account(member)
        await self.open_account(ctx.author)
        user = await self.get_bank_data(ctx.author)
        memberbal = await self.get_bank_data(member)
        if amount > user[0]:
            return await ctx.send("You can't give more than what you have! Common Sense? Duh!")
        else:
            user_new_bal = int(user[0] - amount)
            member_new_bal = int(memberbal[0] + amount)
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(user_new_bal, ctx.author.id))
            await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(member_new_bal, member.id))
            await self.bot.db.commit()
            await ctx.send(f"{ctx.author.mention} You have given {amount} :coin: to {member.name}#{member.discriminator}")

def setup(bot):
    bot.add_cog(Economy(bot))

class Meme(nextcord.ui.View):
        def __init__(self, ctx, **kwargs):
            super().__init__(**kwargs)
            self.ctx = ctx

        async def interaction_check(self,interaction):
            if self.ctx.author == interaction.user:
                return
            else:
                await interaction.response.send_message("This message is not for you! Use your own post meme command to use these interactions",ephemeral=True)
            self.value = None

        @nextcord.ui.button(label='Fresh', style=nextcord.ButtonStyle.green)
        async def fresh(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            response = random.choices([1,2,3,4])
            responses = response[0]

            if responses == 1:
                response_one_moneyy = random.choices([i for i in range(1000,10000)])

                response_one_money = response_one_moneyy[0]
                money = await self.get_bank_data(interaction.user)
                extra_money = int(money[0] + response_one_money)
                await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(extra_money, interaction.user.id))
                await self.bot.db.commit()
                await interaction.response.send_message(f"Your meme exploded and you earned {response_one_money} :coin: !")
            elif responses == 2:
                response_one_moneyy = random.choices([i for i in range(1000,10000)])

                response_one_money = response_one_moneyy[0]
                money = await self.get_bank_data(interaction.user)
                extra_money = int(money[0] + response_one_money)
                await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(extra_money, interaction.user.id))
                await self.bot.db.commit()
                await interaction.response.send_message(f"Your meme is going viral and you earned {response_one_money} :coin: !")
            elif responses == 3:
                shop_data = await self.get_shop_data(interaction.user)
                new_laptops = int(shop_data[1] - 1)
                await self.bot.db.execute("UPDATE shop SET laptop = ? WHERE user_id = ?",(new_laptops,interaction.user.id))
                await self.bot.db.commit()
                await interaction.response.send_message("Everyone hated your meme and they broke your laptop!")
            elif responses == 4:
                await interaction.response.send_message("Your meme sucks and no one likes you!")


            self.stop()

        # This one is similar to the confirmation button except sets the inner value to `False`
        @nextcord.ui.button(label='Kind', style=nextcord.ButtonStyle.grey)
        async def kind(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            response = random.choices([1,2,3,4])
            responses = response[0]

            if responses == 1:
                response_one_moneyy = random.choices([i for i in range(1000,10000)])

                response_one_money = response_one_moneyy[0]
                money = await self.get_bank_data(interaction.user)
                extra_money = int(money[0] + response_one_money)
                await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(extra_money, interaction.user.id))
                await self.bot.db.commit()
                await interaction.response.send_message(f"Your meme exploded and you earned {response_one_money} :coin: !")
            elif responses == 2:
                response_one_moneyy = random.choices([i for i in range(1000,10000)])

                response_one_money = response_one_moneyy[0]
                money = await self.get_bank_data(interaction.user)
                extra_money = int(money[0] + response_one_money)
                await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(extra_money, interaction.user.id))
                await self.bot.db.commit()
                await interaction.response.send_message(f"Your meme is going viral and you earned {response_one_money} :coin: !")
            elif responses == 3:
                shop_data = await self.get_shop_data(interaction.user)
                new_laptops = int(shop_data[1] - 1)
                await self.bot.db.execute("UPDATE shop SET laptop = ? WHERE user_id = ?",(new_laptops,interaction.user.id))
                await self.bot.db.commit()
                await interaction.response.send_message("Everyone hated your meme and they broke your laptop!")
            elif responses == 4:
                await interaction.response.send_message("Your meme sucks and no one likes you!")


            self.stop()

        @nextcord.ui.button(label='Copy Pasta', style=nextcord.ButtonStyle.red)
        async def copypasta(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            response = random.choices([1,2,3,4])
            responses = response[0]

            if responses == 1:
                response_one_moneyy = random.choices([i for i in range(1000,10000)])

                response_one_money = response_one_moneyy[0]
                money = await self.get_bank_data(interaction.user)
                extra_money = int(money[0] + response_one_money)
                await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(extra_money, interaction.user.id))
                await self.bot.db.commit()
                await interaction.response.send_message(f"Your meme exploded and you earned {response_one_money} :coin: !")
            elif responses == 2:
                response_one_moneyy = random.choices([i for i in range(1000,10000)])

                response_one_money = response_one_moneyy[0]
                money = await self.get_bank_data(interaction.user)
                extra_money = int(money[0] + response_one_money)
                await self.bot.db.execute("UPDATE users SET bal = ? WHERE user_id = ?",(extra_money, interaction.user.id))
                await self.bot.db.commit()
                await interaction.response.send_message(f"Your meme is going viral and you earned {response_one_money} :coin: !")
            elif responses == 3:
                shop_data = await self.get_shop_data(interaction.user)
                new_laptops = int(shop_data[1] - 1)
                await self.bot.db.execute("UPDATE shop SET laptop = ? WHERE user_id = ?",(new_laptops,interaction.user.id))
                await self.bot.db.commit()
                await interaction.response.send_message("Everyone hated your meme and they broke your laptop!")
            elif responses == 4:
                await interaction.response.send_message("Your meme sucks and no one likes you!")


            self.stop()

