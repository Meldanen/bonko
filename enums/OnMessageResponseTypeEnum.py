from dataclasses import dataclass
from enum import Enum


@dataclass
class OnMessageResponseType:
    id: int
    value: str


class OnMessageResponseTypeEnum(Enum):
    GOOD_BONKO = OnMessageResponseType(0, "good bonko")

    YE = OnMessageResponseType(1, "ye")

    BAD_BONKO = OnMessageResponseType(2, "bad bonko")

    NAUGHTY_BONKO = OnMessageResponseType(3, "naughty bonko")

    BAUGHTY_BONKO = OnMessageResponseType(4, "baughty bonko")

    @staticmethod
    def is_good_bonko(id):
        return id == OnMessageResponseTypeEnum.GOOD_BONKO.value.id

    @staticmethod
    def is_ye(id):
        return id == OnMessageResponseTypeEnum.YE.value.id

    @staticmethod
    def is_bad_bonko(id):
        return id == OnMessageResponseTypeEnum.BAD_BONKO.value.id or id == OnMessageResponseTypeEnum.NAUGHTY_BONKO.value.id or id == OnMessageResponseTypeEnum.BAUGHTY_BONKO.value.id

    @staticmethod
    def get_from_message(message):
        for enum in OnMessageResponseTypeEnum:
            if enum.value.value == message:
                return enum
