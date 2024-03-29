import asyncio
from datetime import datetime
from random import randrange

from enums.CommandsEnum import CommandsEnum
from enums.EmojiEnum import EmojiEnum
from enums.QuoteEnum import QuoteEnum
from enums.UserEnum import UserEnum


class LoopService:

    def __init__(self, bot, logging_service, permission_service):
        self.bot = bot
        self.logging_service = logging_service
        self.permission_service = permission_service
        self.word_of_the_day_occurred = False
        self.WORD_OF_THE_DAY_TIME = 9
        self.siblings_sibling_daily_penor_occured = False
        self.SIBLINGS_SIBLING_PENOR_TIME = 10
        self.times_randomly_messaged = 0
        self.MAX_TIMES_TO_RANDOMLY_MESSAGE = 2
        self.ONE_HOUR_IN_SECONDS = 3600
        self.HELEN_MODIFIER = 4

    def init_loops(self):
        # self.bot.loop.create_task(self.daily_commands())
        self.bot.loop.create_task(self.random_messages())
        # await self.bot.wait_until_ready()
        # while not self.bot.is_closed():

    async def random_messages(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            now = datetime.now().utcnow()
            if self.time_in_range(23, 1, now):
                self.times_randomly_messaged = 0
            time_to_wait = self.ONE_HOUR_IN_SECONDS * self.HELEN_MODIFIER
            # time_to_wait = randrange(self.ONE_HOUR_IN_SECONDS * self.HELEN_MODIFIER) + self.times_randomly_messaged * 100
            self.logging_service.log(f'Time until next random message: {time_to_wait}, Times messaged today: {self.times_randomly_messaged}')
            if not self.is_too_many_messages():
                self.logging_service.log_starting_process(CommandsEnum.RANDOM_MESSAGE.value)
                for guild in self.bot.guilds:
                    await self.send_random_message_to_server(guild)
                self.times_randomly_messaged += 1
            await asyncio.sleep(time_to_wait)

    async def send_random_message_to_server(self, guild):
        random_quote = await QuoteEnum.get_random_quote_from_history(guild.text_channels, None)
        random_message = f'> {random_quote.quote}'
        random_channel_index = randrange(len(guild.text_channels))
        random_channel = guild.text_channels[random_channel_index]
        while not self.permission_service.is_channel_allowed(random_channel.name):
            random_channel_index = randrange(len(guild.text_channels))
            random_channel = guild.text_channels[random_channel_index]
        self.logging_service.log(f'Sending: {random_message} to: {guild.name}:{random_channel}')
        # print(random_message)
        await random_channel.send(random_message)

    @staticmethod
    def time_in_range(start, end, x):
        """Return true if x is in the range [start, end]"""
        if start <= end:
            return start <= x.hour <= end
        else:
            return start <= x.hour or x.hour <= end

    def is_too_many_messages(self):
        return self.times_randomly_messaged > self.MAX_TIMES_TO_RANDOMLY_MESSAGE

    async def daily_commands(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.logging_service.log(f'Attempting daily {CommandsEnum.WORD_OF_THE_DAY.value}')
            await self.handle_daily_word_of_the_day()
            await self.handle_daily_siblings_sibling_penor()
            await asyncio.sleep(60 * 25)  # wait 55 minutes

    async def handle_daily_word_of_the_day(self):
        now = datetime.now().utcnow()
        if now.hour == self.WORD_OF_THE_DAY_TIME - 1:
            self.word_of_the_day_occurred = False
            self.logging_service.log(f'Setting word_of_the_day_occurred to false, {self.word_of_the_day_occurred}')
        if now.hour == self.WORD_OF_THE_DAY_TIME and not self.word_of_the_day_occurred:
            guilds = self.bot.guilds
            for guild in guilds:
                for channel in guild.text_channels:
                    if channel.name == "discord-games":
                        self.logging_service.log_starting_process(CommandsEnum.WORD_OF_THE_DAY.value)
                        emoji = await EmojiEnum.get_custom_emoji(channel.guild.emojis, EmojiEnum.BONK.value)
                        message = await channel.send("Word of the day: bonk")
                        await message.add_reaction(emoji)
            self.word_of_the_day_occurred = True
            self.logging_service.log(f'Setting word_of_the_day_occurred to true, {self.word_of_the_day_occurred}')

    async def handle_daily_siblings_sibling_penor(self):
        now = datetime.now().utcnow()
        if now.hour == self.SIBLINGS_SIBLING_PENOR_TIME - 1:
            self.siblings_sibling_daily_penor_occured = False
            self.logging_service.log(
                f'Setting siblings_sibling_daily_penor_occured to false, {self.siblings_sibling_daily_penor_occured}')
        if now.hour == self.SIBLINGS_SIBLING_PENOR_TIME and not self.siblings_sibling_daily_penor_occured:
            guilds = self.bot.guilds
            for guild in guilds:
                for channel in guild.text_channels:
                    if channel.name == "glens-weenie":
                        self.logging_service.log_starting_process("Sibling's sibling penor of the day")
                        emoji = await EmojiEnum.get_custom_emoji(guild.emojis, EmojiEnum.BONK.value)
                        user = UserEnum.format_user_id_for_mention(str(UserEnum.SIBLINGS_SIBLING.value.id))
                        message = await channel.send(user)
                        await message.add_reaction(emoji)
            self.siblings_sibling_daily_penor_occured = True
            self.logging_service.log(
                f'Setting siblings_sibling_daily_penor_occured to true, {self.word_of_the_day_occurred}')
