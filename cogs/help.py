from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.core import Group
from utils.logs import Logs
from utils.invoke import Invoke


class Help(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.logger = Logs.create_logger(self)

    async def cog_after_invoke(self, ctx):
        await Invoke.after_invoke(ctx, self.logger)

    @commands.command(name="help", aliases=["도움", "도움말"])
    async def help(self, ctx, command=None):
        embeds = []
        for i, j in ctx.bot.cogs.items():
            command_arr = [
                "\n".join([x.name for y in x.commands])
                if isinstance(x, commands.Group)
                else f"{x.name}"
                for x in j.walk_commands()
            ]
            embed = discord.Embed(
                title=f"📰 {i} 도움말",
                description="\n".join(command_arr),
                color=0x237CCD,
            )
            embeds.append(embed)

        await ctx.send(embed=embeds[0])


def setup(bot) -> None:
    bot.add_cog(Help(bot))
