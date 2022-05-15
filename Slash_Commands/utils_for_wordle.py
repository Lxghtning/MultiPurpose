import random
import nextcord

popular_words = open("D:\\MultiPurpose-Nextcord\\Slash_Commands\\dict-popular.txt").read().splitlines()
all_words = set(word.strip() for word in open("D:\\MultiPurpose-Nextcord\\Slash_Commands\\dict-sowpods.txt"))

EMOJI_CODES = {
    "green": {
        "a": "<:greena:940131507203375145>",
        "b": "<:greenb:940131507148828703>",
        "c": "<:greenc:940131507081732146>",
        "d": "<:greend:940131507123679262>",
        "e": "<:greene:940131506976874527>",
        "f": "<:greenf:940131507081707521>",
        "g": "<:greeng:940131507161403452>",
        "h": "<:greenh:940131507031392287>",
        "i": "<:greeni:940131507073327386>",
        "j": "<:greenj:940131506968485888>",
        "k": "<:greenk:940131507320786964>",
        "l": "<:greenl:940131506955882546>",
        "m": "<:greenm:940131507090108486>",
        "n": "<:greenn:940131507228532786>",
        "o": "<:greeno:940131506922344498>",
        "p": "<:greenp:940131506490318909>",
        "q": "<:greenq:940131506846851104>",
        "r": "<:greenr:940131506523877427>",
        "s": "<:greens:940131506934927421>",
        "t": "<:greent:940131506540654613>",
        "u": "<:greenu:940131506813280286>",
        "v": "<:greenv:940131506892992574>",
        "w": "<:greenw:940131506817466409>",
        "x": "<:greenx:940131506481938456>",
        "y": "<:greeny:940131507106881576>",
         "z":"<:greenz:940131506536456223>",
    },
    "yellow": {
        "a": "<:yellowa:940138870715056138>",
        "b": "<:yellowb:940143328253595689>",
        "c": "<:yellowc:940138871121928223>",
        "d": "<:yellowd:940138870337589259>",
        "e": "<:yellowe:940138870509559839>",
        "f": "<:yellowf:940138870463422504>",
        "g": "<:yellowg:940138870232739843>",
        "h": "<:yellowh:940138870740238386>",
        "i": "<:yellowh:940138870740238386>",
        "j": "<:yellowj:940138870455042048>",
        "k": "<:yellowk:940138870752817184>",
        "l": "<:yellowl:940138870547300362>",
        "m": "<:yellowm:940138870564077628>",
        "n": "<:yellown:940138870576672808>",
        "o": "<:yellowo:940138870480175164>",
        "p": "<:yellowp:940138870425673798>",
        "q": "<:yellowq:940138870467620914>",
        "r": "<:yellowr:940138870354354186>",
        "s": "<:yellows:940138870488571965>",
        "t": "<:yellowt:940138870484394004>",
        "u": "<:yellowu:940138870299840543>",
        "v": "<:yellowv:940138870308212736>",
        "w": "<:yelloww:940138870304043008>",
        "x": "<:yellowx:940138870333403176>",
        "y": "<:yellowy:940138870241099786>",
        "z": "<:yellowz:940138869821681695>",
    },
    "gray": {
        "a": "<:greya:940133833427271720>",
        "b": "<:greyb:940133833171431454>",
        "c": "<:greyc:940133832995262535>",
        "d": "<:greyd:940133832835891273>",
        "e": "<:greye:940133833125281792>",
        "f": "<:greyf:940133833209151558>",
        "g": "<:greyg:940133834039644171>",
        "h": "<:greyh:940133833221750784>",
        "i": "<:greyi:940133833070743593>",
        "j": "<:greyj:940133832978473011>",
        "k": "<:greyk:940133833066549248>",
        "l": "<:greyl:940133833280487434>",
        "m": "<:greym:940133833276264448>",
        "n": "<:greyn:940133832852668479>",
        "o": "<:greyo:940133833049780234>",
        "p": "<:greyp:940133833142046730>",
        "q": "<:greyq:940133833053970482>",
        "r": "<:greyr:940133833012031499>",
        "s": "<:greys:940133832986857522>",
        "t": "<:greyt:940133833171423242>",
        "u": "<:greyu:940133832991051786>",
        "v": "<:greyv:940133832840060950>",
        "w": "<:greyw:940133832865251378>",
        "x": "<:greyx:940133832852647956>",
        "y": "<:greyy:940133832940728411>",
        "z": "<:greyz:940133832844255253>",
    },
}


