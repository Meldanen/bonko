from enum import Enum

from beans.FotiaMaxeriAspis import FotiaMaxeriAspis
from enums.EmojiEnum import EmojiEnum


class FotiaMaxeriAspisEnum(Enum):
    FOTIA = FotiaMaxeriAspis(0, "🔥", EmojiEnum.FIRE)

    MAXERI = FotiaMaxeriAspis(1, "🔪", EmojiEnum.KNIFE)

    ASPIS = FotiaMaxeriAspis(2, "🛡️", EmojiEnum.SHIELD)

    @staticmethod
    def get_from_display(display):
        for enum in FotiaMaxeriAspisEnum:
            if enum.value.value == display:
                return enum

    @staticmethod
    def get_from_id(id):
        for enum in FotiaMaxeriAspisEnum:
            if enum.value.id == id:
                return enum

    @staticmethod
    def get_from_emoji(emoji):
        for enum in FotiaMaxeriAspisEnum:
            if enum.value.emojis.value == emoji:
                return enum

    @staticmethod
    def get_winning_emoji(display):
        if display == FotiaMaxeriAspisEnum.FOTIA.value.display:
            return FotiaMaxeriAspisEnum.MAXERI
        if display == FotiaMaxeriAspisEnum.MAXERI.value.display:
            return FotiaMaxeriAspisEnum.ASPIS
        if display == FotiaMaxeriAspisEnum.ASPIS.value.display:
            return FotiaMaxeriAspisEnum.FOTIA
