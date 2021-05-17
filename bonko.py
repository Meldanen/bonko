# main.py
import os

import emojis
from discord import Emoji as CustomEmoji
from discord.ext import commands
from discord.utils import get
from emojis.db import Emoji as DefaultEmoji

from enums.EmojiEnum import EmojiEnum
from enums.UserEnum import UserEnum



class Bonko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} is here to bonk Giannakides!')

    @commands.command()
    async def bonk(self, ctx):
        print("Bonking in progress")
        if ctx.author.id == self.bot.user.id:
            return
        if self.is_giannakis(ctx.author.id):
            message = emojis.encode("No horny! :angry:")
            await self.send_message_with_reaction(ctx, message, emojis.db.get_emoji_by_alias(EmojiEnum.ANGRY.value))
            return

        emoji = await self.get_custom_emoji(ctx, EmojiEnum.BONK.value)
        giannakis = await self.get_giannakis(False)
        message = f'{str(emoji)} {giannakis}'

        await self.send_message_with_reaction(ctx, "Bonk Giannaki", emoji)
        await self.send_message_with_reaction(ctx, message, emoji)
        await self.send_message_with_reaction(ctx, emoji, emoji)

    @commands.command(name="spamgiannakis")
    async def spam_giannakis(self, ctx, emoji, times):
        if ctx.author.id == self.bot.user.id:
            return
        if self.is_good_person(ctx.author.id):
            emoji = await self.get_custom_emoji(ctx, emoji)
            if not emoji:
                return
            giannakis = await self.get_giannakis(True)
            message = f'{emoji} {giannakis}'
            for i in range(int(times)):
                await self.send_message_with_reaction(ctx, message, emoji)

    @commands.command(name="badgiannakis")
    async def bad_giannakis(self, ctx):
        if ctx.author.id == self.bot.user.id:
            return
        channel = ctx.channel
        async for message in channel.history(limit=200):
            if self.is_giannakis(message.author.id):
                id = self.format_user_id_for_mention(str(UserEnum.MELDANEN.value))
                contentsNoSpaces = message.content.replace(" ", "")
                contentsSplit = contentsNoSpaces.split(id)
                contents = "".join(contentsSplit)
                if not contents:
                    await message.delete()

    @commands.command(name="wordoftheday")
    async def word_of_the_day(self, ctx):
        if ctx.author.id == self.bot.user.id:
            return
        if self.is_giannakis(ctx.author.id):
            await self.send_message(ctx, "No horny!")
        else:
            await self.send_message_with_reaction(ctx, EmojiEnum.BONK.value, EmojiEnum.BONK.value)

    @staticmethod
    async def send_message(ctx, message):
        await ctx.send(str(message))

    async def send_message_with_reaction(self, ctx, message, emoji):
        if isinstance(emoji, CustomEmoji):
            reaction = emoji
        elif isinstance(emoji, DefaultEmoji):
            reaction = emoji.emoji
        else:
            reaction = await self.get_custom_emoji(ctx, emoji)
        message = await ctx.send(message)
        await message.add_reaction(reaction)

    async def get_giannakis(self, mention):
        if mention:
            return self.format_user_id_for_mention(str(UserEnum.GIANNAKIS.value))
        else:
            return "giannaki"

    @staticmethod
    async def get_custom_emoji(ctx, emoji):
        return get(ctx.guild.emojis, name=emoji)

    #
    #
    @staticmethod
    def format_user_id_for_mention(userEnum):
        return "<@!" + userEnum + ">"

    @staticmethod
    def is_giannakis(id):
        return UserEnum.is_giannakis(id)

    @staticmethod
    def is_good_person(id):
        return UserEnum.is_good_person(id)
