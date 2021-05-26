# main.py
import asyncio
from typing import Callable, List

import discord
import emojis
from datetime import datetime

from discord import TextChannel, File
from discord.ext import commands

from enums.AsciiArtEnum import AsciiArtEnum
from enums.CommandsEnum import CommandsEnum
from enums.EmojiEnum import EmojiEnum
from enums.GoodBonkoResponseEnum import GoodBonkoResponseEnum
from enums.ResponseTypeEnum import ResponseTypeEnum
from enums.UserEnum import UserEnum
from services.ArtService import ArtService
from services.LoggingService import LoggingService
from services.RandomResponseService import RandomResponseService


class Bonko(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.allowed_to_spam = set()
        self.logging_service = LoggingService()
        self.art_service = ArtService()
        self.random_response_service = RandomResponseService()
        self.bot.loop.create_task(self.daily_word_of_the_day())
        self.word_of_the_day_occurred = False
        self.WORD_OF_THE_DAY_TIME = 9

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} is here to bonk Giannakides!')

        # "Did you find it?"
        # "I'm not sure"
        # "How does that make you feel?"
        # "Bonk Giannaki"
        # "No"

    async def daily_word_of_the_day(self):

        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.logging_service.log(f'Attempting daily {CommandsEnum.WORD_OF_THE_DAY.value}')
            now = datetime.now().utcnow()
            if now.hour == self.WORD_OF_THE_DAY_TIME - 1:
                self.word_of_the_day_occurred = False
                self.logging_service.log("Setting word_of_the_day_occurred to false")
            if now.hour == self.WORD_OF_THE_DAY_TIME and not self.word_of_the_day_occurred:
                guilds = self.bot.guilds
                for guild in guilds:
                    for channel in guild.text_channels:
                        if channel.name == "general":
                            self.logging_service.log_starting_progress(CommandsEnum.WORD_OF_THE_DAY.value)
                            message = await channel.send("Word of the day: bonk")
                            emoji = await EmojiEnum.get_custom_emoji(channel.guild.emojis, EmojiEnum.BONK.value)
                            await message.add_reaction(emoji)
                            self.word_of_the_day_occurred = True

            await asyncio.sleep(60 * 55)  # wait 55 minutes

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.id == self.bot.user.id:
            return
        response_enum = ResponseTypeEnum.get_from_message(ctx.content)
        if response_enum:
            await self.random_response_service.send_response(ctx, response_enum)

    @commands.command(name=CommandsEnum.BONK.value)
    async def bonk(self, ctx: commands.context):
        self.logging_service.log_starting_progress(CommandsEnum.BONK.value)
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

    @commands.command(name=CommandsEnum.OMEGA_BONK.value)
    async def omega_bonk(self, ctx: commands.context):
        self.logging_service.log_starting_progress(CommandsEnum.OMEGA_BONK.value)
        message = self.art_service.get_omega_bonk()
        emoji = await self.get_custom_emoji(ctx, EmojiEnum.BONK.value)
        await self.send_message_with_reaction(ctx, message, emoji)

    @commands.command(name="giannakis")
    async def giannakis(self, ctx: commands.context):
        self.logging_service.log_starting_progress(CommandsEnum.OMEGA_BONK.value)
        message = AsciiArtEnum.GIANNAKIS.value
        print(len(message))
        emoji = await self.get_custom_emoji(ctx, EmojiEnum.BONK.value)
        await self.send_message_with_reaction(ctx, message, emoji)

    @commands.command(name=CommandsEnum.SPAM_SOFT.value)
    async def spam_soft(self, ctx: commands.context, emoji: str, times: int, *usernames):
        self.logging_service.log_starting_progress(CommandsEnum.SPAM_SOFT.value)
        await self.handle_spam(ctx, emoji, times, list(usernames), False)

    @commands.command(name=CommandsEnum.SPAM_HARD.value)
    async def spam_hard(self, ctx: commands.context, emoji: str, times: int, *usernames):
        self.logging_service.log_starting_progress(CommandsEnum.SPAM_HARD.value)
        await self.handle_spam(ctx, emoji, times, list(usernames), True)

    async def handle_spam(self, ctx: commands.context, emoji: str, times: int, usernames, fuck_off: bool):
        print(usernames)
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        if self.is_allowed_to_spam(author_id):
            emoji = await self.get_emoji(ctx, emoji)
            if not emoji:
                return
            can_mention = await self.is_allowed_to_mention(author_id, fuck_off)
            spam_string = ""
            for username in usernames:
                user_to_spam = await self.get_user(ctx.guild.members, username, can_mention)
                spam_string = spam_string + " " + user_to_spam
            message = f'{emoji} {spam_string} {emoji}'
            for i in range(int(times)):
                await self.send_message_with_reaction(ctx, message, emoji)

    @commands.command(name=CommandsEnum.BAD_GIANNAKIS.value)
    async def bad_giannakis(self, ctx: commands.context):
        self.logging_service.log_starting_progress(CommandsEnum.BAD_GIANNAKIS.value)
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
        self.logging_service.log_starting_progress(CommandsEnum.WORD_OF_THE_DAY.value)
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        if self.is_giannakis(author_id):
            await self.send_message(ctx, "No horny!")
        else:
            emoji = await EmojiEnum.get_emoji(ctx.guild.emojis, EmojiEnum.BONK.value)
            await self.send_message_with_reaction(ctx, EmojiEnum.BONK.value, emoji)

    @commands.command(name=CommandsEnum.PERMISSIONS.value)
    async def permissions(self, ctx: commands.context, permission, *usernames):
        self.logging_service.log_starting_progress(f'{CommandsEnum.PERMISSIONS.value}:{permission}')
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

    async def handle_spam_allowance(self, ctx: commands.context, usernames, add_or_remove):
        try:
            for username in list(usernames):
                user_id = await self.get_user_id(ctx.guild.members, username)
                add_or_remove(user_id)
        except KeyError:
            print(f'{username}:{user_id} not found')

    @commands.command(name=CommandsEnum.ASTONISHED.value)
    async def astonished(self, ctx: commands.context, naked=""):
        self.logging_service.log_starting_progress(CommandsEnum.ASTONISHED.value)
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        emoji = await self.get_emoji(ctx, EmojiEnum.OPEN_MOUTH.value)
        message = ""
        if naked.lower() == "naked":
            message += "u r naked on your cauch, having sex with your boyfriend. i came by knocked your door not very loud. u didnt hear it, and i open oyur door and find u naked on the couch with a dick inside u. i am very sure u would be  very okish with that. u wouldnt throw the couch on my head but anw. i personally dont like this at all \n"
            message += "the point is: lets say i am gay. but id idnt want to share this with my family ok? and now that i am leaving alone, i invited my bf at my place, and we decided to fuck the shit out of each other on the couch and the door suddently opens \n"
        message += "i am just astonished, how i was SO clear that i am leaving the house cause i cant have my privacy there.\n"
        message += " and they came in just like that at the new place. \n"
        message += "i am just astonished on how they cant comprihent that simple thing"
        await self.send_message_with_reaction(ctx, message, emoji)

    @commands.command(name=CommandsEnum.SHRUG.value)
    async def shrug(self, ctx: commands.context):
        self.logging_service.log_starting_progress(CommandsEnum.SHRUG.value)
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        await ctx.message.delete()
        message = "¯\_(ツ)_/¯"
        await self.send_message(ctx, message)

    @commands.command(name=CommandsEnum.ART.value)
    async def art(self, ctx: commands.context, fart_on_emoji=None):
        self.logging_service.log_starting_progress(CommandsEnum.ART.value)
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        head, neck, ass, leg = await self.art_service.get_sibling_art(ctx, fart_on_emoji)
        await self.send_message(ctx, head)
        await self.send_message(ctx, neck)
        await self.send_message(ctx, ass)
        await self.send_message(ctx, leg)

    @commands.command(name=CommandsEnum.LEMONARIS.value)
    async def lemonaris(self, ctx: commands.context, fart_on_emoji=None):
        self.logging_service.log_starting_progress(CommandsEnum.LEMONARIS.value)
        author_id = ctx.author.id
        if author_id == self.bot.user.id:
            return
        message = await self.art_service.get_lemonaris_art(ctx, fart_on_emoji)
        await self.send_message(ctx, message)

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

    async def is_allowed_to_mention(self, author_id, fuck_off):
        return (self.is_megus(author_id) or self.is_melon(author_id)) and fuck_off

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
    def is_melon(id: int) -> bool:
        return UserEnum.is_melon(id)

    @staticmethod
    def is_good_person(id: int) -> bool:
        return UserEnum.is_good_person(id)

    def is_allowed_to_spam(self, id: int) -> bool:
        return self.is_good_person(id) or self.is_emergency_permission(id)

    def is_emergency_permission(self, id: int) -> bool:
        return id in self.allowed_to_spam
