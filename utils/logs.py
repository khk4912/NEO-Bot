import logging
from CONFIG import PRI_FORMATTER
from discord.ext.commands.bot import Cog, HelpCommand


class Logs:
    @staticmethod
    def create_logger(cog: Cog) -> logging.Logger:
        logger = logging.getLogger(cog.qualified_name)
        logger.setLevel(logging.DEBUG)

        if logger.hasHandlers():
            logger.handlers.clear()

        formatter = PRI_FORMATTER

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(
            f"Logs/{cog.qualified_name}.txt", "w"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        logger.info(f"{cog.qualified_name} Logger Loaded.")

        return logger

    @staticmethod
    def main_logger() -> logging.Logger:
        logger = logging.getLogger("discord")
        logger.setLevel(logging.INFO)

        formatter = PRI_FORMATTER

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(f"Logs/Main.txt", "w")
        file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        logger.info(f"Main Logger Loaded.")

        return logger
