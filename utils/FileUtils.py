import discord
from discord import File, HTTPException

from services.LoggingService import LoggingService

FEWER_GIF = "assets/gifs/fewer.gif"
FANCY_BONK_GIF = "assets/gifs/fancy_bonk.gif"
BELOVED_GIF = "assets/gifs/beloved.gif"
GET_GNOMED_GIF = "assets/gifs/get_gnomed.gif"


async def send_file(ctx, file):
    await ctx.send(file=file)


async def send_file_with_reaction(ctx, file, emoji):
    message = await ctx.send(file=file)
    try:
        await message.add_reaction(emoji)
    except HTTPException as e:
        LoggingService().exception(e)


def get_file(path):
    with open(path, 'rb') as f:
        picture = discord.File(f)
        return picture


def is_file(item):
    return isinstance(item, File)
