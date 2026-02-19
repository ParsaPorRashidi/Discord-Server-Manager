import discord
import json
import os
import re

from discord import ui
from discord.ext import commands

from config import DATA_FILE
from config import STREAM_CHANNEL_ID, LIVE_ROLE_ID, STREAMER_ROLE_ID

DATA_FILE = DATA_FILE


def add_active_stream(message_id: int, streamer_id: int):
    if not os.path.exists("data"): os.makedirs("data")
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {}
    data[str(message_id)] = streamer_id
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


class StreamAnnouncementView(ui.LayoutView):
    def __init__(self, streamer_id: int, url: str, title: str, thumbnail: str, avatar_url: str):
        super().__init__(timeout=None)
        self.streamer_id = streamer_id
        self.url = url
        self.title = title
        self.thumbnail = thumbnail
        self.avatar_url = avatar_url
        self.build_layout()

    def build_layout(self):
        self.clear_items()
        container = ui.Container(accent_color=0x6441a5)

        container.add_item(ui.TextDisplay(f"🚀 @everyone <@{self.streamer_id}> is now live!"))

        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.small))

        header = ui.Section(
            ui.TextDisplay(f"# 🔴 {self.title}"),ui.TextDisplay(f"# We Start Our Live Stream!!! "),
            accessory=ui.Thumbnail(self.avatar_url)
        )
        container.add_item(header)

        watch_btn = ui.Button(label="Watch Stream", url=self.url, style=discord.ButtonStyle.link)
        end_btn = ui.Button(label="End Stream", style=discord.ButtonStyle.red, emoji="🛑")
        end_btn.callback = self.end_callback

        container.add_item(ui.ActionRow(watch_btn, end_btn))

        if self.thumbnail:
            gallery = ui.MediaGallery()
            gallery.add_item(media=self.thumbnail)
            container.add_item(gallery)

        self.add_item(container)

    async def end_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.streamer_id and not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ Only the streamer or an admin can end this.",
                                                           ephemeral=True)

        guild = interaction.guild
        streamer = guild.get_member(self.streamer_id)
        live_role = guild.get_role(LIVE_ROLE_ID)

        if streamer and live_role:
            try:
                await streamer.remove_roles(live_role)
            except:
                pass

        await interaction.message.delete()
        if not interaction.response.is_done():
            await interaction.response.send_message("✅ Stream ended.", ephemeral=True)


class GoLiveModal(ui.Modal, title="Start a New Stream"):
    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    stream_url = ui.TextInput(label="Stream Link", placeholder="YouTube or Twitch URL", required=True)
    stream_title = ui.TextInput(label="Stream Title", placeholder="Enter your stream topic...", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        streamer_role = interaction.guild.get_role(STREAMER_ROLE_ID)
        if not streamer_role or streamer_role not in interaction.user.roles:
            return await interaction.response.send_message("❌ You need the Streamer role.", ephemeral=True)

        url = self.stream_url.value.strip()
        if not any(domain in url for domain in ["youtube.com", "youtu.be", "twitch.tv"]):
            return await interaction.response.send_message("❌ Invalid stream link.", ephemeral=True)

        title = self.stream_title.value or f"{interaction.user.display_name} is LIVE!"
        thumbnail = self.cog.get_thumbnail(url)
        channel = interaction.guild.get_channel(STREAM_CHANNEL_ID)

        announcement_view = StreamAnnouncementView(
            streamer_id=interaction.user.id,
            url=url,
            title=title,
            thumbnail=thumbnail,
            avatar_url=interaction.user.display_avatar.url
        )

        try:
            msg = await channel.send(view=announcement_view)

            live_role = interaction.guild.get_role(LIVE_ROLE_ID)
            if live_role: await interaction.user.add_roles(live_role)

            add_active_stream(msg.id, interaction.user.id)
            await interaction.response.send_message(f"✅ Announced in {channel.mention}!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


class GoLiveButtonView(ui.LayoutView):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog
        self.build_layout()

    def build_layout(self):
        self.clear_items()
        container = ui.Container(accent_color=0xa71ee4)
        container.add_item(ui.TextDisplay("# 🎥 Streamer Control Panel"))
        container.add_item(ui.TextDisplay("Ready? Click the button below to go live!"))

        btn = ui.Button(label="Go Live", style=discord.ButtonStyle.primary, emoji="🚀", custom_id="go_live_start")
        btn.callback = self.start_callback
        container.add_item(ui.ActionRow(btn))
        self.add_item(container)

    async def start_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(GoLiveModal(self.cog))


class Streamer(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_thumbnail(self, url: str) -> str | None:
        yt_match = re.search(r"(?:v=|youtu\.be/|embed/)([0-9A-Za-z_-]{11})", url)
        if yt_match: return f"https://img.youtube.com/vi/{yt_match.group(1)}/maxresdefault.jpg"
        tw_match = re.search(r"twitch\.tv/([a-zA-Z0-9_]+)", url)
        if tw_match: return f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{tw_match.group(1)}-1280x720.jpg"
        return None

    @commands.command(name="setup_golive")
    @commands.has_permissions(administrator=True)
    async def setup_golive(self, ctx):
        view = GoLiveButtonView(self)
        await ctx.send(view=view)


async def setup(client):
    await client.add_cog(Streamer(client))