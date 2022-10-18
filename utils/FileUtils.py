from typing import List

import discord
from discord import File, HTTPException

from enums.EmojiEnum import EmojiEnum
from services.LoggingService import LoggingService

FEWER_GIF = "assets/gifs/fewer.gif"
FANCY_BONK_GIF = "assets/gifs/fancy_bonk.gif"
BELOVED_GIF = "assets/gifs/beloved.gif"
GET_GNOMED_GIF = "assets/gifs/get_gnomed.gif"


async def send_file(ctx, file):
    await ctx.send(file=file)


async def send_file_with_reaction(ctx, file, emojis=[]):
    message = await ctx.send(file=file)
    await add_reaction_to_message(ctx, message, emojis)


async def add_reaction_to_message(ctx, message, emojis=[]):
    if not isinstance(emojis, List): emojis = [emojis]
    try:
        for emoji in emojis:
            emoji = await EmojiEnum.get_emoji(ctx.guild.emojis, emoji)
            await message.add_reaction(emoji)
    except HTTPException as e:
        LoggingService().exception(e)


def get_file(path):
    with open(path, 'rb') as f:
        picture = discord.File(f)
        return picture


def is_file(item):
    return isinstance(item, File)
