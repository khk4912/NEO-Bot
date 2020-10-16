from logging import Logger


class Invoke:
    @staticmethod
    async def after_invoke(ctx, logger: Logger) -> None:
        logger.info(f"Command {ctx.command} used by {ctx.author}")
