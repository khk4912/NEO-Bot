from logging import error

import discord
from discord.ext import commands

import CONFIG
from CONFIG import INIT_INTENTS
from db import DBHandler
from utils.embed import Embed
from utils.logs import Logs
from cogs.test_help import TestHelp


class Main(commands.AutoShardedBot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=["봇 ", "봇"],
            help_command=TestHelp(),
            intents=INIT_INTENTS,
            chunk_guilds_at_startup=False,
        )

        self.logger = Logs.main_logger()
        self.db = None

        self.loop.create_task(self._create_db())

        for i in CONFIG.INITIAL_COGS:
            self.load_extension(i)

    async def _create_db(self) -> None:
        db = DBHandler(self.loop)
        await db.make_pool()
        self.db = db

    async def on_ready(self) -> None:
        self.logger.info("Bot Ready.")

    async def on_message(self, message) -> None:
        if message.author.bot:
            return

        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.CommandOnCooldown):
            embed = Embed.warn(
                title="⚠ 쿨타임 중!",
                description=f"{int(error.retry_after)}초 뒤에 재시도하세요.",
            )
            await ctx.send(embed=embed)


bot = Main()
bot.run(CONFIG.BOT_TOKEN)
