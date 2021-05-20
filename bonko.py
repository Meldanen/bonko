# main.py
import emojis
from discord.ext import commands
from emojis.db import Emoji as DefaultEmoji

from enums.CommandsEnum import CommandsEnum
from enums.EmojiEnum import EmojiEnum
from enums.UserEnum import UserEnum


class Bonko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_to_spam = set()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} is here to bonk Giannakides!')

    @commands.command(name=CommandsEnum.BONK.value)
    async def bonk(self, ctx):
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

    @commands.command(name=CommandsEnum.SPAM.value)
    async def spam(self, ctx, username, emoji, times, fuck_off=False):
        print(CommandsEnum.SPAM.value + " in progress")
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        if self.is_allowed_to_spam(author_id):
            emoji = await self.get_emoji(ctx, emoji)
            if not emoji:
                return
            can_mention = self.is_megus(author_id) and fuck_off
            user_to_spam = await self.get_user(ctx.guild.members, username, can_mention)
            message = f'{emoji} {user_to_spam} {emoji}'
            for i in range(int(times)):
                await self.send_message_with_reaction(ctx, message, emoji)

    @commands.command(name=CommandsEnum.BAD_GIANNAKIS.value)
    async def bad_giannakis(self, ctx):
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
    async def word_of_the_day(self, ctx):
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
    async def permissions(self, ctx, permission, *usernames):
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

    async def handle_spam_allowance(self, ctx, usernames, add_or_remove):
        try:
            for username in usernames:
                user_id = await self.get_user_id(ctx.guild.members, username)
                add_or_remove(user_id)
        except KeyError:
            print(f'{username}:{user_id} not found')


    @staticmethod
    async def send_message(ctx, message):
        await ctx.send(str(message))

    @staticmethod
    async def send_message_with_reaction(ctx, message, emoji):
        message = await ctx.send(message)
        await message.add_reaction(emoji)

    @staticmethod
    async def get_user_id(members, username):
        for member in members:
            if username.lower() in member.name.lower():
                return member.id

    async def get_user(self, members, username, mention):
        if mention:
            user_id = await self.get_user_id(members, username)
            return self.format_user_id_for_mention(str(user_id))
        else:
            return username

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
        return id in self.allowed_to_spam
