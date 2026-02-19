import discord
from discord import ui
from discord.ext import commands


class ClearConfirmView(ui.LayoutView):
    def __init__(self, cog, count, author):
        super().__init__(timeout=60)
        self.cog = cog
        self.count = count
        self.author = author
        self.build_layout()

    def build_layout(self):
        # ساخت کانترینر اصلی
        container = ui.Container(accent_color=discord.Color.red())

        # اصلاح: اضافه کردن self قبل از count
        container.add_item(
            ui.TextDisplay(f"# ⚠️ Confirmation\nAre you sure you want to delete **{self.count}** message(s)?")
        )

        # ساخت دکمه تایید
        confirm_btn = ui.Button(label="Confirm & Purge", style=discord.ButtonStyle.danger, emoji="🗑️")
        confirm_btn.callback = self.confirm_callback

        confirm_btn = ui.Button(label="Confirm & Purge", style=discord.ButtonStyle.danger, emoji="🗑️")
        confirm_btn.callback = self.confirm_callback

        cancel_btn = ui.Button(label="Cancel", style=discord.ButtonStyle.secondary)
        cancel_btn.callback = self.cancel_callback

        action_row = ui.ActionRow(confirm_btn, cancel_btn)
        container.add_item(action_row)

        self.add_item(container)

    async def confirm_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            return await interaction.response.send_message("This is not for you!", ephemeral=True)

        await interaction.message.delete()
        await self.cog._clear(interaction.channel, self.count)

    async def cancel_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            return await interaction.response.send_message("This is not for you!", ephemeral=True)

        await interaction.message.delete()
        await interaction.response.send_message("Purge cancelled.", ephemeral=True)


class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def _clear(self, channel, count: int):
        # حذف پیام‌های اصلی (بدون احتساب پیام تاییدیه چون قبلا حذف شده)
        deleted_messages = await channel.purge(limit=count+1)
        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name="Clear:", value=f"{len(deleted_messages)} message(s) have been deleted.")
        await channel.send(embed=conf_embed, delete_after=5)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def clear(self, ctx, count: int):
        if count < 1:
            await ctx.send("Please specify a number greater than 0.", delete_after=5)
            return

        view = ClearConfirmView(self, count, ctx.author)
        await ctx.send(view=view)


async def setup(client):
    await client.add_cog(Clear(client))