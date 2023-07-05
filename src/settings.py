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

DISCORD_BOT_TOKEN = 'MTExNjA5NDgwMDM5NjAyNTkzOA.GueiH_.DsW-wESRvTlYrDEjgZhUbYiihXOBoiBhF-_66E'
ADMIN_DISCORD_ID = '485131474597576724'

def get_discord_bot_token() -> str:
    """
    Retrieve the Discord Bot token from the environment variables.

    :return: The Discord Bot token.
    :rtype: str

    :raises KeyError: If the 'DISCORD_BOT_TOKEN' environment variable does not exist.
    """
    discord_bot_token = DISCORD_BOT_TOKEN
    if discord_bot_token is None:
        raise KeyError(
            "The requested environment variable 'DISCORD_BOT_TOKEN' does not exist"
        )
    return discord_bot_token


def get_admin_id() -> int:
    """
    Retrieve the admin bot id from the environment variables.
    :return: ADMIN_DISCORD_ID.
    :rtype: int
    :raises KeyError: If the 'ADMIN_DISCORD_ID' environment variable does not exist.
    """
    discord_admin_id = ADMIN_DISCORD_ID
    if discord_admin_id is None:
        raise KeyError(
            "The requested environment variable 'ADMIN_DISCORD_ID' does not exist"
        )
    return discord_admin_id
