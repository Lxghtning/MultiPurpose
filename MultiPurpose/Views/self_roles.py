import nextcord
from nextcord.ext import commands

class Verify_View(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @nextcord.ui.button(label="Community", style = nextcord.ButtonStyle.green, custom_id = "________verify_________")
    async def __Verify__(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        role = nextcord.utils.get(interaction.guild.roles, id=832878887095762954)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} has been un-verified successfully!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} has been verified successfully!", ephemeral=True)

    @nextcord.ui.button(label="Valorant", style = nextcord.ButtonStyle.blurple, custom_id = "________valorant_________")
    async def __Valo__(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        role = nextcord.utils.get(interaction.guild.roles, id=832870461233823764)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} The {button.label} role has been removed successfully!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} {button.label} role has been added successfully!", ephemeral=True)

    @nextcord.ui.button(label="CODM", style = nextcord.ButtonStyle.blurple, custom_id = "________CODM_________")
    async def __CODM__(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        role = nextcord.utils.get(interaction.guild.roles, id=832871291836170282)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} The {button.label} role has been removed successfully!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} {button.label} role has been added successfully!", ephemeral=True)

    @nextcord.ui.button(label="BGMI", style = nextcord.ButtonStyle.blurple, custom_id = "________BGMI_________")
    async def __BGMI__(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        role = nextcord.utils.get(interaction.guild.roles, id=832870950298583060)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} The {button.label} role has been removed successfully!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} {button.label} role has been added successfully!", ephemeral=True)

    @nextcord.ui.button(label="CS:GO", style = nextcord.ButtonStyle.blurple, custom_id = "________CS:GO_________")
    async def __CSGO__(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        role = nextcord.utils.get(interaction.guild.roles, id=864516899118907413)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} The {button.label} role has been removed successfully!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} {button.label} role has been added successfully!", ephemeral=True)

    @nextcord.ui.button(label="APEXM", style = nextcord.ButtonStyle.blurple, custom_id = "________APEXM_________")
    async def __APEXM__(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        role = nextcord.utils.get(interaction.guild.roles, id=963010427774718033)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} The {button.label} role has been removed successfully!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} {button.label} role has been added successfully!", ephemeral=True)


class NFT_roles(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @nextcord.ui.button(label="NFT Elite", style = nextcord.ButtonStyle.green, custom_id = "________NFTE_________")
    async def __NFTE__(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        role = nextcord.utils.get(interaction.guild.roles, id=938537695578325003)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} has been un-verified successfully!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} has been verified successfully!", ephemeral=True)

    @nextcord.ui.button(label="NFT Veteran", style = nextcord.ButtonStyle.blurple, custom_id = "________NFTV________")
    async def __NFTV__(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        role = nextcord.utils.get(interaction.guild.roles, id=938537545082474536)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} The {button.label} role has been removed successfully!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} {button.label} role has been added successfully!", ephemeral=True)

    @nextcord.ui.button(label="NFT Rookie", style = nextcord.ButtonStyle.blurple, custom_id = "________NFT Rookie_________")
    async def __NFTR__(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        role = nextcord.utils.get(interaction.guild.roles, id=938537297228480532)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} The {button.label} role has been removed successfully!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} {button.label} role has been added successfully!", ephemeral=True)

    @nextcord.ui.button(label="NFT Game Enthusiasts", style = nextcord.ButtonStyle.blurple, custom_id = "________NFT Game Enthusiasts_________")
    async def __NFTGE__(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        role = nextcord.utils.get(interaction.guild.roles, id=938495191126540309)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} The {button.label} role has been removed successfully!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"<a:blue_verify_tick:965628257829552138> {interaction.user.mention} {button.label} role has been added successfully!", ephemeral=True)

    
    