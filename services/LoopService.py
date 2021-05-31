import asyncio
from datetime import datetime
from random import randrange

from enums.CommandsEnum import CommandsEnum
from enums.EmojiEnum import EmojiEnum


class LoopService:

    def __init__(self, bot, logging_service):
        self.bot = bot
        self.logging_service = logging_service
        self.word_of_the_day_occurred = False
        self.WORD_OF_THE_DAY_TIME = 9
        self.times_randomly_messaged = 0
        self.MAX_TIMES_TO_RANDOMLY_MESSAGE = 4
        self.ONE_HOUR_IN_SECONDS = 3600
        self.HELEN_MODIFIER = 8

    def init_loops(self):
        self.bot.loop.create_task(self.daily_word_of_the_day())
        self.bot.loop.create_task(self.random_messages())

    async def random_messages(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            now = datetime.now().utcnow()
            if self.time_in_range(23, 1, now):
                self.times_randomly_messaged = 0
            time_to_wait = self.ONE_HOUR_IN_SECONDS * self.HELEN_MODIFIER
            # time_to_wait = randrange(self.ONE_HOUR_IN_SECONDS * self.HELEN_MODIFIER) + self.times_randomly_messaged * 100
            self.logging_service.log(f'Time until next random message: {time_to_wait}, Times messaged today: {self.times_randomly_messaged}')
            await asyncio.sleep(time_to_wait)
            if not self.is_too_many_messages():
                self.logging_service.log_starting_progress(CommandsEnum.RANDOM_MESSAGE.value)
                for guild in self.bot.guilds:
                    await self.send_random_message_to_server(guild)
                self.times_randomly_messaged += 1

    async def send_random_message_to_server(self, guild):
        messages = await self.get_possible_messages(guild)
        random_message_index = randrange(len(messages))
        random_message = messages[random_message_index]
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

    @staticmethod
    async def get_possible_messages(guild):
        messages = list()
        messages.append("Did you find it?")
        messages.append("I'm not sure")
        messages.append("How does that make you feel?")
        messages.append("Bonk Giannaki")
        messages.append("No")
        messages.append("ye")
        messages.append("Follow the white rabbit")
        messages.append("Maybe")
        messages.append("Look left")
        messages.append("Bad idea")
        messages.append("As you wish")
        messages.append("Sometimes the question itself is the answer")
        messages.append("Better ask yourself")
        messages.append("What do you think?")
        messages.append("Just relax")
        messages.append("Who knows with these crazy kids")
        messages.append("That's hard to answer")
        messages.append("It depends")
        messages.append("I am the Alpha and the Omega, the First and the Last, the Beginning and the End.")
        messages.append("I don't think that's how it works")
        bonk = await EmojiEnum.get_custom_emoji(guild.emojis, EmojiEnum.BONK.value)
        messages.append(bonk)
        total_random_emojis = int(len(messages) / 4)
        for i in range(total_random_emojis):
            random_emoji_index = randrange(len(guild.emojis))
            random_emoji = guild.emojis[random_emoji_index]
            messages.append(random_emoji)
        return messages

    async def daily_word_of_the_day(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.logging_service.log(f'Attempting daily {CommandsEnum.WORD_OF_THE_DAY.value}')
            now = datetime.now().utcnow()
            if now.hour == self.WORD_OF_THE_DAY_TIME - 1:
                self.word_of_the_day_occurred = False
                self.logging_service.log(f'Setting word_of_the_day_occurred to false, {self.word_of_the_day_occurred}')
            if now.hour == self.WORD_OF_THE_DAY_TIME and not self.word_of_the_day_occurred:
                guilds = self.bot.guilds
                for guild in guilds:
                    for channel in guild.text_channels:
                        if channel.name == "general":
                            self.logging_service.log_starting_progress(CommandsEnum.WORD_OF_THE_DAY.value)
                            emoji = await EmojiEnum.get_custom_emoji(channel.guild.emojis, EmojiEnum.BONK.value)
                            message = await channel.send("Word of the day: bonk")
                            await message.add_reaction(emoji)
                self.word_of_the_day_occurred = True
                self.logging_service.log(f'Setting word_of_the_day_occurred to true, {self.word_of_the_day_occurred}')

            await asyncio.sleep(60 * 55)  # wait 55 minutes