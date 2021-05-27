from discord import File

from enums.EmojiEnum import EmojiEnum
from enums.GoodBonkoResponseEnum import GoodBonkoResponseEnum
from enums.ResponseTypeEnum import ResponseTypeEnum


class RandomResponseService:

    async def send_response(self, ctx, response_type_enum):
        if ResponseTypeEnum.is_good_bonko(response_type_enum.value.id):
            await self.send_random_good_bonk_response(ctx)
        elif ResponseTypeEnum.is_ye(response_type_enum.value.id):
            await self.send_ye_response(ctx)

    @staticmethod
    async def send_random_good_bonk_response(ctx):
        response = GoodBonkoResponseEnum.get_random_response()
        if isinstance(response, File):
            await ctx.channel.send(file=response)
        else:
            await ctx.channel.send(response)

    @staticmethod
    async def send_ye_response(ctx):
        message = await ctx.channel.send("tuc crackers + cottage cheese")
        emoji = await EmojiEnum.get_custom_emoji(ctx.guild.emojis, EmojiEnum.SNACCS.value)
        await message.add_reaction(emoji)


        # "Did you find it?"
        # "I'm not sure"
        # "How does that make you feel?"
        # "Bonk Giannaki"
        # "No"