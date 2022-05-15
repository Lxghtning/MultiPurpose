import nextcord
import random
import numpy as np
from nextcord import Embed

class path1lightning(nextcord.ui.View):
    def __init__(self, db):
        super().__init__()
        self.db = db

    @nextcord.ui.button(label='Kick', style=nextcord.ButtonStyle.primary)
    async def lynxdefaultkick(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        cursor = await self.db.cursor()
        await cursor.execute("SELECT level FROM userlevel WHERE user_id=?",(interaction.user.id,))
        level = await cursor.fetchone()
        hp = random.randint(1,int(level[0] + 20))    
        if level[0] == 0:
            p=[0.5,0.5]
        elif level <= 5 and level != 0:
            p = [0.45,0.55]
        elif level <= 10 and level > 5:
            p = [0.3,0.7]
        else:
            p = [0.9,0.1]
        a = np.random.choices(["yes","no"],p=p)
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
            embed = Embed(title="Soldier",description=f"\n\n```Lost```\n\n")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed,view=self)
            
        elif hp_data[1] <= 0:
            button.label = "won"
            button.style  = nextcord.ButtonStyle.green
            button.disabled = True
            await cursor.execute("DELETE FROM hp WHERE user_id = ?",(interaction.user.id,))
            await self.db.commit()
            embed = Embed(title="Lynx Fight",description=f"\n\n```Won```\n\n")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed,view=self)
           
        else:

            userhp = hp_data[2]     
            bosshp = hp_data[1]
            embed = Embed(title="Soldier",description=f"\n```Fight against Lynx```\n\n",color=self.COLOUR)
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            embed.add_field(name=f"{interaction.author.name}#{interaction.author.discriminator}",value=f"{userhp}")
            embed.add_field(name=f"Lynx Soldier",value=f"{bosshp}")
            # Make sure to update the message with our updated selves
            await interaction.response.edit_message(embed=embed,view=self)

    @nextcord.ui.button(label='punch', style=nextcord.ButtonStyle.primary)
    async def lynxdefaultpunch(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        cursor = await self.db.cursor()
        await cursor.execute("SELECT level FROM userlevel WHERE user_id=?",(interaction.user.id,))
        level = await cursor.fetchone()
        hp = random.randint(1,int(level[0] + 20))    
        if level[0] == 0:
            p=[0.5,0.5]
        elif level <= 5 and level != 0:
            p = [0.45,0.55]
        elif level <= 10 and level > 5:
            p = [0.3,0.7]
        else:
            p = [0.9,0.1]
        a = np.random.choices(["yes","no"],p=p)
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
            embed = Embed(title="Soldier",description=f"\n\n```Lost```\n\n")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed,view=self)
            
        elif hp_data[1] <= 0:
            button.label = "won"
            button.style  = nextcord.ButtonStyle.green
            button.disabled = True
            await cursor.execute("DELETE FROM hp WHERE user_id = ?",(interaction.user.id,))
            await self.db.commit()
            embed = Embed(title="Lynx Fight",description=f"\n\n```Won```\n\n")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed,view=self)
           
        else:

            userhp = hp_data[2]     
            bosshp = hp_data[1]
            embed = Embed(title="Soldier",description=f"\n```Fight against Lynx```\n\n",color=self.COLOUR)
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            embed.add_field(name=f"{interaction.author.name}#{interaction.author.discriminator}",value=f"{userhp}")
            embed.add_field(name=f"Lynx Soldier",value=f"{bosshp}")
            # Make sure to update the message with our updated selves
            await interaction.response.edit_message(embed=embed,view=self)