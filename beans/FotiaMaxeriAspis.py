from dataclasses import dataclass

from enums.EmojiEnum import EmojiEnum


@dataclass
class FotiaMaxeriAspis:
    id: int
    display: str
    emoji: EmojiEnum
