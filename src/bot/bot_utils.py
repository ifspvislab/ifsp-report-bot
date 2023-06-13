"""
bot.utils
=====

Utility functions for the bot.

This module provides utility functions for working with the bot in general.

Functions:
    - show_errors(errors: list[str]) -> Embed: returns a embed with the errors passed as argument

"""


from discord import Embed


def show_errors(errors: list[str]) -> Embed:
    """
    Returns a embed with the errors passed as argument

    :param errors: The errors the program got to that point
    :type errors: list[str]
    :return: Embed
    """
    embed = Embed(title=":cry: Problemas com a sua requisição")
    for index, error in enumerate(errors):
        embed.add_field(name=f"Erro {index+1}", value=error, inline=False)
    return embed
