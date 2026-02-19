import discord
from discord import ui
from discord.ext import commands

from config import Welcome_Channel


class WelcomeLayout(ui.LayoutView):
    def __init__(self, member: discord.Member):
        super().__init__()

        container = ui.Container(accent_color=0xa71ee4)

        mention_section = ui.TextDisplay(f"{member.mention}")
        container.add_item(mention_section)

        avatar_img = ui.Thumbnail(member.display_avatar.url)
        header = ui.Section(
            ui.TextDisplay(f'# Welcome to the Club! ✨\nDear {member.display_name}, we are glad you joined!'),
            accessory=avatar_img
        )
        container.add_item(header)

        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.small))

        info_text = ui.TextDisplay(
            f"📈 Member Count: **{member.guild.member_count}**\n"
            f"🔗 Check out our links below to get started!"
        )
        container.add_item(info_text)

        website = ui.Button(label='Website', url='https://Back-Blaze.ir', emoji='🌐')
        rules = ui.Button(label='Rules', url=f"https://discord.gg/jZzdXZEDGx", emoji='📜')

        action_row = ui.ActionRow(website, rules)
        container.add_item(action_row)

        self.add_item(container)


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.welcome_channel_id = Welcome_Channel

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.get_channel(self.welcome_channel_id)
        if channel:
            try:
                layout = WelcomeLayout(member)
                await channel.send(view=layout)
            except Exception as e:
                print(f"Error: {e}")

    @commands.command(name="testwelcome")
    async def testwelcome(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        layout = WelcomeLayout(member)
        await ctx.send(view=layout)

async def setup(client):
    await client.add_cog(Welcome(client))