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
    bot = commands.Bot(command_prefix=';;', intents=intents)
    bot.add_cog(Bonko(bot))
    bot.run(TOKEN)
