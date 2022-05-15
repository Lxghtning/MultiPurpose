import nextcord
import random
from nextcord import Embed

class Battle(nextcord.ui.View):
    def __init__(self, db):
        super().__init__()
        self.db = db

    @nextcord.ui.button(label='0', style=nextcord.ButtonStyle.primary)
    async def count(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        number = int(button.label) if button.label else 0
        
        cursor = await self.db.cursor()
        await cursor.execute("SELECT level FROM userlevel WHERE user_id=?",(interaction.user.id,))
        level = await cursor.fetchone()
        hp = random.randint(1,int(level[0] + 20))    
        a = random.choices(["yes","no"])
        if a[0] == "yes":
            await cursor.execute("UPDATE hp SET user_hp = user_hp - ? WHERE user_id = ?",(hp,interaction.user.id))
            await self.db.commit()
        else:
            await cursor.execute("UPDATE hp SET boss_hp = boss_hp - ? WHERE user_id = ?",(hp,interaction.user.id))
            await self.db.commit()

        await cursor.execute("SELECT * FROM hp WHERE user_id = ?",(interaction.user.id,))
        hp_data = await cursor.fetchone()
        if hp_data[2] <= 0:
            button.label = "Lose"
            button.disabled = True
            await cursor.execute("DELETE FROM hp WHERE user_id = ?",(interaction.user.id,))
            await self.db.commit()
            embed = Embed(title="Boss Fight",description=f"\n```Lost```\n\n")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed,view=self)
            
        elif hp_data[1] <= 0:
            button.label = "won"
            button.style  = nextcord.ButtonStyle.green
            button.disabled = True
            await cursor.execute("DELETE FROM hp WHERE user_id = ?",(interaction.user.id,))
            await self.db.commit()
            embed = Embed(title="Boss Fight",description=f"\n```won```\n\n")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed,view=self)
           
        else:
            button.label = str(number + 1)
            userhp = hp_data[2]     
            bosshp = hp_data[1]
            embed = Embed(title="Boss Fight",description=f"\n```Level 10 Boss fight```\n\n")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            embed.add_field(name=f"{interaction.user.name}#{interaction.user.discriminator}",value=f"{userhp}")
            embed.add_field(name=f"Naruto Boss",value=f"{bosshp}")
            # Make sure to update the message with our updated selves
            await interaction.response.edit_message(embed=embed,view=self)
