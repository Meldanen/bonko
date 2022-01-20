from dataclasses import dataclass

from enums.EmojiEnum import EmojiEnum


@dataclass
class Quote:
    id: int
    quote: str
    reaction: EmojiEnum
    file: bool
