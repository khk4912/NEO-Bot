from discord.ext.commands import Command


class NotAllowedStatusException(Exception):
    def __init__(self, status_code: int) -> None:
        super().__init__(f"Status Code {status_code}")


class FailedToParseException(Exception):
    def __init__(self, command: Command) -> None:
        super().__init__(f"{Command.qualified_name}")
