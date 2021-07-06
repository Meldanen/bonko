from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from random import randrange

from enums.EmojiEnum import EmojiEnum
from enums.UserEnum import UserEnum
from utils import FileUtils


@dataclass
class RandomQuote:
    id: int
    quote: str
    reaction: str
    file: bool


class RandomQuoteEnum(Enum):
    RANDOM_RANDOM = RandomQuote(0, None, EmojiEnum.WISENAKIS, False)

    INTELIGENE = RandomQuote(1, "\"I didn't borned with inteligene\" ~ glennakios 2020", EmojiEnum.WISENAKIS, False)

    SIMPLE = RandomQuote(2,
                         " I can find joy in simplicity. I dont care if my computer needs 2 minutes to boot. I dont care if my pc is a but slower. Xalara, i dont have the feeling that i need  an ssd. I am stoikos. My computer is good enough for me. It is not the best computer out there, it has its speed issues, but i am stoikos. I accept that issue , i am fine with it",
                         EmojiEnum.WISENAKIS, False)

    MOUSE = RandomQuote(3,
                        "tested by me. i play a lot of mmo's and reached high end game  on wow. not just ok i am good so, u r telling me, the  best mmo button, deserves to be on  lowest tier list?",
                        EmojiEnum.WISENAKIS, False)

    CAUCH = RandomQuote(4,
                        "u r naked on your cauch, having sex with your boyfriend. i came by knocked your door not very loud. u didnt hear it, and i open oyur door and find u naked on the couch with a dick inside u. i am very sure u would be  very okish with that. u wouldnt throw the couch on my head but anw. i personally dont like this at all ",
                        EmojiEnum.WISENAKIS, False)

    MEXIOCRITY = RandomQuote(5,
                             "I really dont see the diference  etween simplicity , cause in the end of the day they both helong in the big picture whicth u cant just see but sure, if u want to call it mexiocrity, then ok its mediocrity",
                             EmojiEnum.WISENAKIS, False)

    ANTONIO = RandomQuote(6, "antonio frena!  frena frena!! antonio!! frena!! ANTONIO FRENA!!!", EmojiEnum.WISENAKIS,
                          False)

    ANCHIEVE = RandomQuote(7,
                           "I am gianniscand i am proud to call me a happy person ( or mediorce  as u would call it) that spent my life in missery cause i will always strive for something i will never anchieve, perfection",
                           EmojiEnum.WISENAKIS, False)

    DELICANCY = RandomQuote(8, "sucha  complicate delicancy, not chocolates simplicity", EmojiEnum.WISENAKIS, False)

    X_D = RandomQuote(9,
                      "also, sibl corrected 1 of my mistakes, whitch means she readed it - and if sibl ignored it/ didnt got triggered enough by it, it means its not that bad xD",
                      EmojiEnum.WISENAKIS, False)

    PROSTITUE = RandomQuote(10,
                            "u are a prostitute and u sell your body? i dont see it asa human. i see it as an object.  in this world when u pay for THINGS, u get things. u wanna sell your body? your body now is a thing, its an item an item that i booked down for the next 30m. u want to sell service? fullfill your services",
                            EmojiEnum.WISENAKIS, False)

    PUSSY = RandomQuote(11, "assets/images/pussy.png", EmojiEnum.WISENAKIS, True)

    PANGEA = RandomQuote(12,
                         "i know what pangea is... u know what. fuck this shit... i am not gonna bother... sure ok u r right it feels like u dont even bother to read what i say, thats what getting me upset.... i understant , maybe its  alanguage barrier again- thats why i am like just let it go",
                         EmojiEnum.WISENAKIS, False)

    EXPERTISE = RandomQuote(13,
                            "but again. u testing my expertise on the english language. if u judge me over 1 misshear, imo thats wrong. cause that has nothing to do with  my expertise in the language. if during the whole interview i was like: what? could u repeat that? then yes",
                            EmojiEnum.WISENAKIS, False)

    PLANTS = RandomQuote(14, "ah! i see, its sinep in reverse. makes sense why plants are green then",
                         EmojiEnum.WISENAKIS, False)

    BOOTY = RandomQuote(15, "my eyes will lead me to your booty, like the nose lead a cartoon character to a pie", EmojiEnum.WISENAKIS, False)

    @staticmethod
    async def get_random_quote(ctx, user_id):
        index = randrange(len(RandomQuoteEnum))
        return await RandomQuoteEnum.get_quote(ctx, index, user_id)

    @staticmethod
    async def get_quote(ctx, id, user_id):
        quote = RandomQuoteEnum.get_by_id(id)
        if quote == RandomQuoteEnum.RANDOM_RANDOM:
            return await RandomQuoteEnum.get_random_quote_from_history(ctx, user_id)
        elif quote.value.file:
            return FileUtils.get_file(quote.value.quote)
        else:
            return quote.value

    @staticmethod
    def get_by_id(id):
        for enum in RandomQuoteEnum:
            if enum.value.id == id:
                return enum

    @staticmethod
    async def get_random_quote_from_history(ctx, user_id):
        messages = list()
        for channel in ctx.guild.text_channels:
            channel_creation = int(channel.created_at.timestamp())
            now = int(datetime.now().utcnow().timestamp())
            random_start = datetime.fromtimestamp(randrange(channel_creation, now))
            async for message in channel.history(limit=101, around=random_start):
                if message.author.id == user_id:
                    messages.append(message)
        random_index = randrange(len(messages))
        message = messages[random_index]
        if message and message.content:
            return RandomQuote(0, message.content, EmojiEnum.WISENAKIS, False)
        return RandomQuoteEnum.SIMPLE.value
