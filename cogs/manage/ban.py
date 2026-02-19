import discord
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):

        await ctx.guild.ban(member, reason=reason)
        conf_embed = discord.Embed(title="Success!", color=discord.Color.red())
        conf_embed.add_field(name="Banned:", value=f"{member.mention} has been banned from the server by {ctx.author.mention}.", inline=False)
        conf_embed.add_field(name="Reason:", value=reason or "No reason provided", inline=False)
        await ctx.send(embed=conf_embed)

    @commands.has_permissions(administrator=True)
    @commands.command(name="unban", description="Unban a member by ID")
    async def unban(self, ctx, user_id: int):
        try:
            user_id = int(user_id)
        except ValueError:
            return await ctx.send("Please provide a valid user ID.")

        try:
            banned_users = await ctx.guild.bans()
            user = discord.utils.get(banned_users, user__id=user_id)

            if user is None:
                return await ctx.send(f"User with ID {user_id} is not banned.")

            await ctx.guild.unban(user.user)
            await ctx.send(f"User {user.user.name}#{user.user.discriminator} has been unbanned.")

        except discord.Forbidden:
            await ctx.send("I don't have the required permissions to unban users.")
        except discord.HTTPException:
            await ctx.send("An error occurred while trying to unban the user.")

async def setup(client):
    await client.add_cog(Ban(client))