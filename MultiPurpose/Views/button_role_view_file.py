import nextcord
from Self_Roles_Folder.button_roles_pyfile import Button_Dict

class ButtonRoleView_VIEW(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    break_out = False
    async def role_add_or_remove_callback(self, interaction):
                for role in Button_Dict.keys():
                    if break_out:
                        print("j")
                        break
                                       
                    else:
                        for buttons in self.children:
                            if buttons.label == role:
                                role_to_be_added_or_removed = nextcord.utils.get(interaction.guild.roles, id=Button_Dict[role].value())
                                if role_to_be_added_or_removed in interaction.user.roles:
                                    await interaction.user.remove_roles(role_to_be_added_or_removed)
                                    await interaction.response.send_message(f"Successfully removed {buttons.label} role from you.",ephemeral=True)
                                    break_out = True
                                    break
                                else:
                                    await interaction.user.add_roles(role_to_be_added_or_removed)
                                    await interaction.response.send_message(f"Successfully added {buttons.label} role to you.",ephemeral=True)
                                    break_out=True
                                    break
    
    # @nextcord.ui.button(label='0', style=nextcord.ButtonStyle.primary)
    # async def count(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):