from pprint import pprint
from typing import List, Mapping, Optional

import discord
from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import Command, command
from EZPaginator import Paginator


class Help(commands.HelpCommand):
    def __init__(self) -> None:
        super().__init__(command_attrs={"aliases": ["도움"]})

    # TODO : 기본 HelpCommand로 조물딱 할 수 있게 해보기

    async def send_bot_help(
        self, mapping: Mapping[Optional[Cog], List[Command]]
    ) -> None:
        ctx = self.context

        embeds = []
        for i, j in mapping.items():
            command_arr = [f"`{x.qualified_name}`" for x in j]
            embed = discord.Embed(
                title="📰 도움말", description="자세한 도움말을 보려면 `봇 도움 (명령어 이름)`을 사용하세요.", color=0x237CCD,
            )
            embed.add_field(
                name=f"{i.qualified_name}" if not i is None else "None",
                value=", ".join(command_arr),
            )
            embeds.append(embed)

        msg = await ctx.send(embed=embeds[0])
        page = Paginator(
            self.context.bot,
            msg,
            embeds=embeds,
            use_more=True,
            only=ctx.author,
        )
        await page.start()

    async def send_command_help(self, command:Command) -> None:
        
