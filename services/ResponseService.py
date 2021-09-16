from discord import File

from enums.EmojiEnum import EmojiEnum
from enums.FotiaMaxeriAspisEnum import FotiaMaxeriAspisEnum
from enums.JudgeBonkoResponseEnum import JudgeBonkoResponseEnum
from enums.OnMessageResponseTypeEnum import OnMessageResponseTypeEnum
from enums.UserEnum import UserEnum


class ResponseService:

    async def send_response(self, ctx, response_type_enum):
        if OnMessageResponseTypeEnum.is_good_bonko(response_type_enum.value.id):
            await self.send_random_good_bonko_response(ctx.channel)
        # elif OnMessageResponseTypeEnum.is_ye(response_type_enum.value.id):
        #     await self.send_ye_response(ctx.channel, ctx.guild)
        elif OnMessageResponseTypeEnum.is_bad_bonko(response_type_enum.value.id):
            await self.send_random_bad_bonko_response(ctx.channel)
        # elif OnMessageResponseTypeEnum.is_yeah(response_type_enum.value.id) or OnMessageResponseTypeEnum.is_yea(
        #         response_type_enum.value.id):
        #     await self.send_yeah_response(ctx.author.id, ctx.channel, ctx.guild)
        elif OnMessageResponseTypeEnum.is_fotia_maxeri_aspis(response_type_enum.value.id):
            await self.send_reaction(ctx, response_type_enum)
        elif OnMessageResponseTypeEnum.is_ey(response_type_enum.value.id):
            await self.send_yeah_response(ctx.author.id, ctx.channel, ctx.guild, True)
        elif OnMessageResponseTypeEnum.is_good_anti_bonko(response_type_enum.value.id):
            await self.send_good_anti_bonko_response(ctx.channel)
        elif OnMessageResponseTypeEnum.is_hyperfeminine_villoui(response_type_enum.value.id):
            await self.send_hyperfeminine_villoui_response(ctx)

    async def send_random_good_bonko_response(self, channel):
        response = JudgeBonkoResponseEnum.get_random_happy_response()
        await self.send(channel, response)

    async def send_random_bad_bonko_response(self, channel):
        response = JudgeBonkoResponseEnum.get_random_sad_response()
        await self.send(channel, response)

    async def send_random_response(self, channel):
        response = JudgeBonkoResponseEnum.get_random_response()
        await self.send(channel, response)

    async def send_good_anti_bonko_response(self, channel):
        response = JudgeBonkoResponseEnum.EYES.value.value
        await self.send(channel, response)

    async def send(self, channel, response):
        if isinstance(response, File):
            await channel.send(file=response)
        else:
            await channel.send(response)

    async def send_hyperfeminine_villoui_response(self, ctx):
        channel = ctx.channel
        guild = ctx.guild
        # message = await channel.send(";)")
        emoji = await EmojiEnum.get_custom_emoji(guild.emojis, EmojiEnum.YENS.value)
        # await message.add_reaction(emoji)
        await ctx.add_reaction(emoji)

    @staticmethod
    async def send_ye_response(channel, guild):
        # message = await channel.send("tuc crackers + cottage cheese")
        message = await channel.send("anaraes + digestives")
        emoji = await EmojiEnum.get_custom_emoji(guild.emojis, EmojiEnum.SNACCS.value)
        await message.add_reaction(emoji)

    @staticmethod
    async def send_yeah_response(user_id, channel, guild, reverse=False):
        if not UserEnum.is_nyroid(user_id):
            return
        text = "Did you mean: ye"
        if reverse:
            text = text[::-1]
        message = await channel.send(text)
        emoji = await EmojiEnum.get_custom_emoji(guild.emojis, EmojiEnum.SNACCS.value)
        await message.add_reaction(emoji)

    @staticmethod
    async def send_reaction(ctx, response_type_enum):
        reaction = FotiaMaxeriAspisEnum.get_winning_emoji(response_type_enum.value.value).value.display
        await ctx.add_reaction(reaction)
