import nextcord
from nextcord.ext import commands
from nextcord import Embed

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error,commands.BadArgument):
            e = Embed(description=f"```The parameters or arguments you have provided are incorrect.```",color=0x2f3136)
            e.set_thumbnail(url=ctx.author.display_avatar.url)
            await ctx.send(embed=e)
        
        elif isinstance(error, commands.CheckFailure):
            e = Embed(description=f"```This Command is not for you.```",color=0x2f3136)
            e.set_thumbnail(url=ctx.author.display_avatar.url)
            await ctx.send(embed=e)
        
        elif isinstance(error, commands.BotMissingPermissions):
            e = Embed(description=f"```The bot is missing permissions for this command.```",color=0x2f3136)
            e.set_thumbnail(url=ctx.author.display_avatar.url)
            await ctx.send(embed=e)

        elif isinstance(error, commands.DisabledCommand):
            e = Embed(description=f"```This command is disabled.```",color=0x2f3136)
            e.set_thumbnail(url=ctx.author.display_avatar.url)
            await ctx.send(embed=e)

        elif isinstance(error, commands.MissingPermissions):
            e = Embed(description=f"```OOPS! Looks like you are missing permissions for this command.```",color=0x2f3136)
            e.set_thumbnail(url=ctx.author.display_avatar.url)
            await ctx.send(embed=e)

        elif isinstance(error, commands.MissingRequiredArgument):
            e = Embed(description=f"```Looks like you have not entered all the required arguments.```",color=0x2f3136)
            e.set_thumbnail(url=ctx.author.display_avatar.url)
            await ctx.send(embed=e)

        elif isinstance(error, commands.CommandNotFound):
            e = Embed(description=f"```No command called {ctx.message.content} was found. Please use the help command to get a list of commands available.```",color=0x2f3136)
            e.set_thumbnail(url=ctx.author.display_avatar.url)
            await ctx.send(embed=e)
            
        else:
            await ctx.send(str(error))
            raise error
            

def setup(bot):
    bot.add_cog(Errors(bot))