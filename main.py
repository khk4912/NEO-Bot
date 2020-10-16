import discord
from discord.ext import commands

import CONFIG
from utils.logs import Logs
from db import DBHandler


class Main(commands.AutoShardedBot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=["봇 ", "봇"],
            help_command=None,
            intents=discord.Intents(members=True).default(),
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


bot = Main()
bot.run(CONFIG.BOT_TOKEN)
