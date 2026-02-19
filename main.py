import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix='=', intents=intents)

@client.event
async def on_ready():
    await client.tree.sync()
    print(f"✅ {client.user} IS ONLINE!")

async def load():
    for root, dirs, files in os.walk('./cogs'):
        for file in files:
            if file.endswith('.py'):
                cog_path = os.path.relpath(os.path.join(root, file), './cogs')
                cog_path = cog_path.replace(os.path.sep, '.').replace('.py', '')
                try:
                    await client.load_extension(f'cogs.{cog_path}')
                except Exception as e:
                    print(f'❌ Failed to load {file}: {e}')

async def main():
    async with client:
        await load()
        if TOKEN:
            await client.start(TOKEN)
        else:
            print("❌ Error: DISCORD_TOKEN not found in .env file.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass