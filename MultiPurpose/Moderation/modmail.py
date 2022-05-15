from nextcord.ext import commands
from nextcord import utils
import nextcord
import asyncio

class onMessage(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			return

		if isinstance(message.channel, nextcord.DMChannel):
			guild = self.bot.get_guild(921667897447813192)
			categ = utils.get(guild.categories, name = "Modmail tickets")
			if not categ:
				overwrites = {
					guild.default_role : nextcord.PermissionOverwrite(read_messages = False),
					guild.me : nextcord.PermissionOverwrite(read_messages = True)
				}
				categ = await guild.create_category(name = "Modmail tickets", overwrites = overwrites)

			channel = nextcord.utils.get(categ.channels, topic = str(message.author.id))
			if not channel:
				channel = await categ.create_text_channel(name = f"{message.author.name}#{message.author.discriminator}", topic = str(message.author.id))
				await channel.send(f"New modmail created by {message.author.mention}")

			embed = nextcord.Embed(description = message.content, colour = 0x696969)
			embed.set_author(name = message.author, icon_url = message.author.avatar.url)
			await channel.send(embed = embed)

		elif isinstance(message.channel, nextcord.TextChannel):
			if message.content.startswith("!"):
				pass
			else:
				topic = message.channel.topic
				if topic:
					member = message.guild.get_member(int(topic))
					if member:
						embed = nextcord.Embed(description = message.content, colour = 0x696969)
						embed.set_author(name = message.author, icon_url = message.author.avatar.url)
						await member.send(embed = embed)

	@commands.command()
	async def close(self, ctx):
		if ctx.channel.category.name == "Modmail tickets":
			await ctx.send("Deleting the channel in 10 seconds!")
			await asyncio.sleep(10)
			await ctx.channel.delete()

def setup(bot):
	bot.add_cog(onMessage(bot))