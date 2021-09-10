from dataclasses import dataclass
from enum import Enum

from enums.SentimentEnum import SentimentEnum


@dataclass
class OnMessageResponseType:
    id: int
    value: str
    sentiment: SentimentEnum


class OnMessageResponseTypeEnum(Enum):
    GOOD_BONKO = OnMessageResponseType(0, "good bonko", SentimentEnum.HAPPY)

    YE = OnMessageResponseType(1, "ye", SentimentEnum.NEUTRAL)

    BAD_BONKO = OnMessageResponseType(2, "bad bonko", SentimentEnum.SAD)

    NAUGHTY_BONKO = OnMessageResponseType(3, "naughty bonko", SentimentEnum.SAD)

    BAUGHTY_BONKO = OnMessageResponseType(4, "baughty bonko", SentimentEnum.SAD)

    YEAH = OnMessageResponseType(5, "yeah", SentimentEnum.NEUTRAL)

    FOTIA = OnMessageResponseType(6, "🔥", SentimentEnum.NEUTRAL)

    MAXERI = OnMessageResponseType(7, "🔪", SentimentEnum.NEUTRAL)

    ASPIS = OnMessageResponseType(8, "🛡️", SentimentEnum.NEUTRAL)

    YEA = OnMessageResponseType(9, "yea", SentimentEnum.NEUTRAL)

    EY = OnMessageResponseType(10, "ey", SentimentEnum.NEUTRAL)

    GOOD_ANTI_BONKO = OnMessageResponseType(10, "good antibonko", SentimentEnum.NEUTRAL)

    @staticmethod
    def is_good_bonko(id):
        return OnMessageResponseTypeEnum.get_from_id(id).value.sentiment == SentimentEnum.HAPPY

    @staticmethod
    def is_ye(id):
        return id == OnMessageResponseTypeEnum.YE.value.id


    @staticmethod
    def is_bad_bonko(id):
        return OnMessageResponseTypeEnum.get_from_id(id).value.sentiment == SentimentEnum.SAD

    @staticmethod
    def is_yeah(id):
        return id == OnMessageResponseTypeEnum.YEAH.value.id

    @staticmethod
    def is_yea(id):
        return id == OnMessageResponseTypeEnum.YEA.value.id

    @staticmethod
    def is_ey(id):
        return id == OnMessageResponseTypeEnum.EY.value.id

    @staticmethod
    def is_good_anti_bonko(id):
        return id == OnMessageResponseTypeEnum.GOOD_ANTI_BONKO.value.id

    @staticmethod
    def is_fotia_maxeri_aspis(id):
        return id == OnMessageResponseTypeEnum.FOTIA.value.id or id == OnMessageResponseTypeEnum.MAXERI.value.id or id == OnMessageResponseTypeEnum.ASPIS.value.id

    @staticmethod
    def is_startswith_ye(message):
        return message.startswith(OnMessageResponseTypeEnum.YE.value.value)

    @staticmethod
    def get_from_message(message):
        for enum in OnMessageResponseTypeEnum:
            if enum.value.value == message:
                return enum
        # if OnMessageResponseTypeEnum.is_startswith_ye(message):
        #     return OnMessageResponseTypeEnum.YEAH

    @staticmethod
    def get_from_id(id):
        for enum in OnMessageResponseTypeEnum:
            if enum.value.id == id:
                return enum
