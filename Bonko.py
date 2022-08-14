# main.py
from random import randint
from typing import List

import discord
import emojis
from discord import HTTPException
from discord.ext import commands
from discord.ext.commands import Cog

from beans.ReactMode import ReactMode
from enums.AsciiArtEnum import AsciiArtEnum
from enums.CommandsEnum import CommandsEnum
from enums.EmojiEnum import EmojiEnum
from enums.OnMessageResponseTypeEnum import OnMessageResponseTypeEnum
from enums.OnOffEnum import OnOffEnum
from enums.QuoteEnum import QuoteEnum
from enums.RoleEnum import RoleEnum
from enums.ServerEnum import ServerEnum
from enums.UserEnum import UserEnum
from services.ArtService import ArtService
from services.KeepAliveService import keep_alive
from services.LoggingService import LoggingService
from services.LoopService import LoopService
from services.PermissionService import PermissionService
from services.ResponseService import ResponseService
from services.TextExtractingService import TextExtractingService
from utils import FileUtils
import random


class Bonko(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.allowed_to_spam = set()
        self.logging_service = LoggingService()
        self.art_service = ArtService()
        self.react_mode_properties = ReactMode()
        self.get_gnomed_bad_luck_protection = 0
        keep_alive()

    @commands.Cog.listener()
    async def on_ready(self):
        self.permission_service = PermissionService(self.bot.user.id, self.logging_service)
        # self.loop_service = LoopService(self.bot, self.logging_service, self.permission_service)
        # self.loop_service.init_loops()
        self.response_service = ResponseService(self.logging_service, self.permission_service)
        self.text_extracting_service = TextExtractingService(self.bot)
        print(f'{self.bot.user.name} is here to please the Green Cone!')

    @commands.command(name="extract")
    async def extract(self, ctx):
        if self.is_megus(ctx.author.id):
            await self.text_extracting_service.extract(ctx, UserEnum.GIANNAKIS.value.id)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.id == self.bot.user.id:
            return
        response_enum = OnMessageResponseTypeEnum.get_from_message(ctx.content.lower())
        if response_enum:
            await self.response_service.send_response(ctx, response_enum)
        if self.react_mode_properties.is_active():
            for emoji in self.react_mode_properties.get_emojis():
                emoji = await EmojiEnum.get_emoji(ctx.guild.emojis, emoji)
                await ctx.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild = message.guild
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
            entry_target = entry.target
        channel = message.channel
        if self.permission_service.is_bonko(entry_target.id):
            banned_stuff = ["anaraes + digestives", "did you mean: ye"]
            if message.content and (message.content.lower() in banned_stuff):
                await channel.send("This is turning me on Step-Bonko!")
                # print(" " + message.content)

    @Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await self.react_to(reaction, EmojiEnum.BONK.value)
        await self.react_to(reaction, EmojiEnum.SALT.value)

    async def react_to(self, reaction, emoji_to_react_to):
        # try:
        if isinstance(reaction, str):
            reaction_emoji_name = reaction
        else:
            if isinstance(reaction.emoji, str):
                reaction_emoji_name = reaction.emoji
            else:
                reaction_emoji_name = reaction.emoji.name
        if emoji_to_react_to == reaction_emoji_name:
            message = reaction.message
            guild = reaction.message.guild
            bonk_emoji = await EmojiEnum.get_emoji(guild.emojis, reaction_emoji_name)
            await message.add_reaction(bonk_emoji)
        # except:
        #     pass

    @commands.command(name=CommandsEnum.REACT_MODE.value.command)
    async def react_mode(self, ctx: commands.context, activation, *emojis):
        self.logging_service.log_starting_process(CommandsEnum.REACT_MODE.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.REACT_MODE):
            return
        onOffEnum = OnOffEnum.get_from_display(activation)
        if OnOffEnum.is_on(onOffEnum):
            self.react_mode_properties.set_active(True)
            self.react_mode_properties.set_emojis(emojis)
        elif OnOffEnum.is_off(onOffEnum):
            self.react_mode_properties.set_active(False)
            self.react_mode_properties.set_emojis(None)

    @commands.command(name=CommandsEnum.SALT_MODE.value.command)
    async def salt_mode(self, ctx: commands.context, activation):
        self.logging_service.log_starting_process(CommandsEnum.SALT_MODE.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.SALT_MODE):
            return
        await self.react_mode(ctx, activation, EmojiEnum.SALT.value)

    @commands.command(name=CommandsEnum.HELP.value.command)
    async def help(self, ctx: commands.context, role=None):
        self.logging_service.log_starting_process(CommandsEnum.HELP.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.HELP):
            return
        if role is None or role.lower() == 'all':
            role = RoleEnum.DEVELOPER.value
        role = RoleEnum.get_from_string(role)
        message = CommandsEnum.format_displays_for_help_command(role)
        await self.send_message(ctx, message)

    @commands.command(name=CommandsEnum.HAXOR.value.command)
    async def haxor(self, ctx: commands.context, code, send_message=False):
        self.logging_service.log_starting_process(CommandsEnum.HAXOR.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.HAXOR):
            return
        execution_result = {}
        try:
            exec(code, globals(), execution_result)
            if execution_result:
                message = execution_result['results']()
                if send_message:
                    await self.send_message(ctx, message)
        except Exception as e:
            await self.send_message(ctx, e)

    @commands.command(name=CommandsEnum.SAY.value.command)
    async def say(self, ctx: commands.context, server_name, channel_name, message):
        self.logging_service.log_starting_process(CommandsEnum.SAY.value)
        author_id = ctx.author.id
        if not self.is_allowed_to_use_command(author_id, CommandsEnum.SAY):
            return
        await self.console_say(server_name, channel_name, message)

    async def console_say(self, server_name, channel_name, message):
        guild = self.bot.get_guild(ServerEnum.get_from_name(server_name).value.id)
        if not guild:
            self.logging_service.log(f"Server '{server_name}' not found for {CommandsEnum.SAY.value}")
            return
        for channel in guild.text_channels:
            if channel.name == channel_name:
                message = message.replace("\"", "")
                # print(message)
                # print(channel.name)
                await channel.send(message)

    @commands.command(name=CommandsEnum.BONK.value.command)
    async def bonk(self, ctx: commands.context):
        self.logging_service.log_starting_process(CommandsEnum.BONK.value)
        author_id = ctx.author.id
        if not self.is_allowed_to_use_command(author_id, CommandsEnum.BONK):
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

    @commands.command(name=CommandsEnum.OMEGA_BONK.value.command)
    async def omega_bonk(self, ctx: commands.context):
        self.logging_service.log_starting_process(CommandsEnum.OMEGA_BONK.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.OMEGA_BONK):
            return
        index = randint(0, 1)
        emoji = await self.get_custom_emoji(ctx, EmojiEnum.BONK.value)
        if index == 0:
            message = self.art_service.get_omega_bonk()
            await self.send_message_with_reaction(ctx, message, emoji)
        else:
            file = FileUtils.get_file(FileUtils.FANCY_BONK_GIF)
            await self.send_file_with_reaction(ctx, file, emoji)

    @commands.command(name=CommandsEnum.SALT.value.command)
    async def salt(self, ctx: commands.context):
        self.logging_service.log_starting_process(CommandsEnum.SALT.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.SALT):
            return
        message = self.art_service.get_salt()
        emoji = await self.get_emoji(ctx, EmojiEnum.SALT.value)
        await self.send_message_with_reaction(ctx, message, emoji)

    @commands.command(name="giannakis")
    async def giannakis(self, ctx: commands.context):
        self.logging_service.log_starting_process(CommandsEnum.OMEGA_BONK.value)
        message = AsciiArtEnum.GIANNAKIS.value
        print(len(message))
        emoji = await self.get_custom_emoji(ctx, EmojiEnum.BONK.value)
        await self.send_message_with_reaction(ctx, message, emoji)

    @commands.command(name=CommandsEnum.SPAM_SOFT.value.command)
    async def spam_soft(self, ctx: commands.context, emoji: str, times: int, *usernames):
        self.logging_service.log_starting_process(CommandsEnum.SPAM_SOFT.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.SPAM_SOFT):
            return
        await self.handle_spam(ctx, emoji, times, list(usernames), False)

    @commands.command(name=CommandsEnum.SPAM_HARD.value.command)
    async def spam_hard(self, ctx: commands.context, emoji: str, times: int, *usernames):
        self.logging_service.log_starting_process(CommandsEnum.SPAM_HARD.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.SPAM_HARD):
            return
        await self.handle_spam(ctx, emoji, times, list(usernames), True)

    async def handle_spam(self, ctx: commands.context, emoji: str, times: int, usernames, fuck_off: bool):
        print(usernames)
        author_id = ctx.author.id
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

    @commands.command(name=CommandsEnum.BAD_GIANNAKIS.value.command)
    async def bad_giannakis(self, ctx: commands.context):
        self.logging_service.log_starting_process(CommandsEnum.BAD_GIANNAKIS.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.BAD_GIANNAKIS):
            return
        async for message in ctx.channel.history(limit=200):
            # if self.is_megus(message.author.id) and message.content == ';;extract':
            if self.is_giannakis(message.author.id):
                id = self.format_user_id_for_mention(str(UserEnum.MELDANEN.value))
                contentsNoSpaces = message.content.replace(" ", "")
                contentsSplit = contentsNoSpaces.split(id)
                contents = "".join(contentsSplit)
                if not contents:
                    await message.delete()

    @commands.command(name=CommandsEnum.WORD_OF_THE_DAY.value.command)
    async def word_of_the_day(self, ctx: commands.context):
        self.logging_service.log_starting_process(CommandsEnum.WORD_OF_THE_DAY.value)
        author_id = ctx.author.id
        if not self.is_allowed_to_use_command(author_id, CommandsEnum.WORD_OF_THE_DAY):
            return
        if self.is_giannakis(author_id):
            await self.send_message(ctx, "No horny!")
        else:
            emoji = await EmojiEnum.get_emoji(ctx.guild.emojis, EmojiEnum.BONK.value)
            await self.send_message_with_reaction(ctx, EmojiEnum.BONK.value, emoji)

    @commands.command(name=CommandsEnum.PERMISSIONS.value.command)
    async def permissions(self, ctx: commands.context, permission, *usernames):
        self.logging_service.log_starting_process(f'{CommandsEnum.PERMISSIONS.value}:{permission}')
        author_id = ctx.author.id
        if not self.is_allowed_to_use_command(author_id, CommandsEnum.PERMISSIONS):
            return
        if CommandsEnum.is_spam_related(permission):
            if self.is_good_person(author_id):
                if CommandsEnum.is_allow_spam(permission) and self.is_allowed_to_use_command(author_id,
                                                                                             CommandsEnum.ALLOW_SPAM):
                    await self.handle_spam_allowance(ctx, usernames, self.allowed_to_spam.add)
                elif CommandsEnum.is_disallow_spam(permission) and self.is_allowed_to_use_command(author_id,
                                                                                                  CommandsEnum.DISALLOW_SPAM):
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

    @commands.command(name=CommandsEnum.ASTONISHED.value.command)
    async def astonished(self, ctx: commands.context, naked=""):
        self.logging_service.log_starting_process(CommandsEnum.ASTONISHED.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.ASTONISHED):
            return
        emoji = await self.get_emoji(ctx, EmojiEnum.ASTONISHED.value)
        message = ""
        if naked.lower() == "naked":
            message += "u r naked on your cauch, having sex with your boyfriend. i came by knocked your door not very loud. u didnt hear it, and i open oyur door and find u naked on the couch with a dick inside u. i am very sure u would be  very okish with that. u wouldnt throw the couch on my head but anw. i personally dont like this at all \n"
            message += "the point is: lets say i am gay. but id idnt want to share this with my family ok? and now that i am leaving alone, i invited my bf at my place, and we decided to fuck the shit out of each other on the couch and the door suddently opens \n"
        message += "i am just astonished, how i was SO clear that i am leaving the house cause i cant have my privacy there.\n"
        message += " and they came in just like that at the new place. \n"
        message += "i am just astonished on how they cant comprihent that simple thing"
        await self.send_message_with_reaction(ctx, message, emoji)

    @commands.command(name=CommandsEnum.SHRUG.value.command)
    async def shrug(self, ctx: commands.context):
        self.logging_service.log_starting_process(CommandsEnum.SHRUG.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.SHRUG):
            return
        message = "¯\_(ツ)_/¯"
        await self.send_message(ctx, message)
        await ctx.message.delete()

    @commands.command(name=CommandsEnum.ART.value.command)
    async def art(self, ctx: commands.context, *fart_on_emoji):
        self.logging_service.log_starting_process(CommandsEnum.ART.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.ART):
            return
        head, neck, ass, leg = await self.art_service.get_sibling_art(ctx, fart_on_emoji)
        await self.send_message(ctx, head)
        await self.send_message(ctx, neck)
        await self.send_message(ctx, ass)
        await self.send_message(ctx, leg)

    @commands.command(name=CommandsEnum.LEMONARIS.value.command)
    async def lemonaris(self, ctx: commands.context, *fart_on_emoji):
        self.logging_service.log_starting_process(CommandsEnum.LEMONARIS.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.LEMONARIS):
            return
        message = await self.art_service.get_lemonaris_art(ctx, fart_on_emoji)
        await self.send_message(ctx, message)

    @commands.command(name=CommandsEnum.QUOTE.value.command)
    async def quote(self, ctx: commands.context, quote_id=None):
        self.logging_service.log_starting_process(CommandsEnum.QUOTE.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.QUOTE):
            return
        if quote_id:
            quote = await QuoteEnum.get_quote(ctx, int(quote_id), UserEnum.GIANNAKIS.value.id)
        else:
            quote = await QuoteEnum.get_random_quote_from_history(ctx.guild.text_channels)
        if not quote:
            return
        if FileUtils.is_file(quote):
            await self.send_file(ctx, quote)
        else:
            message = quote.quote
            reaction = await self.get_emoji(ctx, quote.reaction.value)
            await self.send_message_with_reaction(ctx, f'> {message}', reaction)

    @commands.command(name=CommandsEnum.WAR_CRIMES.value.command)
    async def war_crimes(self, ctx: commands.context, cheese=None):
        self.logging_service.log_starting_process(CommandsEnum.WAR_CRIMES.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.WAR_CRIMES):
            return
        if cheese and cheese.lower() == "cheese":
            quote = await QuoteEnum.get_quote(ctx, QuoteEnum.WAR_CRIMES_CHEESE.value.id, None)
        else:
            quote = await QuoteEnum.get_quote(ctx, QuoteEnum.WAR_CRIMES.value.id, None)
        if not quote:
            return
        if FileUtils.is_file(quote):
            emoji = await self.get_emoji(ctx, QuoteEnum.WAR_CRIMES.value.reaction.value)
            await FileUtils.send_file_with_reaction(ctx, quote, emoji)

    @commands.command(name=CommandsEnum.GARIDAKI.value.command)
    async def garidaki(self, ctx: commands.context):
        self.logging_service.log_starting_process(CommandsEnum.GARIDAKI.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.GARIDAKI):
            return
        quote = await QuoteEnum.get_quote(ctx, QuoteEnum.GARIDAKI.value.id, None)
        if not quote:
            return
        emoji = await self.get_emoji(ctx, QuoteEnum.GARIDAKI.value.reaction.value)
        await FileUtils.send_file_with_reaction(ctx, quote, emoji)

    @commands.command(name=CommandsEnum.COQ.value.command)
    async def coq(self, ctx: commands.context):
        self.logging_service.log_starting_process(CommandsEnum.COQ.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.COQ):
            return
        message = "\n———————————————————"
        message += "\n   You won coq. Type Yepge to claim"
        message += "\n———————————————————"
        await self.send_message(ctx, message)

    @commands.command(name=CommandsEnum.HIVE_MIND.value.command)
    async def hive_mind(self, ctx: commands.context):
        self.logging_service.log_starting_process(CommandsEnum.HIVE_MIND.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.HIVE_MIND):
            return
        file = self.get_file("assets/images/hivemind.png")
        await self.send_file(ctx, file)

    @commands.command(name=CommandsEnum.OH_YOU.value.command)
    async def oh_you(self, ctx: commands.context):
        self.logging_service.log_starting_process(CommandsEnum.OH_YOU.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.OH_YOU):
            return
        file = self.get_file("assets/images/kafrilla.png")
        await self.send_file(ctx, file)

    @commands.command(name=CommandsEnum.BELOVED.value.command)
    async def beloved(self, ctx: commands.context):
        self.logging_service.log_starting_process(CommandsEnum.BELOVED.value)
        if not self.is_allowed_to_use_command(ctx.author.id, CommandsEnum.BELOVED):
            return
        chance_to_get_gnomed = random.uniform(0, 1)
        get_gnomed_threshold = 0.18 + self.get_gnomed_bad_luck_protection
        print(f'Chance to get gnomed: {chance_to_get_gnomed} <= {get_gnomed_threshold}')
        if chance_to_get_gnomed <= get_gnomed_threshold:
            self.get_gnomed_bad_luck_protection = 0
            file = self.get_file(FileUtils.GET_GNOMED_GIF)
        else:
            self.get_gnomed_bad_luck_protection = self.get_gnomed_bad_luck_protection + 0.02
            file = self.get_file(FileUtils.BELOVED_GIF)
        await self.send_file(ctx, file)

    @staticmethod
    async def send_message(ctx: commands.context, message: str):
        await ctx.send(str(message))

    async def send_message_with_reaction(self, ctx: commands.context, message: str, emoji):
        message = await ctx.send(message)
        try:
            await message.add_reaction(emoji)
        except HTTPException as e:
            self.logging_service.exception(e)

    @staticmethod
    async def send_file(ctx, file):
        await FileUtils.send_file(ctx, file)

    @staticmethod
    async def send_file_with_reaction(ctx, file, emoji):
        await FileUtils.send_file_with_reaction(ctx, file, emoji)

    @staticmethod
    async def get_user(members: List, username: str, mention: bool) -> str:
        return await UserEnum.get_user(members, username, mention)

    @staticmethod
    async def get_user_id(members: List, username: str) -> int:
        return await UserEnum.get_user_id(members, username)

    @staticmethod
    async def get_giannakis(mention: bool) -> str:
        return await UserEnum.get_giannakis(mention)

    async def is_allowed_to_mention(self, author_id, fuck_off):
        return self.permission_service.is_allowed_to_mention(author_id, fuck_off)

    @staticmethod
    async def get_emoji(ctx: commands.context, emoji: str):
        return await EmojiEnum.get_emoji(ctx.guild.emojis, emoji)

    @staticmethod
    async def get_custom_emoji(ctx: commands.context, emoji: str):
        return await EmojiEnum.get_custom_emoji(ctx.guild.emojis, emoji)

    @staticmethod
    def format_user_id_for_mention(user_id: str) -> str:
        return UserEnum.format_user_id_for_mention(user_id)

    def is_allowed_to_use_command(self, user_id, command):
        return self.permission_service.is_allowed_to_use_command(user_id, command, self.allowed_to_spam)

    def is_giannakis(self, id: int) -> bool:
        return self.permission_service.is_giannakis(id)

    def is_megus(self, id: int) -> bool:
        return self.permission_service.is_megus(id)

    def is_good_person(self, id: int) -> bool:
        return self.permission_service.is_good_person(id)

    def is_quillbot(self, id: int) -> bool:
        return self.permission_service.is_quillbot(id)

    def get_file(self, path):
        return FileUtils.get_file(path)
