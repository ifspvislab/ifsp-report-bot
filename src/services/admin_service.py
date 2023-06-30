"""
admin_service
=======================

This module provides the function for managing the admin verification.

"""
import discord

from settings import get_admin_id

ID_ADMIN = int(get_admin_id())


def is_admin(interaction: discord.Interaction):
    """
    Check if the interaction user is an admin.

    :param interaction: The Discord interaction.
    :type interaction: discord.Interaction
    :return: True if the user is an admin, False otherwise.
    :rtype: bool
    """
    if interaction.user.id == int(get_admin_id()):
        return True
    return False
