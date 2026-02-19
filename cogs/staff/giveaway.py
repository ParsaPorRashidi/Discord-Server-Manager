import random

import discord
from discord import ui
from discord.ext import commands


class GiveawaySetupModal(ui.Modal, title='Setup Your Giveaway'):
    g_title = ui.TextInput(label='Giveaway Title', placeholder='e.g. Nitro Full', required=True)
    g_desc = ui.TextInput(label='Description', style=discord.TextStyle.paragraph, required=True)

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        try:
            logo = discord.File('images/uni.png', filename='uni.png')
            layout = GiveawayLayout(self.cog, self.g_title.value, self.g_desc.value)
            await interaction.response.send_message(view=layout, file=logo)
        except FileNotFoundError:
            layout = GiveawayLayout(self.cog, self.g_title.value, self.g_desc.value)
            await interaction.response.send_message(content="⚠️ Logo file not found, sending without icon.", view=layout)


class GiveawayLayout(ui.LayoutView):
    def __init__(self, cog, title, desc):
        super().__init__(timeout=None)
        self.cog = cog
        self.title_val = title
        self.desc_val = desc
        self.build_layout()

    def build_layout(self):
        self.clear_items()
        container = ui.Container(accent_color=0xa71ee4)

        icon = ui.Thumbnail('attachment://uni.png')

        header = ui.Section(
            ui.TextDisplay(f'# 🎉 {self.title_val} 🎉'),
            ui.TextDisplay(f'{self.desc_val}'),
            accessory=icon
        )
        container.add_item(header)
        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.small))

        mentions = [f"<@{uid}>" for uid in self.cog.participants]
        participants_list = "\n".join(mentions) if mentions else "No one has joined yet."

        container.add_item(ui.TextDisplay(f'## 🎟️ Participants'))
        container.add_item(ui.TextDisplay(participants_list))

        join_btn = ui.Button(label="Join/Leave", style=discord.ButtonStyle.green)
        join_btn.callback = self.join_leave

        draw_btn = ui.Button(label="Draw Winner", style=discord.ButtonStyle.red)
        draw_btn.callback = self.draw_winner

        action_row = ui.ActionRow(join_btn, draw_btn)
        container.add_item(action_row)
        self.add_item(container)

    async def join_leave(self, interaction: discord.Interaction):
        if interaction.user.id in self.cog.participants:
            self.cog.participants.remove(interaction.user.id)
            await interaction.response.send_message("❌ Removed from giveaway.", ephemeral=True)
        else:
            self.cog.participants.append(interaction.user.id)
            await interaction.response.send_message("✅ Joined successfully!", ephemeral=True)

        self.build_layout()
        await interaction.message.edit(view=self)

    async def draw_winner(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("Admins only!", ephemeral=True)

        if not self.cog.participants:
            return await interaction.response.send_message("No one joined!", ephemeral=True)

        winner_id = random.choice(self.cog.participants)
        winner = await self.cog.bot.fetch_user(winner_id)

        await interaction.channel.send(f"🎊 **Winner:** {winner.mention}! Prize: **{self.title_val}**")
        self.cog.participants.clear()

        self.clear_items()
        closed_cont = ui.Container(accent_color=discord.Color.dark_gray())
        closed_cont.add_item(
            ui.TextDisplay(f"# 🏁 Giveaway Closed\nPrize: {self.title_val}\nWinner: {winner.display_name}"))
        self.add_item(closed_cont)
        await interaction.message.edit(view=self)


class GiveAway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.participants = []

    class SetupView(ui.View):
        def __init__(self, cog):
            super().__init__(timeout=None)
            self.cog = cog

        @ui.button(label="Setup Giveaway", style=discord.ButtonStyle.blurple)
        async def open_modal(self, interaction: discord.Interaction, button: ui.Button):
            await interaction.response.send_modal(GiveawaySetupModal(self.cog))

    @commands.command(name="giveaway")
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx):
        view = self.SetupView(self)
        await ctx.send("Click to configure details:", view=view)


async def setup(bot):
    await bot.add_cog(GiveAway(bot))