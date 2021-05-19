# main.py
import emojis
from discord import Emoji as CustomEmoji
from discord.ext import commands
from discord.utils import get
from emojis.db import Emoji as DefaultEmoji

from enums.CommandsEnum import CommandsEnum
from enums.EmojiEnum import EmojiEnum
from enums.UserEnum import UserEnum


class Bonko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emergency_bonkage = set()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} is here to bonk Giannakides!')

    @commands.command(name=CommandsEnum.BONK.value)
    async def bonk(self, ctx):
        print("Bonking in progress")
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        if self.is_megus(author_id):
            message = emojis.encode("No horny! :angry:")
            await self.send_message_with_reaction(ctx, message, emojis.db.get_emoji_by_alias(EmojiEnum.ANGRY.value))
            return

        emoji = await self.get_custom_emoji(ctx, EmojiEnum.BONK.value)
        giannakis = await self.get_giannakis(False)
        message = f'{str(emoji)} {giannakis}'

        await self.send_message_with_reaction(ctx, "Bonk Giannaki", emoji)
        await self.send_message_with_reaction(ctx, message, emoji)
        await self.send_message_with_reaction(ctx, emoji, emoji)

    @commands.command(name=CommandsEnum.SPAM_GIANNAKIS.value)
    async def spam_giannakis(self, ctx, emoji, times, fuck_off=False):
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        if self.is_allowed_to_spam(author_id):
            emoji = await self.get_emoji(ctx, emoji)
            if not emoji:
                return
            giannakis = await self.get_giannakis(self.is_megus(author_id) and fuck_off)
            message = f'{emoji} {giannakis} {emoji}'
            for i in range(int(times)):
                await self.send_message_with_reaction(ctx, message, emoji)

    @commands.command(name=CommandsEnum.BAD_GIANNAKIS.value)
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

    @commands.command(name=CommandsEnum.WORD_OF_THE_DAY.value)
    async def word_of_the_day(self, ctx):
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        if self.is_giannakis(author_id):
            await self.send_message(ctx, "No horny!")
        else:
            emoji = await EmojiEnum.get_emoji(ctx.guild.emojis, EmojiEnum.BONK.value)
            await self.send_message_with_reaction(ctx, EmojiEnum.BONK.value, emoji)

    @commands.command(name=CommandsEnum.ALLOW_BONKAGE.value)
    async def allow_bonkage(self, ctx, *args):
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        if self.is_good_person(author_id):
            await self.handle_bonkage(ctx, args, self.emergency_bonkage.add)
        print("Can spam:")
        print(self.emergency_bonkage)

    @commands.command(name=CommandsEnum.DISALLOW_BONKAGE.value)
    async def disallow_bonkage(self, ctx, *args):
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        if self.is_good_person(author_id):
            await self.handle_bonkage(ctx, args, self.emergency_bonkage.remove)
        print("Can spam:")
        print(self.emergency_bonkage)

    @staticmethod
    async def handle_bonkage(ctx, args, add_or_remove):
        members = ctx.guild.members
        for member in members:
            for username in args:
                if username.lower() in member.name.lower():
                    add_or_remove(member.id)

    @staticmethod
    async def send_message(ctx, message):
        await ctx.send(str(message))

    async def send_message_with_reaction(self, ctx, message, emoji):
        message = await ctx.send(message)
        await message.add_reaction(emoji)

    async def get_giannakis(self, mention):
        if mention:
            return self.format_user_id_for_mention(str(UserEnum.GIANNAKIS.value))
        else:
            return "giannaki"

    async def get_emoji(self, ctx, emoji):
        return await EmojiEnum.get_emoji(ctx.guild.emojis, emoji)

    @staticmethod
    async def get_custom_emoji(ctx, emoji):
        return await EmojiEnum.get_custom_emoji(ctx.guild.emojis, emoji)

    @staticmethod
    def format_user_id_for_mention(userEnum):
        return "<@!" + userEnum + ">"

    @staticmethod
    def is_giannakis(id):
        return UserEnum.is_giannakis(id)

    @staticmethod
    def is_megus(id):
        return UserEnum.is_megus(id)

    @staticmethod
    def is_good_person(id):
        return UserEnum.is_good_person(id)

    def is_allowed_to_spam(self, id):
        return self.is_good_person(id) or self.is_emergency_permission(id)

    def is_emergency_permission(self, id):
        return id in self.emergency_bonkage
