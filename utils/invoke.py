import discord
from functools import wraps
from logging import Logger


class Invoke:
    @staticmethod
    async def after_invoke(ctx, logger: Logger) -> None:
        logger.info(f"Command {ctx.command} used by {ctx.author}")


def with_typing(f):
    @wraps(f)
    async def wrapper(*args, **kwargs) -> None:
        ctx = args[1]
        async with ctx.channel.typing():
            return await f(*args, **kwargs)

    return wrapper


def need_chunk(f):
    @wraps(f)
    async def wrapper(*args, **kwargs) -> None:
        ctx = args[1]
        if not ctx.guild.chunked:
            embed = discord.Embed(
                title="🔄 길드 캐싱 중...",
                description="이 작업을 수행하기 위해 길드를 캐싱하고 있어요...\n상황에 따라 많은 시간이 소요될 수 있어요!",
                color=0x237CCD,
            )
            msg = await ctx.send(embed=embed)
            await ctx.guild.chunk()
            await msg.delete()
        return await f(*args, **kwargs)

    return wrapper
