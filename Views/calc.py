from simpcalc import simpcalc # pip install simpcalci
import nextcord
from nextcord.ext import commands # pip install nextcord.py

# alternate for simpcalc package

# import aiohttp
# class BadArgument(Exception):
#    """This is raise when a bad/invalid argument is passed"""
#    pass

# async def calculate(self, expr):
#        expr = expr.replace('**', '^')
#        my_expr = "".join(expr.split(expr))
#        my_expr = urllib.parse.quote(expr)
#        async with aiohttp.ClientSession() as session:
#            async with session.get(f"http://api.mathjs.org/v4/?expr={my_expr}") as r:
#              result = await r.text()
#        if result.startswith("Error:"):
#            raise BadArgument("An Invalid argument was passed.")
#        return result

class InteractiveView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.expr = ""
        self.calc = simpcalc.Calculate() # if you are using the above function, no need to declare this!

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="1", row=0)
    async def one(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "1"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="2", row=0)
    async def two(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "2"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="3", row=0)
    async def three(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "3"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="+", row=0)
    async def plus(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "+"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="4", row=1)
    async def last(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "4"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="5", row=1)
    async def five(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "5"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="6", row=1)
    async def six(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "6"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="/", row=1)
    async def divide(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            self.expr += "/"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="7", row=2)
    async def seven(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "7"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="8", row=2)
    async def eight(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "8"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="9", row=2)
    async def nine(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "9"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="*", row=2)
    async def multiply(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "*"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label=".", row=3)
    async def dot(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "."
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="0", row=3)
    async def zero(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "0"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="=", row=3)
    async def equal(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        try:
            self.expr = await self.calc.calculate(self.expr)
        except commands.BadArgument: # if you are function only, change this to BadArgument
            return await interaction.response.send_message("Um, looks like you provided a wrong expression....")
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="-", row=3)
    async def minus(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "-"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="(", row=4)
    async def left_bracket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "("
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label=")", row=4)
    async def right_bracket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += ")"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.red, label="C", row=4)
    async def clear(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr = ""
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.red, label="<--", row=4)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr = self.expr[:-1]
        await interaction.message.edit(content=f"```\n{self.expr}\n```")