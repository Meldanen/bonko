from enum import Enum
from discord import Emoji as CustomEmoji
from discord.utils import get
from emojis.db import Emoji as DefaultEmoji
import emojis


class EmojiEnum(Enum):
    BONK = "bonk"

    ANGRY = "angry"

    OPEN_MOUTH = "open_mouth"

    @staticmethod
    async def get_emoji(guild_emojis: list(), emoji):
        if isinstance(emoji, CustomEmoji):
            return emoji
        elif isinstance(emoji, DefaultEmoji):
            return emoji.emoji
        else:
            custom_emoji = await EmojiEnum.get_custom_emoji(guild_emojis, emoji)
        if custom_emoji is not None:
            return custom_emoji
        return emojis.encode(f':{emoji}:')

    @staticmethod
    async def get_custom_emoji(guild_emojis: list(), emoji):
        return get(guild_emojis, name=emoji)
