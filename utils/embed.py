import discord


class Embed:
    @staticmethod
    def check(title=None, description=None) -> discord.Embed:
        embed = discord.Embed(
            title="✅ {}".format(title),
            description="{}".format(description),
            color=0x1DC73A,
        )
        return embed

    @staticmethod
    def warn(title=None, description=None) -> discord.Embed:
        embed = discord.Embed(
            title="⚠ {}".format(title),
            description="{}".format(description),
            color=0xD8EF56,
        )
        return embed

    @staticmethod
    def error(title=None, description=None) -> discord.Embed:
        embed = discord.Embed(
            title="❌ {}".format(title),
            description="{}".format(description),
            color=0xFF0909,
        )
        return embed
