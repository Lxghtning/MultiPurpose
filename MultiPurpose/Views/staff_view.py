import nextcord
from nextcord.ext import commands
from nextcord.ui import View, button

class staffView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None


    @button(label="Approve",style=nextcord.ButtonStyle.green,custom_id="___approve___")
    async def approve_button(self, button, interaction):
        await interaction.message.mentions[0].send(f"**Your CODM application has been approved in {interaction.guild.name}.**")
        await interaction.response.edit_message(f"Approval sent to {interaction.message.mentions[0]}.")

    @button(label="Deny",style=nextcord.ButtonStyle.green,custom_id="___deny___")
    async def approve_button(self, button, interaction):
        await interaction.message.mentions[0].send(f"**Your CODM application has been denied in {interaction.guild.name}.**")
        await interaction.response.edit_message(f"Approval sent to {interaction.message.mentions[0]}.")

    

