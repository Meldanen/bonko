from discord import File

from enums.EmojiEnum import EmojiEnum
from enums.GoodBonkoResponseEnum import GoodBonkoResponseEnum
from enums.OnMessageResponseTypeEnum import OnMessageResponseTypeEnum


class ResponseService:

    async def send_response(self, ctx, response_type_enum):
        if OnMessageResponseTypeEnum.is_good_bonko(response_type_enum.value.id):
            await self.send_random_good_bonk_response(ctx.channel)
        elif OnMessageResponseTypeEnum.is_ye(response_type_enum.value.id):
            await self.send_ye_response(ctx.channel, ctx.guild)

    @staticmethod
    async def send_random_good_bonk_response(channel):
        response = GoodBonkoResponseEnum.get_random_response()
        if isinstance(response, File):
            await channel.send(file=response)
        else:
            await channel.send(response)

    @staticmethod
    async def send_ye_response(channel, guild):
        message = await channel.send("tuc crackers + cottage cheese")
        emoji = await EmojiEnum.get_custom_emoji(guild.emojis, EmojiEnum.SNACCS.value)
        await message.add_reaction(emoji)
