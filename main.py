# main.py
import os

import discord
from dotenv import load_dotenv

from Bonko import Bonko
from discord.ext import commands

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix=';;', intents=intents, help_command=None)

    # Define the setup hook
    async def setup_hook():
        await bot.add_cog(Bonko(bot))

    bot.setup_hook = setup_hook  # Set the hook
    bot.run(TOKEN)