import nextcord
from nextcord.ext import menus,commands
from nextcord import slash_command
from .utils_for_wordle import (
    generate_puzzle_embed,
    is_game_over,
    is_valid_word,
    random_puzzle_id,
    update_embed,
)


GUILD_IDS = [921667897447813192, 843120245908176896, 911617189595979857, 946284164020326440, 843120245908176896, 946284164020326440, 724690424790515742]


class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def make(self, user, game):
        invite = await user.voice.channel.create_invite(
            reason="Play game",
            unique=False,
            target_type=nextcord.InviteTarget.embedded_application,
            target_application_id=game,
        )
        return invite.url


    @slash_command(name="activities",description="Use the different discord activities",guild_ids = GUILD_IDS)
    async def activites_(
        self,
        interaction: nextcord.Interaction,
        game: str = nextcord.SlashOption(
            name="game",
            choices={
                "Poker": "755827207812677713",
                "Chess in the park": "832012774040141894",
                "Sketch Heads / Doodle Crew": "902271654783242291",
                "Letter League / Letter Tile": "879863686565621790",
                "Spellcast": "852509694341283871",
                "Awkword": "879863881349087252",
                "Youtube Together": "755600276941176913",
                "Watch Together": "880218394199220334",
                "Checkers in the park": "832013003968348200",
                "Wordsnacks": "879863976006127627",
                "Ocho": "832025144389533716",
                "Betryal.io": "773336526917861400",
                "Fishington.io": "814288819477020702",
            },
            description="Choose the game you wish to play!",
        ),
    ):
        if not interaction.user.voice:
            return await interaction.response.send_message(
                "Connect to a voice channel.", ephemeral=True
            )
        return await interaction.response.send_message(
            await self.make(interaction.user, int(game)), ephemeral=False
        )

    @commands.Cog.listener()
    async def on_message(self, message):

        
        if message.type == nextcord.MessageType.premium_guild_subscription:
            embed=nextcord.Embed(title="Server just got boosted!", description=f"Thanks to {message.author.mention} for boosting!\nWe appreciate your work!",colour=0xFF0000)
            await message.channel.send(embed=embed)
        ref = message.reference
        if not ref or not isinstance(ref.resolved, nextcord.Message):
            return
        parent = ref.resolved

        if parent.author.id != self.bot.user.id:
            return

        if not parent.embeds:
            return

        embed = parent.embeds[0]

        guess = message.content.lower()

        if (
            embed.author.name != message.author.name
            or embed.author.icon_url != message.author.display_avatar.url
        ):
            reply = "Start a new game with /play"
            if embed.author:
                reply = f"This game was started by {embed.author.name}. " + reply
            await message.reply(reply,mention_author=False, delete_after=5)
            try:
                await message.delete(delay=5)
            except Exception:
                pass
            return

        if is_game_over(embed):
            await message.reply(
                "The game is already over. Start a new game with /play", delete_after=5
            )
            try:
                await message.delete(delay=5)
            except Exception:
                pass
            return

        if len(message.content.split()) > 1:
            await message.reply(
                "Please respond with a single 5-letter word.",mention_author=False, delete_after=5
            )
            try:
                await message.delete(delay=5)
            except Exception:
                pass
            return

        if not is_valid_word(guess):
            await message.reply("That is not a valid word",mention_author=False, delete_after=5)
            try:
                await message.delete(delay=5)
            except Exception:
                pass
            return

        embed = update_embed(embed, guess)
        await parent.edit(embed=embed)

        try:
            await message.delete()
        except Exception:
            pass

    @slash_command(name="play",description="Play a game of Wordle Clone",guild_ids = GUILD_IDS)
    async def play_(
        interaction: nextcord.Interaction,
        puzzle_id: int = nextcord.SlashOption(
            description="Puzzle ID, leave out for a random puzzle", required=False
        ),
    ):
        print("Play command of wordle clone")
        puzzle_id = puzzle_id or random_puzzle_id()
        embed = generate_puzzle_embed(interaction.user, puzzle_id)
        await interaction.send(embed=embed)

def setup(bot):
    bot.add_cog(SlashCommands(bot))