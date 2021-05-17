# main.py
import os

from dotenv import load_dotenv
from discord.ext import commands

from bonko import Bonko

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot = commands.Bot(command_prefix=';;')
    bot.add_cog(Bonko(bot))
    bot.run(TOKEN)
