# main.py
from typing import Callable, List

import emojis
from discord.ext import commands

from enums.CommandsEnum import CommandsEnum
from enums.EmojiEnum import EmojiEnum
from enums.UserEnum import UserEnum


class Bonko(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.allowed_to_spam = set()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} is here to bonk Giannakides!')

    @commands.command(name=CommandsEnum.BONK.value)
    async def bonk(self, ctx: commands.context):
        print(CommandsEnum.BONK.value + " in progress")
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        if self.is_giannakis(author_id):
            message = emojis.encode("No horny! :angry:")
            await self.send_message_with_reaction(ctx, message, emojis.db.get_emoji_by_alias(EmojiEnum.ANGRY.value))
            return

        emoji = await self.get_custom_emoji(ctx, EmojiEnum.BONK.value)
        giannakis = await self.get_giannakis(False)
        message = f'{str(emoji)} {giannakis}'

        await self.send_message_with_reaction(ctx, "Bonk Giannaki", emoji)
        await self.send_message_with_reaction(ctx, message, emoji)
        await self.send_message_with_reaction(ctx, emoji, emoji)

    @commands.command(name=CommandsEnum.SPAM_SOFT.value)
    async def spam_gentle(self, ctx: commands.context, emoji: str, times: int, *usernames: List[str]):
        print(CommandsEnum.SPAM_SOFT.value + " in progress")
        await self.handle_spam(ctx, emoji, times, usernames, False)

    @commands.command(name=CommandsEnum.SPAM_HARD.value)
    async def spam_hard(self, ctx: commands.context, emoji: str, times: int, *usernames: List[str]):
        print(CommandsEnum.SPAM_HARD.value + " in progress")
        await self.handle_spam(ctx, emoji, times, usernames, True)

    async def handle_spam(self, ctx: commands.context, emoji: str, times: int, usernames: List[str], fuck_off: bool):
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        if self.is_allowed_to_spam(author_id):
            emoji = await self.get_emoji(ctx, emoji)
            if not emoji:
                return
            can_mention = self.is_megus(author_id) and fuck_off
            spam_string = ""
            for username in usernames:
                user_to_spam = await self.get_user(ctx.guild.members, username, can_mention)
                spam_string = spam_string + " " + user_to_spam
            message = f'{emoji} {spam_string} {emoji}'
            for i in range(int(times)):
                await self.send_message_with_reaction(ctx, message, emoji)

    @commands.command(name=CommandsEnum.BAD_GIANNAKIS.value)
    async def bad_giannakis(self, ctx: commands.context):
        print(CommandsEnum.BAD_GIANNAKIS.value + " in progress")
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
    async def word_of_the_day(self, ctx: commands.context):
        print(CommandsEnum.WORD_OF_THE_DAY.value + " in progress")
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        if self.is_giannakis(author_id):
            await self.send_message(ctx, "No horny!")
        else:
            emoji = await EmojiEnum.get_emoji(ctx.guild.emojis, EmojiEnum.BONK.value)
            await self.send_message_with_reaction(ctx, EmojiEnum.BONK.value, emoji)

    @commands.command(name=CommandsEnum.PERMISSIONS.value)
    async def permissions(self, ctx: commands.context, permission: CommandsEnum, *usernames: List[str]):
        print(f'{CommandsEnum.PERMISSIONS.value}:{permission} in progress')
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        if CommandsEnum.is_spam_related(permission):
            if self.is_good_person(author_id):
                if CommandsEnum.is_allow_spam(permission):
                    await self.handle_spam_allowance(ctx, usernames, self.allowed_to_spam.add)
                elif CommandsEnum.is_disallow_spam(permission):
                    await self.handle_spam_allowance(ctx, usernames, self.allowed_to_spam.remove)
                print("Can spam:")
                print(self.allowed_to_spam)

    async def handle_spam_allowance(self, ctx: commands.context, usernames: List[str], add_or_remove: Callable):
        try:
            for username in usernames:
                user_id = await self.get_user_id(ctx.guild.members, username)
                add_or_remove(user_id)
        except KeyError:
            print(f'{username}:{user_id} not found')

    @staticmethod
    async def send_message(ctx: commands.context, message: str):
        await ctx.send(str(message))

    @staticmethod
    async def send_message_with_reaction(ctx: commands.context, message: str, emoji):
        message = await ctx.send(message)
        await message.add_reaction(emoji)

    @staticmethod
    async def get_user_id(members: List, username: str) -> int:
        for member in members:
            if username.lower() in member.name.lower():
                return member.id

    async def get_user(self, members: List, username: str, mention: bool) -> str:
        if mention:
            user_id = await self.get_user_id(members, username)
            return self.format_user_id_for_mention(str(user_id))
        else:
            return username

    async def get_giannakis(self, mention: bool) -> str:
        if mention:
            return self.format_user_id_for_mention(str(UserEnum.GIANNAKIS.value))
        else:
            return "giannaki"

    @staticmethod
    async def get_emoji(ctx: commands.context, emoji: str):
        return await EmojiEnum.get_emoji(ctx.guild.emojis, emoji)

    @staticmethod
    async def get_custom_emoji(ctx: commands.context, emoji: str):
        return await EmojiEnum.get_custom_emoji(ctx.guild.emojis, emoji)

    @staticmethod
    def format_user_id_for_mention(user_id: str) -> str:
        return "<@!" + user_id + ">"

    @staticmethod
    def is_giannakis(id: int) -> bool:
        return UserEnum.is_giannakis(id)

    @staticmethod
    def is_megus(id: int) -> bool:
        return UserEnum.is_megus(id)

    @staticmethod
    def is_good_person(id: int) -> bool:
        return UserEnum.is_good_person(id)

    def is_allowed_to_spam(self, id: int) -> bool:
        return self.is_good_person(id) or self.is_emergency_permission(id)

    def is_emergency_permission(self, id: int) -> bool:
        return id in self.allowed_to_spam
