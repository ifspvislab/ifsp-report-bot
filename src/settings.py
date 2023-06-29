"""
settings
========

This module provides functionality for retrieving a Discord Bot token from environment variables.

Functions:
    - get_discord_bot_token(): Retrieve the Discord Bot token from the environment variables.
    
"""
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s --- [%(filename)s | %(funcName)s] : %(message)s",
)


def get_discord_bot_token() -> str:
    """
    Retrieve the Discord Bot token from the environment variables.

    :return: The Discord Bot token.
    :rtype: str

    :raises KeyError: If the 'DISCORD_BOT_TOKEN' environment variable does not exist.
    """
    discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
    if discord_bot_token is None:
        raise KeyError(
            "The requested environment variable 'DISCORD_BOT_TOKEN' does not exist"
        )
    return discord_bot_token


def get_admin_id() -> int:
    discord_admin_id = os.getenv("ADMIN_DISCORD_ID")
    if discord_admin_id is None:
        raise KeyError(
            "The requested environment variable 'ADMIN_DISCORD_ID' does not exist"
        )
    return discord_admin_id
