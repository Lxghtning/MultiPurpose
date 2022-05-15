import nextcord 
from nextcord import Embed
from nextcord.ext import commands
import random
import numpy
from datetime import datetime 



# :brown_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::brown_square:
# :brown_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::brown_square:
# :brown_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::brown_square:
# :brown_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::brown_square:
# :brown_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::brown_square:
# :brown_square:                                                                                                  :brown_square: 
# :brown_square:                                                                                                  :brown_square: 
# :brown_square:                                                                                                  :brown_square:
# :brown_square:                                                                                                  :brown_square:
# :brown_square:                                                                                                  :brown_square:  


# :blue_circle::blue_circle::blue_circle::blue_circle:
# :blue_circle::blue_circle::blue_circle::blue_circle:
# :blue_circle::blue_circle::blue_circle::blue_circle:
# :blue_circle::blue_circle::blue_circle::blue_circle:
#           :blue_circle:
#           :blue_circle:
#           :blue_circle:
#           :blue_circle:
#           :blue_circle:
#           :blue_circle:
#           :blue_circle:


# ㅤㅤㅤㅤ:red_circle::red_circle:
#                   :red_circle::red_circle: 
#                   :white_circle::white_circle:
#                :white_circle::white_circle::white_circle:
#             :white_circle::white_circle::white_circle::white_circle:
#           :white_circle::white_circle::white_circle::white_circle::white_circle:

# :black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:
# :black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:
# :black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:
# :black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:
#             :black_large_square:                  :black_large_square:
#             :black_large_square:                  :black_large_square:
# :black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:  
# :black_large_square:       :black_large_square:  
# :black_large_square:       :black_large_square:
# :black_large_square:       :black_large_square:
#              :black_large_square:
#              :black_large_square:
#              :black_large_square:
#         :black_large_square::black_large_square::black_large_square:
#         :black_large_square:       :black_large_square:
#         :black_large_square:       :black_large_square:
#         :black_large_square:       :black_large_square:


options = ["smash","defend-smash","lift","net-short","normal","between-the-legs"]
choice = ["not-out","outside"]

class Badminton(nextcord.ui.View):
    def __int__(self):
        super().__int__()

    @nextcord.ui.button(emoji="🏸", style=nextcord.ButtonStyle.primary,custom_id="smash")
    async def smash(self,button,interaction):
        choice = random.choices(options)
        if choice[0] == "smash":
            embed = Embed(description=f"You won {interaction.user.mention}")
            await interaction.response.edit_message(embed=embed)
            self.stop()
        else:
            await interaction.response.edit_message(f"choice  was {choice[0]}")
        