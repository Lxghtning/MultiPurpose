import nextcord
from nextcord.ext import commands
import aiohttp

class crosschat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def startcrosschat(self,ctx,guild_id:int,*,channel):
        try:
            guild = self.bot.get_guild(guild_id)
        except:
            return await ctx.send(f"{ctx.author.mention} Either the guild ID is wrong or the bot is not in that guild.")
        try:
            channe = nextcord.utils.get(guild.channels,name=channel)
        except:
            return await ctx.send(f"{ctx.author.mention} The guild does not have a channel with the name of {channel}")
        await channe.create_webhook(name="crosschat")
        await ctx.channel.create_webhook(name="crosschat")

        

def setup(bot):
    bot.add_cog(crosschat(bot))