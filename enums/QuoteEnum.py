from datetime import datetime
from enum import Enum
from random import randrange

from beans.Quote import Quote
from enums.DateFormatEnum import DateFormatEnum
from enums.EmojiEnum import EmojiEnum
from utils import FileUtils


class QuoteEnum(Enum):
    RANDOM = Quote(0, None, EmojiEnum.WISENYRAKIS, False)

    INTELIGENE = Quote(1, "\"I didn't borned with inteligene\" ~ glennakios 2020", EmojiEnum.WISENYRAKIS, False)

    SIMPLE = Quote(2,
                   " I can find joy in simplicity. I dont care if my computer needs 2 minutes to boot. I dont care if my pc is a but slower. Xalara, i dont have the feeling that i need  an ssd. I am stoikos. My computer is good enough for me. It is not the best computer out there, it has its speed issues, but i am stoikos. I accept that issue , i am fine with it",
                   EmojiEnum.WISENYRAKIS, False)

    MOUSE = Quote(3,
                  "tested by me. i play a lot of mmo's and reached high end game  on wow. not just ok i am good so, u r telling me, the  best mmo button, deserves to be on  lowest tier list?",
                  EmojiEnum.WISENYRAKIS, False)

    CAUCH = Quote(4,
                  "u r naked on your cauch, having sex with your boyfriend. i came by knocked your door not very loud. u didnt hear it, and i open oyur door and find u naked on the couch with a dick inside u. i am very sure u would be  very okish with that. u wouldnt throw the couch on my head but anw. i personally dont like this at all ",
                  EmojiEnum.WISENYRAKIS, False)

    MEXIOCRITY = Quote(5,
                       "I really dont see the diference  etween simplicity , cause in the end of the day they both helong in the big picture whicth u cant just see but sure, if u want to call it mexiocrity, then ok its mediocrity",
                       EmojiEnum.WISENYRAKIS, False)

    ANTONIO = Quote(6, "antonio frena!  frena frena!! antonio!! frena!! ANTONIO FRENA!!!", EmojiEnum.WISENYRAKIS,
                    False)

    ANCHIEVE = Quote(7,
                     "I am gianniscand i am proud to call me a happy person ( or mediorce  as u would call it) that spent my life in missery cause i will always strive for something i will never anchieve, perfection",
                     EmojiEnum.WISENYRAKIS, False)

    DELICANCY = Quote(8, "sucha  complicate delicancy, not chocolates simplicity", EmojiEnum.WISENYRAKIS, False)

    X_D = Quote(9,
                "also, sibl corrected 1 of my mistakes, whitch means she readed it - and if sibl ignored it/ didnt got triggered enough by it, it means its not that bad xD",
                EmojiEnum.WISENYRAKIS, False)

    PROSTITUE = Quote(10,
                      "u are a prostitute and u sell your body? i dont see it asa human. i see it as an object.  in this world when u pay for THINGS, u get things. u wanna sell your body? your body now is a thing, its an item an item that i booked down for the next 30m. u want to sell service? fullfill your services",
                      EmojiEnum.WISENYRAKIS, False)

    PUSSY = Quote(11, "assets/images/pussy.png", EmojiEnum.WISENYRAKIS, True)

    PANGEA = Quote(12,
                   "i know what pangea is... u know what. fuck this shit... i am not gonna bother... sure ok u r right it feels like u dont even bother to read what i say, thats what getting me upset.... i understant , maybe its  alanguage barrier again- thats why i am like just let it go",
                   EmojiEnum.WISENYRAKIS, False)

    EXPERTISE = Quote(13,
                      "but again. u testing my expertise on the english language. if u judge me over 1 misshear, imo thats wrong. cause that has nothing to do with  my expertise in the language. if during the whole interview i was like: what? could u repeat that? then yes",
                      EmojiEnum.WISENYRAKIS, False)

    PLANTS = Quote(14, "ah! i see, its sinep in reverse. makes sense why plants are green then",
                   EmojiEnum.WISENYRAKIS, False)

    BOOTY = Quote(15, "my eyes will lead me to your booty, like the nose lead a cartoon character to a pie",
                  EmojiEnum.WISENYRAKIS, False)

    KARPA = Quote(16, "Men axonese kosta mou!! En na ime standby mode,etimos na sou doko KARPA", EmojiEnum.WISENYRAKIS,
                  False)

    KFC = Quote(17,
                "sure, but i know i can get an other bucket, with more meet, and when i come back from work and I AM DOWNSTAIRS, next to the kiosk, personally i will get the other bucket that they offer more value for money, and just get the bbq sauce omw  home on a personal lvl ( at least ) its not a promo :stuck_out_tongue: i just cant see it as one xD",
                EmojiEnum.WISENYRAKIS, False)

    WAR_CRIMES = Quote(18, "assets/images/war_crimes.png", EmojiEnum.SADNESS, True)

    WAR_CRIMES_CHEESE = Quote(19, "assets/images/war_crimes_cheese.png", EmojiEnum.SADNESS, True)

    ONIONS = Quote(20,
                   "there were caramelized onions!!!! cut the onions, and boil them in water... does it really matter if its boild or oiled? :stuck_out_tongue:",
                   EmojiEnum.SADNESS, False)

    GARIDAKI = Quote(21,
                   "assets/images/garidaki.png",
                   EmojiEnum.POTATO, True)

    @staticmethod
    async def get_random_quote(ctx, user_id):
        index = randrange(len(QuoteEnum))
        return await QuoteEnum.get_quote(ctx, index, user_id)

    @staticmethod
    async def get_quote(ctx, id, user_id):
        quote = QuoteEnum.get_by_id(id)
        if quote == QuoteEnum.RANDOM:
            return await QuoteEnum.get_random_quote_from_history(ctx.guild.text_channels, user_id)
        elif quote.value.file:
            return FileUtils.get_file(quote.value.quote)
        else:
            return quote.value

    @staticmethod
    def get_by_id(id):
        for enum in QuoteEnum:
            if enum.value.id == id:
                return enum

    @staticmethod
    async def get_random_quote_from_history(guild_text_channels, user_id=None):
        messages = list()
        for channel in guild_text_channels:
            channel_creation = int(channel.created_at.timestamp())
            now = int(datetime.now().utcnow().timestamp())
            random_start = datetime.fromtimestamp(randrange(channel_creation, now))
            async for message in channel.history(limit=101, around=random_start):
                if user_id and message.author.id == user_id:
                    messages.append(message)
                else:
                    messages.append(message)
        if not messages or len(messages) == 0:
            return QuoteEnum.SIMPLE.value
        random_index = randrange(len(messages))
        message = messages[random_index]
        if message and message.content:
            author = message.author.nick if message.author.nick else message.author.name
            time = DateFormatEnum.format_date_with_enum(message.created_at, DateFormatEnum.DATE_TIME)
            message = f'{message.content} ~ {author} {time}'
            return Quote(0, message, EmojiEnum.WISENYRAKIS, False)
        return QuoteEnum.SIMPLE.value
