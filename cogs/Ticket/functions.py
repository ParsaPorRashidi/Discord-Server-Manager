import datetime
import os

import discord
from discord import ui

from config import STAFF_ROLE_ID, TICKET_CATEGORY_ID, TICKET_LOG_DIR

STAFF_ROLE_ID = STAFF_ROLE_ID
TICKET_CATEGORY_ID = TICKET_CATEGORY_ID
TICKET_LOG_DIR = TICKET_LOG_DIR

os.makedirs(TICKET_LOG_DIR, exist_ok=True)

def generate_ticket_number() -> str:
    return str(int(datetime.datetime.now().timestamp() * 1000))[-8:]

async def get_or_create_category(guild: discord.Guild) -> discord.CategoryChannel:
    if TICKET_CATEGORY_ID:
        category = guild.get_channel(TICKET_CATEGORY_ID)
        if category:
            return category
    category = discord.utils.get(guild.categories, name="Tickets")
    if not category:
        category = await guild.create_category("Tickets")
    return category

def log_ticket_creation(ticket_number: str, user: discord.User, category: str, channel_id: int):
    log_path = os.path.join(TICKET_LOG_DIR, f"{ticket_number}.txt")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"Ticket Number: {ticket_number}\n")
        f.write(f"User: {user} (ID: {user.id})\n")
        f.write(f"Category: {category}\n")
        f.write(f"Channel ID: {channel_id}\n")
        f.write(f"Created at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 50 + "\n")

class TicketView(ui.View):
    def __init__(self, ticket_number: str):
        super().__init__(timeout=None)
        self.ticket_number = ticket_number

    @ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="🔒")
    async def close_ticket(self, interaction: discord.Interaction, button: ui.Button):
        if not (interaction.user.guild_permissions.manage_channels or
                any(role.id == STAFF_ROLE_ID for role in interaction.user.roles)):
            await interaction.response.send_message("You do not have permission to close this ticket.", ephemeral=True)
            return

        await interaction.response.send_message("Ticket is being closed...")
        channel = interaction.channel

        log_path = os.path.join(TICKET_LOG_DIR, f"{self.ticket_number}.txt")
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f"\nClosed by: {interaction.user} (ID: {interaction.user.id})\n")
            f.write(f"Closed at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        await channel.delete()

async def create_ticket(interaction: discord.Interaction, category_key: str):
    await interaction.response.defer(ephemeral=True)

    guild = interaction.guild
    user = interaction.user

    category_names = {
        '1': 'Player Report',
        '2': 'Staff Inquiry',
        '3': 'Custom Character',
        'faq': 'FAQ',
        'ban': 'Ban Appeal'
    }
    category_name = category_names.get(category_key, 'General')

    ticket_number = generate_ticket_number()
    channel_name = f"ticket-{ticket_number}"

    category = await get_or_create_category(guild)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    staff_role = guild.get_role(STAFF_ROLE_ID)
    if staff_role:
        overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

    try:
        channel = await category.create_text_channel(
            name=channel_name,
            overwrites=overwrites,
            topic=f"Ticket {ticket_number} - {category_name} - created by {user}"
        )
    except Exception as e:
        await interaction.followup.send(f"Error creating channel: {e}", ephemeral=True)
        return

    embed = discord.Embed(
        title=f"Ticket #{ticket_number}",
        description=f"Category: **{category_name}**\n"
                    f"User: {user.mention}\n"
                    "Please describe your issue in detail. Staff will respond shortly.",
        color=discord.Color.blurple(),
        timestamp=datetime.datetime.now()
    )
    embed.set_footer(text="Use the button below to close this ticket.")

    view = TicketView(ticket_number)
    await channel.send(embed=embed, view=view)

    log_ticket_creation(ticket_number, user, category_name, channel.id)

    await interaction.followup.send(f"✅ Your ticket `{ticket_number}` has been created in {channel.mention}.", ephemeral=True)