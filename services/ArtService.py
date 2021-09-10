from enums.AsciiArtEnum import AsciiArtEnum
from enums.EmojiEnum import EmojiEnum


class ArtService:

    async def get_sibling_art(self, ctx, fart_on_emojis):
        head = await self.get_emoji(ctx, "sibling")
        neck = await self.get_emoji(ctx, "giraffe")
        ass = await self.get_emoji(ctx, "peach")
        ass += await self.get_emoji(ctx, "dash")
        if fart_on_emojis:
            for fart_on_emoji in fart_on_emojis:
                emoji = await self.get_emoji(ctx, fart_on_emoji)
                if emoji:
                    ass += str(emoji)
        leg = await self.get_emoji(ctx, "leg_tone3")
        return head, neck, ass, leg

    async def get_lemonaris_art(self, ctx, fart_on_emojis):
        head = self.add_spaces("", 7)
        head += str(await self.get_emoji(ctx, "hue"))

        torso = "\u200b "
        torso += await self.get_emoji(ctx, "muscle_tone1")
        torso += await self.get_emoji(ctx, "lemon")
        torso += await self.get_emoji(ctx, "muscle_tone1")
        ass = self.add_spaces("", 7)
        ass += await self.get_emoji(ctx, "peach")
        ass += await self.get_emoji(ctx, "dash")
        if fart_on_emojis:
            for fart_on_emoji in fart_on_emojis:
                emoji = await self.get_emoji(ctx, fart_on_emoji)
                if emoji:
                    ass += str(emoji)
        leg = self.add_spaces("", 4)
        leg += await self.get_emoji(ctx, "leg_tone1")
        leg += await self.get_emoji(ctx, "leg_tone1")
        return f'{head}\n{torso}\n{ass}\n{leg}'

    @staticmethod
    def add_spaces(message, number_of_spaces):
        if not message:
            message = ""
        for i in range(number_of_spaces):
            message += "\u200b "
        return message

    @staticmethod
    def get_omega_bonk():
        return AsciiArtEnum.OMEGA_BONK.value

    @staticmethod
    def get_salt():
        return AsciiArtEnum.SALT.value

    @staticmethod
    def get_emoji(ctx, emoji):
        return EmojiEnum.get_emoji(ctx.guild.emojis, emoji)
