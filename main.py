# main.py
import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get

from enums.EmojiEnum import EmojiEnum
from enums.UserEnum import UserEnum

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=';;')


@bot.event
async def on_ready():
    print(f'{bot.user.name} is here to bonk Giannakides')


@bot.command(name="bonk")
async def bonk(ctx):
    print("Bonking in progress")
    if ctx.author == bot.user:
        return
    emoji = await get_emoji(ctx, EmojiEnum.BONK)
    if ctx.author.id == UserEnum.GIANNAKIS.value:
        await ctx.send("Bad Giannakis!")
        return
    await send_message_with_reaction(ctx, emoji, None)
    await send_message_with_reaction(ctx, emoji, format_user_id_for_mention(str(UserEnum.GIANNAKIS.value)))
    await send_message_with_reaction(ctx, emoji, None)


async def send_message_with_reaction(ctx, emoji, emoji_suffix):
    if emoji_suffix:
        message = await ctx.send(str(emoji) + " " + emoji_suffix)
    else:
        message = await ctx.send(emoji)
    await message.add_reaction(emoji)


async def get_emoji(ctx, emojiEnum):
    return get(ctx.guild.emojis, name=emojiEnum.value)


def format_user_id_for_mention(userEnum):
    return "<@" + userEnum + ">"


bot.run(TOKEN)
