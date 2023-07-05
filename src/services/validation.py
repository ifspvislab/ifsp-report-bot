"""
validation module
"""


class DiscordIdError(Exception):
    """
    Exception raised when an invalid Discord ID is encountered.
    """


def verify_discord_id(value: str):
    """Verify the correctness of the Discord ID.

    Args:
        value (str): The Discord ID value to be verified.

    Raises:
        DiscordIdError: If the Discord ID is invalid.
    """
    if not value.isnumeric():
        raise DiscordIdError("Discord ID inválido")
