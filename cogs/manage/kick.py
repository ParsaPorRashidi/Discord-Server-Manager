import asyncio

import discord
from discord.ext import commands


class kick (commands.Cog):
    def __init__(self, client):
        self.client = client

    
    async def _kick(self, ctx, member: discord.Member, *, reason=None):

        if member == ctx.author:
            return await ctx.send("You cannot kick yourself.")

        await member.kick(reason=reason)

        conf_embed = discord.Embed(title="Member Kicked", color=discord.Color.red())
        conf_embed.add_field(name="Kicked Member", value=f"{member.mention}", inline=False)
        conf_embed.add_field(name="Kicked By", value=f"{ctx.author.mention}", inline=False)
        conf_embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)

        await ctx.send(embed=conf_embed)

        try:
            await member.send(f"You have been kicked from {ctx.guild.name}. Reason: {reason or 'No reason provided'}")
        except discord.HTTPException:
            pass  

            await asyncio.sleep(10)
            await ctx.channel.purge(limit=1)
        else:
            await ctx.send("You don't have permission to kick members.")

            await asyncio.sleep(10)

            await ctx.channel.purge(limit=1)


    @commands.has_permissions(administrator=True)
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await self._kick(ctx, member, reason=reason)

async def setup(client):
    await client.add_cog(kick(client))