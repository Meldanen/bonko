from discord import File

from enums.EmojiEnum import EmojiEnum
from enums.FotiaMaxeriAspisEnum import FotiaMaxeriAspisEnum
from enums.JudgeBonkoResponseEnum import JudgeBonkoResponseEnum
from enums.OnMessageResponseTypeEnum import OnMessageResponseTypeEnum


class ResponseService:

    async def send_response(self, ctx, response_type_enum):
        if OnMessageResponseTypeEnum.is_good_bonko(response_type_enum.value.id):
            await self.send_random_good_bonko_response(ctx.channel)
        elif OnMessageResponseTypeEnum.is_ye(response_type_enum.value.id):
            await self.send_ye_response(ctx.channel, ctx.guild)
        elif OnMessageResponseTypeEnum.is_bad_bonko(response_type_enum.value.id):
            await self.send_random_bad_bonko_response(ctx.channel)
        elif OnMessageResponseTypeEnum.is_yeah(response_type_enum.value.id):
            await self.send_yeah_response(ctx.channel, ctx.guild)
        elif OnMessageResponseTypeEnum.is_fotia_maxeri_aspis(response_type_enum.value.id):
            await self.send_reaction(ctx, response_type_enum)

    async def send_random_good_bonko_response(self, channel):
        response = JudgeBonkoResponseEnum.get_random_happy_response()
        await self.send(channel, response)

    async def send_random_bad_bonko_response(self, channel):
        response = JudgeBonkoResponseEnum.get_random_sad_response()
        await self.send(channel, response)

    async def send_random_response(self, channel):
        response = JudgeBonkoResponseEnum.get_random_response()
        await self.send(channel, response)

    async def send(self, channel, response):
        if isinstance(response, File):
            await channel.send(file=response)
        else:
            await channel.send(response)

    @staticmethod
    async def send_ye_response(channel, guild):
        message = await channel.send("tuc crackers + cottage cheese")
        emoji = await EmojiEnum.get_custom_emoji(guild.emojis, EmojiEnum.SNACCS.value)
        await message.add_reaction(emoji)

    @staticmethod
    async def send_yeah_response(channel, guild):
        message = await channel.send("Did you mean: ye")
        emoji = await EmojiEnum.get_custom_emoji(guild.emojis, EmojiEnum.SNACCS.value)
        await message.add_reaction(emoji)

    @staticmethod
    async def send_reaction(ctx, response_type_enum):
        reaction = FotiaMaxeriAspisEnum.get_winning_emoji(response_type_enum.value.value).value.display
        await ctx.add_reaction(reaction)
