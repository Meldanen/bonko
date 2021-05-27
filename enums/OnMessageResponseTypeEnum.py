from dataclasses import dataclass
from enum import Enum


@dataclass
class OnMessageResponseType:
    id: int
    value: str


class OnMessageResponseTypeEnum(Enum):
    GOOD_BONKO = OnMessageResponseType(0, "good bonko")

    YE = OnMessageResponseType(1, "ye")

    @staticmethod
    def is_good_bonko(id):
        return id == OnMessageResponseTypeEnum.GOOD_BONKO.value.id

    @staticmethod
    def is_ye(id):
        return id == OnMessageResponseTypeEnum.YE.value.id

    @staticmethod
    def get_from_message(message):
        for enum in OnMessageResponseTypeEnum:
            if enum.value.value == message:
                return enum
