import nextcord
from nextcord.ext import commands
from Views.confirm import Confirm
from nextcord import Embed
import asyncio
from Views.staff_view import staffView
from time import sleep

class Apply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def apply(self, ctx):
        view = Confirm()
        embed = Embed(description=f"**Staff Application process for {ctx.guild.name}**")
        await ctx.send(embed=embed,view=view)
        await view.wait()
        if view.value is None:
            await ctx.send(f"{ctx.author.mention} this process has timed out.")
        elif view.value:
            try:
                channel = await ctx.author.create_dm()
            except:
                return await ctx.send(f"{ctx.author.mention} Please open your DM's")

            q_list = ["Which Region are you from?",
            "What time do you usually play?",
            "Casual or Competitive?",
            "Main Gun Type Used?",
            "In Game Role",
            "Can You use VC?",
            "Previous Clans / Team you have played for? If any.",
            "What tier were the teams you played for?",
            "Briefly Describe Why do you wanna join us? What will you be wiling to offer the clan",
            "What makes you choose TRX over other clans out there ?",
            "Attach SS of Your ingame Stats below",
            "You agree that you have answered all the above questions truthfully and is willing to face consequences if proved fake"]

            a_list= []

            def check(m):
                return m.content is not None and m.channel == channel and m.author == ctx.author

            for question in q_list:
                sleep(.5)
                try:
                    await channel.send(question)
                except:
                    return await ctx.send(f"{ctx.author.mention} Please open your DM's.")
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=60)
                except asyncio.TimeoutError:
                    return await channel.send(f"{ctx.author.mention} This process has timed out!")
                if msg.content == "cancel" or msg.content == "abort":
                    return await channel.send(f"{ctx.author.mention} This process has timed out!")
                if msg.attachments:
                    a_list.append(msg.attachments[0])
                else:
                    a_list.append(msg.content)
        else:
            return await ctx.send(f"Procesds successfully aborted.")
        
        em = Embed(description="\n".join(f'{a}. {b}' for a, b in enumerate(a_list, 1)))
        await ctx.send(content=ctx.author.mention,embed=em,view=staffView())
def setup(bot):
    bot.add_cog(Apply(bot))