def generate_colored_word(guess: str, answer: str) -> str:
    """
    Builds a string of emoji codes where each letter is
    colored based on the key:
    - Same letter, same place: Green
    - Same letter, different place: Yellow
    - Different letter: Gray

    Args:
        word (str): The word to be colored
        answer (str): The answer to the word

    Returns:
        str: A string of emoji codes
    """
    colored_word = [EMOJI_CODES["gray"][letter] for letter in guess]
    guess_letters = list(guess)
    answer_letters = list(answer)
    # change colors to green if same letter and same place
    for i in range(len(guess_letters)):
        if guess_letters[i] == answer_letters[i]:
            colored_word[i] = EMOJI_CODES["green"][guess_letters[i]]
            answer_letters[i] = None
            guess_letters[i] = None
    # change colors to yellow if same letter and not the same place
    for i in range(len(guess_letters)):
        if guess_letters[i] is not None and guess_letters[i] in answer_letters:
            colored_word[i] = EMOJI_CODES["yellow"][guess_letters[i]]
            answer_letters[answer_letters.index(guess_letters[i])] = None
    return "".join(colored_word)


def generate_blanks() -> str:
    """
    Generate a string of 5 blank white square emoji characters

    Returns:
        str: A string of white square emojis
    """
    return "\N{WHITE MEDIUM SQUARE}" * 5


def generate_puzzle_embed(user: nextcord.User, puzzle_id: int) -> nextcord.Embed:
    """
    Generate an embed for a new puzzle given the puzzle id and user

    Args:
        user (nextcord.User): The user who submitted the puzzle
        puzzle_id (int): The puzzle ID

    Returns:
        nextcord.Embed: The embed to be sent
    """
    embed = nextcord.Embed(title="Wordle Clone")
    embed.description = "\n".join([generate_blanks()] * 6)
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    embed.set_footer(
        text=f"ID: {puzzle_id} ︱ To play, use the command /play!\n"
        "To guess, reply to this message with a word."
    )
    return embed


def update_embed(embed: nextcord.Embed, guess: str) -> nextcord.Embed:
    """
    Updates the embed with the new guesses

    Args:
        embed (nextcord.Embed): The embed to be updated
        puzzle_id (int): The puzzle ID
        guess (str): The guess made by the user

    Returns:
        nextcord.Embed: The updated embed
    """
    puzzle_id = int(embed.footer.text.split()[1])
    answer = popular_words[puzzle_id]
    colored_word = generate_colored_word(guess, answer)
    empty_slot = generate_blanks()
    # replace the first blank with the colored word
    embed.description = embed.description.replace(empty_slot, colored_word, 1)
    # check for game over
    num_empty_slots = embed.description.count(empty_slot)
    if guess == answer:
        if num_empty_slots == 0:
            embed.description += "\n\nPhew!"
        if num_empty_slots == 1:
            embed.description += "\n\nGreat!"
        if num_empty_slots == 2:
            embed.description += "\n\nSplendid!"
        if num_empty_slots == 3:
            embed.description += "\n\nImpressive!"
        if num_empty_slots == 4:
            embed.description += "\n\nMagnificent!"
        if num_empty_slots == 5:
            embed.description += "\n\nGenius!"
    elif num_empty_slots == 0:
        embed.description += f"\n\nThe answer was {answer}!"
    return embed


def is_valid_word(word: str) -> bool:
    """
    Validates a word

    Args:
        word (str): The word to validate

    Returns:
        bool: Whether the word is valid
    """
    return word in all_words


def random_puzzle_id() -> int:
    """
    Generates a random puzzle ID

    Returns:
        int: A random puzzle ID
    """
    return random.randint(0, len(popular_words) - 1)


def is_game_over(embed: nextcord.Embed) -> bool:
    """
    Checks if the game is over in the embed

    Args:
        embed (nextcord.Embed): The embed to check

    Returns:
        bool: Whether the game is over
    """
    return "\n\n" in embed.description
