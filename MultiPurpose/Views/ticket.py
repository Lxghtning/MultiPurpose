import nextcord
from nextcord.ext import commands
import io
import chat_exporter

class Close(nextcord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.value = None

    @nextcord.ui.button(label = "Close", style=nextcord.ButtonStyle.primary,custom_id="Clyoosodveee")
    async def tClayddose(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        messages = await interaction.channel.history(limit=1, oldest_first=True).flatten()
        a = messages[0].mentions
        user = a[0]
        await interaction.channel.set_permissions(user, view_channel = False)
        await interaction.response.send_message(f"Ticket closed by {interaction.user.name}#{interaction.user.discriminator}")
        self.value=True

    @nextcord.ui.button(label = "Delete", style=nextcord.ButtonStyle.red,custom_id="Clogdosoevvvvee")
    async def tCdddlaose(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.guild_permissions.manage_messages:
            await interaction.channel.delete()
        elif interaction.user.guild_permissions.manage_messages is not True:
            await interaction.channel.send(f"You do not have Manage Messages Permissions to Close this channel! {interaction.user.mention}", delete_after = 5)

        self.value=True
        


    @nextcord.ui.button(label = "Transcript", style=nextcord.ButtonStyle.primary ,custom_id="Cloosoueee")
    async def tfCalose(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel
        if interaction.user.guild_permissions.manage_messages:
            limit=None
            tz_info = "Asia/Kolkata"
            transcript = await chat_exporter.export(interaction.channel, limit, tz_info, interaction.guild)



            transcript_file = nextcord.File(io.BytesIO(transcript.encode()),
                                        filename=f"transcript-{interaction.channel.name}.html")
            await interaction.response.send_message("Enter the channel ID where the transcript will be sent!")
            msg = await self.bot.wait_for('message',check=check) 
            channel = int(msg.content)        
            try:
                await channel.send(file=transcript_file)
            except:
                await interaction.channel.send("Wrong Channel ID provided!")
        elif interaction.user.guild_permissions.manage_messages is not True:
            await interaction.channel.send("You do not have Manage Messages Permissions to Close this channel!", ephemeral=True)

        self.value=True

class Help_Desk(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label = "RECRUITMENT", style=nextcord.ButtonStyle.green, custom_id="______req______")
    async def recruiment_button_view(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.bot:
            return
        else:
            categ = nextcord.utils.get(interaction.guild.categories, id=844118367076876298)
            await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True)
            ticket_channel = await categ.create_text_channel(name=f"{button.label}ticket-{interaction.user.name}#{interaction.user.discriminator}")
            embed=nextcord.Embed(description=f"<#{ticket_channel.id}> - Your ticket has been created")
            await interaction.edit_original_message(embed=embed)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            view=Close()
            await ticket_channel.send(f"{interaction.user.mention}")
            embed = nextcord.Embed(title=f"Support Needed!", description=f"A ticket opened by **{interaction.user.name}**,\n Server Display name is **{interaction.user.display_name}**\n Support will be with you soon!\, Please describe your problem in the chat!\n The **Close button** can only be used by staffs with manage messages perms!", color=0xFF0000 )
            await ticket_channel.send(embed=embed, view=view)

    @nextcord.ui.button(label = "GENERAL QUERY ", style=nextcord.ButtonStyle.gray, custom_id="______gq______")
    async def gq_view(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.bot:
            return
        else:
            categ = nextcord.utils.get(interaction.guild.categories, id=844118367076876298)
            await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True)
            ticket_channel = await categ.create_text_channel(name=f"{button.label}ticket-{interaction.user.name}#{interaction.user.discriminator}")
            embed=nextcord.Embed(description=f"<#{ticket_channel.id}> - Your ticket has been created")
            await interaction.edit_original_message(embed=embed)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            view=Close()
            await ticket_channel.send(f"{interaction.user.mention}")
            embed = nextcord.Embed(title=f"Support Needed!", description=f"A ticket opened by **{interaction.user.name}**,\n Server Display name is **{interaction.user.display_name}**\n Support will be with you soon!\, Please describe your problem in the chat!\n The **Close button** can only be used by staffs with manage messages perms!", color=0xFF0000 )
            await ticket_channel.send(embed=embed, view=view)

    @nextcord.ui.button(label = "SERVER RELATED QUERY ", style=nextcord.ButtonStyle.blurple, custom_id="______srq______")
    async def srq_view(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.bot:
            return
        else:
            categ = nextcord.utils.get(interaction.guild.categories, id=844118367076876298)
            await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True)
            ticket_channel = await categ.create_text_channel(name=f"{button.label}ticket-{interaction.user.name}#{interaction.user.discriminator}")
            embed=nextcord.Embed(description=f"<#{ticket_channel.id}> - Your ticket has been created")
            await interaction.edit_original_message(embed=embed)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            view=Close()
            await ticket_channel.send(f"{interaction.user.mention}")
            embed = nextcord.Embed(title=f"Support Needed!", description=f"A ticket opened by **{interaction.user.name}**,\n Server Display name is **{interaction.user.display_name}**\n Support will be with you soon!\, Please describe your problem in the chat!\n The **Close button** can only be used by staffs with manage messages perms!", color=0xFF0000 )
            await ticket_channel.send(embed=embed, view=view)

    @nextcord.ui.button(label = "HELP", style=nextcord.ButtonStyle.red, custom_id="______help______")
    async def help_view(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.bot:
            return
        else:
            categ = nextcord.utils.get(interaction.guild.categories, id=844118367076876298)
            await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True)
            ticket_channel = await categ.create_text_channel(name=f"{button.label}ticket-{interaction.user.name}#{interaction.user.discriminator}")
            embed=nextcord.Embed(description=f"<#{ticket_channel.id}> - Your ticket has been created")
            await interaction.edit_original_message(embed=embed)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            view=Close()
            await ticket_channel.send(f"{interaction.user.mention}")
            embed = nextcord.Embed(title=f"Support Needed!", description=f"A ticket opened by **{interaction.user.name}**,\n Server Display name is **{interaction.user.display_name}**\n Support will be with you soon!\, Please describe your problem in the chat!\n The **Close button** can only be used by staffs with manage messages perms!", color=0xFF0000 )
            await ticket_channel.send(embed=embed, view=view)

class Req_Desk(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label = "CODM", style=nextcord.ButtonStyle.green, custom_id="______CODM______")
    async def CODM_view(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.bot:
            return
        else:
            categ = nextcord.utils.get(interaction.guild.categories, id=842376353453441054)
            await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True)
            ticket_channel = await categ.create_text_channel(name=f"{button.label}ticket-{interaction.user.name}#{interaction.user.discriminator}")
            embed=nextcord.Embed(description=f"<#{ticket_channel.id}> - Your ticket has been created")
            await interaction.edit_original_message(embed=embed)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            view=Close()
            await ticket_channel.send(f"{interaction.user.mention}")
            embed = nextcord.Embed(title=f"Support Needed!", description=f"A ticket opened by **{interaction.user.name}**,\n Server Display name is **{interaction.user.display_name}**\n Support will be with you soon!\, Please describe your problem in the chat!\n The **Close button** can only be used by staffs with manage messages perms!", color=0xFF0000 )
            await ticket_channel.send(embed=embed, view=view)

    @nextcord.ui.button(label = "BGMI", style=nextcord.ButtonStyle.gray, custom_id="______BGMI______")
    async def BGMI_view(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.bot:
            return
        else:
            categ = nextcord.utils.get(interaction.guild.categories, id=910850952460926976)
            await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True)
            ticket_channel = await categ.create_text_channel(name=f"{button.label}ticket-{interaction.user.name}#{interaction.user.discriminator}")
            embed=nextcord.Embed(description=f"<#{ticket_channel.id}> - Your ticket has been created")
            await interaction.edit_original_message(embed=embed)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            view=Close()
            await ticket_channel.send(f"{interaction.user.mention}")
            embed = nextcord.Embed(title=f"Support Needed!", description=f"A ticket opened by **{interaction.user.name}**,\n Server Display name is **{interaction.user.display_name}**\n Support will be with you soon!\, Please describe your problem in the chat!\n The **Close button** can only be used by staffs with manage messages perms!", color=0xFF0000 )
            await ticket_channel.send(embed=embed, view=view)

    @nextcord.ui.button(label = "VALORANT ", style=nextcord.ButtonStyle.blurple, custom_id="______VALORANT ______")
    async def VALORANT_view(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.bot:
            return
        else:
            categ = nextcord.utils.get(interaction.guild.categories, id=910851199375396886)
            await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True)
            ticket_channel = await categ.create_text_channel(name=f"{button.label}ticket-{interaction.user.name}#{interaction.user.discriminator}")
            embed=nextcord.Embed(description=f"<#{ticket_channel.id}> - Your ticket has been created")
            await interaction.edit_original_message(embed=embed)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            view=Close()
            await ticket_channel.send(f"{interaction.user.mention}")
            embed = nextcord.Embed(title=f"Support Needed!", description=f"A ticket opened by **{interaction.user.name}**,\n Server Display name is **{interaction.user.display_name}**\n Support will be with you soon!\, Please describe your problem in the chat!\n The **Close button** can only be used by staffs with manage messages perms!", color=0xFF0000 )
            await ticket_channel.send(embed=embed, view=view)

    @nextcord.ui.button(label = "MANAGEMENT", style=nextcord.ButtonStyle.red, custom_id="______MANAGEMENT______")
    async def MANAGEMENT_view(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.bot:
            return
        else:
            categ = nextcord.utils.get(interaction.guild.categories, id=844118367076876298)
            await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True)
            ticket_channel = await categ.create_text_channel(name=f"{button.label}ticket-{interaction.user.name}#{interaction.user.discriminator}")
            embed=nextcord.Embed(description=f"<#{ticket_channel.id}> - Your ticket has been created")
            await interaction.edit_original_message(embed=embed)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            view=Close()
            await ticket_channel.send(f"{interaction.user.mention}")
            embed = nextcord.Embed(title=f"Support Needed!", description=f"A ticket opened by **{interaction.user.name}**,\n Server Display name is **{interaction.user.display_name}**\n Support will be with you soon!\, Please describe your problem in the chat!\n The **Close button** can only be used by staffs with manage messages perms!", color=0xFF0000 )
            await ticket_channel.send(embed=embed, view=view)

class NFT_Desk(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label = "NFT GAMES", style=nextcord.ButtonStyle.green, custom_id="______NFT GAMES______")
    async def NFT_GAMES_view(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.bot:
            return
        else:
            categ = nextcord.utils.get(interaction.guild.categories, id=938454899753095238)
            await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True)
            ticket_channel = await categ.create_text_channel(name=f"{button.label}ticket-{interaction.user.name}#{interaction.user.discriminator}")
            embed=nextcord.Embed(description=f"<#{ticket_channel.id}> - Your ticket has been created")
            await interaction.edit_original_message(embed=embed)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            view=Close()
            await ticket_channel.send(f"{interaction.user.mention}")
            embed = nextcord.Embed(title=f"Support Needed!", description=f"A ticket opened by **{interaction.user.name}**,\n Server Display name is **{interaction.user.display_name}**\n Support will be with you soon!\, Please describe your problem in the chat!\n The **Close button** can only be used by staffs with manage messages perms!", color=0xFF0000 )
            await ticket_channel.send(embed=embed, view=view)

    @nextcord.ui.button(label = "NFT COLLECTIBLES", style=nextcord.ButtonStyle.gray, custom_id="______NFT COLLECTIBLES______")
    async def NFT_COLLECTIBLES_view(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.bot:
            return
        else:
            categ = nextcord.utils.get(interaction.guild.categories, id=938454899753095238)
            await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True)
            ticket_channel = await categ.create_text_channel(name=f"{button.label}ticket-{interaction.user.name}#{interaction.user.discriminator}")
            embed=nextcord.Embed(description=f"<#{ticket_channel.id}> - Your ticket has been created")
            await interaction.edit_original_message(embed=embed)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            view=Close()
            await ticket_channel.send(f"{interaction.user.mention}")
            embed = nextcord.Embed(title=f"Support Needed!", description=f"A ticket opened by **{interaction.user.name}**,\n Server Display name is **{interaction.user.display_name}**\n Support will be with you soon!\, Please describe your problem in the chat!\n The **Close button** can only be used by staffs with manage messages perms!", color=0xFF0000 )
            await ticket_channel.send(embed=embed, view=view)

    @nextcord.ui.button(label = "CRYPTO", style=nextcord.ButtonStyle.blurple, custom_id="______CRYPTO ______")
    async def CRYPTO_view(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.bot:
            return
        else:
            categ = nextcord.utils.get(interaction.guild.categories, id=938454899753095238)
            await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True)
            ticket_channel = await categ.create_text_channel(name=f"{button.label}ticket-{interaction.user.name}#{interaction.user.discriminator}")
            embed=nextcord.Embed(description=f"<#{ticket_channel.id}> - Your ticket has been created")
            await interaction.edit_original_message(embed=embed)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            view=Close()
            await ticket_channel.send(f"{interaction.user.mention}")
            embed = nextcord.Embed(title=f"Support Needed!", description=f"A ticket opened by **{interaction.user.name}**,\n Server Display name is **{interaction.user.display_name}**\n Support will be with you soon!\, Please describe your problem in the chat!\n The **Close button** can only be used by staffs with manage messages perms!", color=0xFF0000 )
            await ticket_channel.send(embed=embed, view=view)

    @nextcord.ui.button(label = "METAVERSE", style=nextcord.ButtonStyle.red, custom_id="______METAVERSE______")
    async def METAVERSE_view(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.bot:
            return
        else:
            categ = nextcord.utils.get(interaction.guild.categories, id=938454899753095238)
            await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True)
            ticket_channel = await categ.create_text_channel(name=f"{button.label}ticket-{interaction.user.name}#{interaction.user.discriminator}")
            embed=nextcord.Embed(description=f"<#{ticket_channel.id}> - Your ticket has been created")
            await interaction.edit_original_message(embed=embed)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            view=Close()
            await ticket_channel.send(f"{interaction.user.mention}")
            embed = nextcord.Embed(title=f"Support Needed!", description=f"A ticket opened by **{interaction.user.name}**,\n Server Display name is **{interaction.user.display_name}**\n Support will be with you soon!\, Please describe your problem in the chat!\n The **Close button** can only be used by staffs with manage messages perms!", color=0xFF0000 )
            await ticket_channel.send(embed=embed, view=view)