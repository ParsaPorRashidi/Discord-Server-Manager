import discord
from discord import ui
from discord.ext import commands

from .functions import create_ticket


class MenuLayout(ui.LayoutView):
    def __init__(self):
        super().__init__()

        container = ui.Container(accent_color=0xa71ee4)
        Blaze_logo = ui.Thumbnail('attachment://logo.png')

        Header = ui.Section(
            ui.TextDisplay('# 💠 Back Blaze Support Center'),
            ui.TextDisplay(
                'Welcome to our official support portal! Please select the department that best matches your inquiry. '
                'Our team is here to help you with any issues you may encounter.'
            ),
            accessory=Blaze_logo
        )
        container.add_item(Header)

        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))

        row1 = ui.TextDisplay('## 🛠️ Main Support Categories')
        row2 = ui.TextDisplay('Choose a topic that best matches your current issue:')
        row1_select = ui.Select(
            placeholder='— Select a Ticket Category —',
            options=[
                discord.SelectOption(label='Player Report', value='1', emoji='🚫', description='Report rule violations, harassment, or cheating.'),
                discord.SelectOption(label='Staff Inquiry', value='2', emoji='👥', description='Questions, feedback, or complaints about staff.'),
                discord.SelectOption(label='Custom Character', value='3', emoji='🎭', description='Apply for or modify a custom character.'),
            ]
        )

        row1_select.callback = self.select_callback

        row3 = ui.ActionRow(row1_select)
        container.add_item(row1)
        container.add_item(row2)
        container.add_item(row3)


        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))

        faq = ui.Button(label='🎫 Open FAQ Ticket', style=discord.ButtonStyle.green)
        faq.callback = self.faq_callback

        row4 = ui.Section(
            ui.TextDisplay('## ❓ General Assistance'),
            accessory=faq
        )
        row5 = ui.TextDisplay(
            'If you are experiencing general issues or have questions not covered by the categories above, '
            'feel free to open a ticket here. Our team will guide you.'
        )

        container.add_item(row4)
        container.add_item(row5)

        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))

        unban = ui.Button(label='🔓 Appeal Ban' ,style=discord.ButtonStyle.red)
        unban.callback = self.ban_callback

        row6 = ui.Section(
            ui.TextDisplay('## ⚖️ Ban Appeal Request'),
            accessory=unban
        )
        row7 = ui.TextDisplay(
            'Submit a request to review your account status and appeal restrictions. '
            'Please include your in-game name and the reason for the appeal.'
        )

        container.add_item(row6)
        container.add_item(row7)

        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))

        row8 = ui.TextDisplay('## ⚠️ Important Guidelines')
        row9 = ui.TextDisplay(
            'Please avoid opening duplicate tickets or spamming the support system. '
            'Be respectful and provide as much detail as possible to help us assist you faster.'
        )

        container.add_item(row8)
        container.add_item(row9)

        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))

        gallery = 'attachment://ticket.png'

        row10 = ui.MediaGallery()
        row10.add_item(media=gallery)

        container.add_item(row10)

        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))

        self.add_item(container)

    async def select_callback(self, interaction: discord.Interaction):
        value = interaction.data['values'][0]
        await create_ticket(interaction, value)

    async def faq_callback(self ,interaction: discord.Interaction):
        await create_ticket(interaction, 'faq')

    async def ban_callback(self ,interaction: discord.Interaction):
        await create_ticket(interaction, 'ban')

class TicketLayout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("TestLayout cog loaded")

    @commands.has_permissions(administrator=True)
    @commands.command(name="ticket")
    async def ticket_command(self, ctx: commands.Context):
        layout = MenuLayout()
        logo = discord.File('images/logo.png', 'logo.png')
        thumbnail = discord.File('images/ticket.png', 'ticket.png')
        await ctx.reply(view=layout, files=[logo, thumbnail])

async def setup(client):
    await client.add_cog(TicketLayout(client))