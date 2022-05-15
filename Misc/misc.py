import nextcord
from nextcord.ext import commands
from nextcord import Embed
from nextcord import Member
from datetime import datetime as dt
import random
import asyncio
from games import tictactoe, wumpus, hangman, minesweeper, twenty
from Views.calc import InteractiveView
from Views.buttontic import TicTacToeButton

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["info","userinfo","user-info"])
    async def whois(self, ctx, member:nextcord.Member=None):
        """
        Shows information about a member in a server
        """
        if member==None:
            member=ctx.author
        embed = Embed(description=f"```Showing Information of {member}```\n\n",colour=0x2f3136)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="📅",
        value=member.created_at.strftime("%Y-%m-%d"),
        inline=False)
        embed.add_field(name="<a:member_join:945654446686367835> Joined at",
        value=member.joined_at.strftime("%Y-%m-%d"),
        inline=False)
        for i in range(0,len(member.roles)):
            values=member.roles[i]
            
        embed.add_field(name="<:role:945655213249921175> Roles",
            value=values,
            inline=True)
        embed.add_field(name="<:name:945656039007719424> Server Display Name",
        value=f"**{member.display_name}**",
        inline=True)
        try:
            embed.add_field(name="<a:activities:945657106449707018> Activity",
            value="**{member.activities[0].name}**",
            inline=False)
        except:
            embed.add_field(name="<a:activities:945657106449707018> Activity",
            value="<a:cross:945657241879609434> **No activities currently.**",
            inline=True)
        if member.bot:
            value="<a:verifytick:942981999583449160> **Yes**"
        else:
            value="<a:cross:945657241879609434> **No**"
        embed.add_field(name="Is bot?",
        value=value,
        inline=False)
        #embed.timestamp = dt.datetime.now()
        await ctx.send(embed=embed)

    @commands.command(aliases=["avatar","pfp"])
    async def av(self, ctx, member:Member=None):
        """Shows a member's avatar'"""
        if member is None:
            member=ctx.author
        embed=Embed(description=f"```Showing Avatar of {member}```",colour=0x2f3136)
        #embed.timestamp = dt.datetime.now()
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["number-of-commands","commands"])
    async def nc(self, ctx):
        """Shows the number of commands in the bot"""
        embed=Embed(description=f"```The number of commands is {len(self.bot.commands)}```",colour=0x2f3136)
        embed.timestamp = dt.now()
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(icon_url=ctx.author.display_avatar.url, text=f"Requested by {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(name='2048')
    async def twenty(self, ctx):
        """Play 2048 game"""
        await twenty.play(ctx, self.bot)

    @commands.command(name="8ball")
    async def eight_ball(self, ctx, ques=""):
        """Magic 8Ball"""
        if ques=="":
            await ctx.send("Ask me a question first")
        else:
            choices = [
            'It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes – definitely.', 'You may rely on it.',
            'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
            'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.',
            "Don't count on it.", 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Very doubtful.'
            ]
            await ctx.send(f":8ball: says: ||{random.choice(choices)}||")

    @commands.command(name='hangman', aliases=['hang'])
    async def hangman(self, ctx):
        """Play Hangman"""
        await hangman.play(self.bot, ctx)

    @commands.command(name='minesweeper', aliases=['ms'])
    async def minesweeper(self, ctx, columns = None, rows = None, bombs = None):
        """Play Minesweeper"""
        await minesweeper.play(ctx, columns, rows, bombs)

    

    @commands.command(name='rps', aliases=['rockpaperscissors'])
    async def rps(self, ctx):
        """Play Rock, Paper, Scissors game"""
        def check_win(p, b):
            if p=='🌑':
                return False if b=='📄' else True
            if p=='📄':
                return False if b=='✂' else True
            # p=='✂'
            return False if b=='🌑' else True

        async with ctx.typing():
            reactions = ['🌑', '📄', '✂']
            game_message = await ctx.send("**Rock Paper Scissors**\nChoose your shape:", delete_after=15.0)
            for reaction in reactions:
                await game_message.add_reaction(reaction)
            bot_emoji = random.choice(reactions)

        def check(reaction, user):
            return user != self.bot.user and user == ctx.author and (str(reaction.emoji) == '🌑' or '📄' or '✂')
        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Time's Up! :stopwatch:")
        else:
            await ctx.send(f"**:man_in_tuxedo_tone1:\t{reaction.emoji}\n:robot:\t{bot_emoji}**")
            # if conds
            if str(reaction.emoji) == bot_emoji:
                await ctx.send("**It's a Tie :ribbon:**")
            elif check_win(str(reaction.emoji), bot_emoji):
                await ctx.send("**You win :sparkles:**")
            else:
                await ctx.send("**I win :robot:**")

    

    @commands.command(name='teams', aliases=['team'])
    async def teams(self, ctx, num=2):
        """Makes random teams with specified number(def. 2)"""
        if not ctx.author.voice:
            return await ctx.send("You are not connected to a voice channel :mute:")
        members = ctx.author.voice.channel.members
        memnames = []
        for member in members:
            memnames.append(member.name)

        remaining = memnames
        if len(memnames)>=num:
            for i in range(num):
                team = random.sample(remaining,len(memnames)//num)
                remaining = [x for x in remaining if x not in team]
                await ctx.send(f"Team {chr(65+i)}\n" + "```CSS\n" + '\n'.join(team) + "\n```")
        if len(remaining)> 0:
            await ctx.send("Remaining\n```diff\n- " + '\n- '.join(remaining) + "\n```")

    @commands.command(name='toss', aliases=['flip'])
    async def toss(self, ctx):
        """Flips a Coin"""
        coin = ['+ heads', '- tails']
        await ctx.send(f"```diff\n{random.choice(coin)}\n```")

    @commands.command(name='quiz', aliases=['trivia'])
    async def quiz(self, ctx):
        """Start an interactive quiz game"""
        try:
            async with ctx.typing():
                question = await self.tclient.fetch_questions(
                    amount=1
                    # difficulty=aiopentdb.Difficulty.easy
                )
                question = question[0]
                if question.type.value == 'boolean':
                    options = ['True', 'False']
                else:
                    options = [question.correct_answer]
                    options.extend(question.incorrect_answers)
                    options = random.sample(options, len(options)) # Shuffle
                answer = options.index(question.correct_answer)

                if len(options) == 2 and options[0] == 'True' and options[1] == 'False':
                    reactions = ['✅', '❌']
                else:
                    reactions = ['1⃣', '2⃣', '3⃣', '4⃣']

                description = []
                for x, option in enumerate(options):
                    description += '\n {} {}'.format(reactions[x], option)

                embed = nextcord.Embed(title=question.content, description=''.join(description), color=nextcord.Colour(0xFF9933))
                embed.set_footer(text='Answer using the reactions below⬇')
                quiz_message = await ctx.send(embed=embed)
                for reaction in reactions:
                    await quiz_message.add_reaction(reaction)

            def check(reaction, user):
                return user != self.bot.user and user == ctx.author and (str(reaction.emoji) == '1️⃣' or '2️⃣' or '3️⃣' or '4️⃣' or '✅' or '❌')

            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(f"Time's Up! :stopwatch:\nAnswer is **{options[answer]}**")
            else:
                if str(reaction.emoji) == reactions[answer]:
                    await ctx.send("Correct answer:sparkles:")
                else:
                    await ctx.send(f"Wrong Answer :no_entry_sign:\nAnswer is **{options[answer]}**")
        except:
            return await ctx.send('Failed to start quiz :x:')

    @commands.command(name='tictactoe', aliases=['ttt'])
    async def ttt(self, ctx):
        """Play Tic-Tac-Toe"""
        await tictactoe.play_game(self.bot, ctx, chance_for_error=0.2) # Win Plausible

    @commands.command(name='wumpus')
    async def _wumpus(self, ctx):
        """Play Wumpus game"""
        await wumpus.play(self.bot, ctx)

    @commands.command(name="calculator",aliases=["calc","calculate"])
    async def interactive_calc(self, ctx):
        """Start the calculator"""
        view = InteractiveView()
        await ctx.send("```\n```",view=view)

    @commands.command()
    async def bttt(self, ctx):
        """Play Button Tic-Tac-Toe"""
        await ctx.send(f"Tic-Tac-Toe Buttons, :x: goes first.",view=TicTacToeButton())
def setup(bot):
    bot.add_cog(Miscellaneous(bot))