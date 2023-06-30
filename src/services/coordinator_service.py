"""
This module provides classes and exceptions for managing coordinators.
"""
import discord

from data import CoordinatorData


def is_coordinator(interaction: discord.Interaction):
    """
    Check if the user is a coordinator.

    This function checks if the user associated with the provided `discord.Interaction`
    is a coordinator by comparing their Discord ID with the coordinators' Discord IDs
    stored in the coordinator data.

    :param interaction: The Discord interaction object.
    :type interaction: discord.Interaction
    :return: True if the user is a coordinator, False otherwise.
    :rtype: bool
    """
    discord_id = interaction.user.id
    coordinators = CoordinatorData.load_coordinators(self=CoordinatorData)

    for coordinator in coordinators:
        if str(coordinator.discord_id) == str(discord_id):
            return True
    return False
