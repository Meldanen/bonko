# main.py
import os

import emojis
from discord import Emoji as CustomEmoji
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from emojis.db import Emoji as DefaultEmoji

from enums.EmojiEnum import EmojiEnum
from enums.UserEnum import UserEnum

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=';;')


@bot.event
async def on_ready():
    print(f'{bot.user.name} is here to bonk Giannakides!')


@bot.command(name="bonk")
async def bonk(ctx):
    print("Bonking in progress")
    if ctx.author.id == bot.user.id:
        return
    if ctx.author.id == UserEnum.GIANNAKIS.value:
        message = emojis.encode("No horny! :angry:")
        await send_message_with_reaction(ctx, message, emojis.db.get_emoji_by_alias(EmojiEnum.ANGRY.value))
        return
    await bonk_giannakis(ctx, mention=False)


@bot.command(name="spamgiannakis")
async def spam_giannakis(ctx, emoji, times):
    if ctx.author.id == bot.user.id:
        return
    if ctx.author.id == UserEnum.MELDANEN.value:
        emoji = await get_custom_emoji(ctx, emoji)
        if not emoji:
            return
        giannakis = await get_giannakis(True)
        message = f'{emoji} {giannakis}'
        for i in range(int(times)):
            await send_message_with_reaction(ctx, message, emoji)


@bot.command(name="badgiannakis")
async def bad_giannakis(ctx):
    if ctx.author.id == bot.user.id:
        return
    channel = ctx.channel
    async for message in channel.history(limit=200):
        if message.author.id == UserEnum.GIANNAKIS.value:
            id = format_user_id_for_mention(str(UserEnum.MELDANEN.value))
            contentsNoSpaces = message.content.replace(" ", "")
            contentsSplit = contentsNoSpaces.split(id)
            contents = "".join(contentsSplit)
            if not contents:
                await message.delete()


@bot.command(name="wordoftheday")
async def word_of_the_day(ctx):
    if ctx.author.id == bot.user.id:
        return
    if ctx.author.id == UserEnum.GIANNAKIS.value:
        await send_message(ctx, "No horny!")
    else:
        await send_message_with_reaction(ctx, EmojiEnum.BONK.value, EmojiEnum.BONK.value)


async def send_message(ctx, message):
    await ctx.send(str(message))


async def send_message_with_reaction(ctx, message, emoji):
    if isinstance(emoji, CustomEmoji):
        reaction = emoji
    elif isinstance(emoji, DefaultEmoji):
        reaction = emoji.emoji
    else:
        reaction = await get_custom_emoji(ctx, emoji)
    message = await ctx.send(message)
    await message.add_reaction(reaction)


async def bonk_giannakis(ctx, mention=True):
    emoji = await get_custom_emoji(ctx, EmojiEnum.BONK.value)
    giannakis = await get_giannakis(mention)
    message = f'{str(emoji)} {giannakis}'

    await send_message_with_reaction(ctx, "Bonk Giannaki", emoji)
    await send_message_with_reaction(ctx, message, emoji)
    await send_message_with_reaction(ctx, emoji, emoji)


async def get_giannakis(mention):
    if mention:
        return format_user_id_for_mention(str(UserEnum.GIANNAKIS.value))
    else:
        return "giannaki"


async def get_custom_emoji(ctx, emoji):
    return get(ctx.guild.emojis, name=emoji)


def format_user_id_for_mention(userEnum):
    return "<@!" + userEnum + ">"


bot.run(TOKEN)
