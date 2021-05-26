from dataclasses import dataclass
from enum import Enum


@dataclass
class ResponseType:
    id: int
    value: str


class ResponseTypeEnum(Enum):
    GOOD_BONKO = ResponseType(0, "good bonko")

    RANDOM_TEXT = ResponseType(1, "random text")

    YE = ResponseType(2, "ye")

    @staticmethod
    def is_good_bonko(id):
        return id == ResponseTypeEnum.GOOD_BONKO.value.id

    @staticmethod
    def is_random_text(id):
        return id == ResponseTypeEnum.RANDOM_TEXT.value.id

    @staticmethod
    def is_ye(id):
        return id == ResponseTypeEnum.YE.value.id

    @staticmethod
    def get_from_message(message):
        for enum in ResponseTypeEnum:
            if enum.value.value == message:
                return enum
