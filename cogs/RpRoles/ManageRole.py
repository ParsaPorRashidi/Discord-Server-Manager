import asyncio

import discord
from discord import ui
from discord.ext import commands

from config import ADMIN_ROLES, HOSPITAL_ROLES

ADMIN_ROLES = ADMIN_ROLES
HOSPITAL_ROLES = HOSPITAL_ROLES

class MemberIDModal(ui.Modal, title='Staff Registration Form'):
    user_id = ui.TextInput(
        label='Member Discord ID',
        placeholder='e.g. 123456789012345678',
        min_length=17, max_length=20, required=True
    )

    def __init__(self, role_id, role_name):
        super().__init__()
        self.role_id = role_id
        self.role_name = role_name

    async def on_submit(self, interaction: discord.Interaction):
        try:
            target_member = await interaction.guild.fetch_member(int(self.user_id.value))
            role = interaction.guild.get_role(self.role_id)

            if not role:
                return await interaction.response.send_message("❌ **Error:** Role ID is invalid.", ephemeral=True)

            await target_member.add_roles(role)

            embed = discord.Embed(
                title="📋 Staff Assignment Log",
                description=(
                    f"> **Action:** New Role Assigned\n"
                    f"> **Target:** {target_member.mention}\n"
                    f"> **Position:** `{self.role_name}`\n"
                    f"> **Authorized by:** {interaction.user.mention}"
                ),
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow()
            )
            embed.set_footer(text="Hospital HR Management System")

            await interaction.response.send_message(embed=embed)
            await asyncio.sleep(10)
            await interaction.delete_original_response()

        except Exception as e:
            await interaction.response.send_message(f"❌ **System Error:** {e}", ephemeral=True)


class RoleManagementLayout(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=180)
        self.build_layout()

    def build_layout(self):
        container = ui.Container(accent_color=0xa71ee4)

        container.add_item(ui.TextDisplay("# 🏥 Medical Personnel Administration"))
        container.add_item(ui.TextDisplay(
            "Welcome to the **Central Hospital Management Interface**. This panel is strictly for authorized "
            "personnel (HR/Chiefs) to update staff registries and hierarchy positions."
        ))

        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.small))

        container.add_item(ui.TextDisplay(
            "### 🛠️ Instructions:\n"
            "1. Select the target rank from the dropdown menu below.\n"
            "2. Enter the valid **Discord User ID** of the staff member.\n"
            "3. The system will automatically log the change and update roles."
        ))

        options = []
        for name, (r_id, desc) in HOSPITAL_ROLES.items():
            options.append(discord.SelectOption(label=name, value=str(r_id), description=desc, emoji="💉"))

        select_menu = ui.Select(placeholder="🔍 Search for a medical rank...", options=options)
        select_menu.callback = self.select_callback
        container.add_item(ui.ActionRow(select_menu))

        gallery_item = ui.MediaGallery()
        gallery_item.add_item(media='attachment://Manage.png')
        container.add_item(gallery_item)

        container.add_item(ui.TextDisplay("*Note: All actions are logged and visible to the high command.*"))

        self.add_item(container)

    async def select_callback(self, interaction: discord.Interaction):
        role_id = int(interaction.data['values'][0])
        role_name = [name for name, (i, d) in HOSPITAL_ROLES.items() if i == role_id][0]
        await interaction.response.send_modal(MemberIDModal(role_id, role_name))


class HospitalManager(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="hospital")
    async def hospital_cmd(self, ctx):
        user_role_ids = [role.id for role in ctx.author.roles]
        if not any(r_id in ADMIN_ROLES for r_id in user_role_ids):
            return await ctx.send("⚠️ **Unauthorized:** Access denied to HR database.", delete_after=5)

        try:
            file = discord.File("images/Manage.png", filename="Manage.png")
            view = RoleManagementLayout()
            await ctx.send(view=view, file=file)
        except FileNotFoundError:
            view = RoleManagementLayout()
            await ctx.send("📂 **System Alert:** Interface background missing.", view=view)

async def setup(client):
    await client.add_cog(HospitalManager(client))