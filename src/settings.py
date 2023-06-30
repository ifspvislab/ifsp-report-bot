"""
settings
========

This module provides functionality for retrieving a Discord Bot token from environment variables.

Functions:
    - get_discord_bot_token(): Retrieve the Discord Bot token from the environment variables.
    
"""
import logging
import os
import zoneinfo

# from decouple import config
# DISCORD_BOT_TOKEN = config("DISCORD_BOT_TOKEN")

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


def get_coordinator_id() -> int:
    """
    Retrieve the admin bot id from the environment variables.
    :return: COORDINATOR_DISCORD_ID.
    :rtype: int
    :raises KeyError: If the 'COORDINATOR_DISCORD_ID' environment variable does not exist.
    """
    discord_coordinator_id = os.getenv("COORDINATOR_DISCORD_ID")
    if discord_coordinator_id is None:
        raise KeyError(
            "The requested environment variable 'COORDINATOR_DISCORD_ID' does not exist"
        )
    return discord_coordinator_id


def get_time_zone():
    """
    Retrieve the time zone.

    Returns:
        zoneinfo.ZoneInfo: The time zone representing 'America/Sao_Paulo'.
    """
    return zoneinfo.ZoneInfo("America/Sao_Paulo")
