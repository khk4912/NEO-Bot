import discord
from discord.ext import commands
from discord.ext.commands.context import Context


class TestHelp(commands.HelpCommand):
    def __init__(self) -> None:
        super().__init__(command_attrs={"aliases": ["도움"]})

    # TODO : 기본 HelpCommand로 조물딱 할 수 있게 해보기

    # async def send_bot_help(self, mapping) -> None:
    #     ctx = self.context
    #     for i,j in ctx.bot.cogs:

    #         embed = discord.Embed(
    #             title="",
    #             description="",
    #             color=0x237CCD,
    #         )

