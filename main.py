# main.py
import os

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
    print(f'{bot.user.name} is here to bonk Giannakides!')


@bot.command(name="bonk")
async def bonk(ctx):
    print("Bonking in progress")
    if ctx.author == bot.user:
        return
    emoji = await get_emoji(ctx, EmojiEnum.BONK.value)
    if ctx.author.id == UserEnum.GIANNAKIS.value:
        await ctx.send("Bad Giannakis! No horny!")
        return
    await send_message_with_reaction(ctx, emoji, None)
    # await send_message_with_reaction(ctx, emoji, format_user_id_for_mention(str(UserEnum.GIANNAKIS.value)))
    await send_message_with_reaction(ctx, emoji, "giannakis")
    await send_message_with_reaction(ctx, emoji, None)


@bot.command(name="spamgiannakis")
async def bonk(ctx, emoji, times):
    if ctx.author.id == bot.user.id:
        return
    if ctx.author.id == UserEnum.MELDANEN.value:
        emoji = await get_emoji(ctx, emoji)
        if not emoji:
            return
        for i in range(int(times)):
            await send_message_with_reaction(ctx, emoji, format_user_id_for_mention(str(UserEnum.GIANNAKIS.value)))


@bot.command(name="badgiannakis")
async def bonk(ctx):
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


async def send_message_with_reaction(ctx, emoji, emoji_suffix):
    if emoji_suffix:
        message = await ctx.send(f"{str(emoji)} {emoji_suffix}")
    else:
        message = await ctx.send(emoji)
    await message.add_reaction(emoji)


async def get_emoji(ctx, emoji):
    return get(ctx.guild.emojis, name=emoji)


def format_user_id_for_mention(userEnum):
    return "<@!" + userEnum + ">"


bot.run(TOKEN)
