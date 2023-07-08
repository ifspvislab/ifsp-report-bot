"""
is_coordinator
"""

import discord

from data import CoordinatorData

from .coordinator_service import CoordinatorService


def is_coordinator(interaction: discord.Interaction) -> bool:
    """
    Check if the user is a coordinator.

    This function checks if the user associated with the provided `discord.Interaction`
    stored in the coordinator data.
    """
    if (
        CoordinatorService(CoordinatorData()).find_coordinator_by_type(
            "discord_id", interaction.user.id
        )
        is not None
    ):
        return True
    return False
