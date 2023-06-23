"""Services for cordinator"""
import discord

from settings import get_coordinator_id

ID_COORDINATOR = get_coordinator_id()


class CoordinatorService:
    def is_coordinator(interaction: discord.Interaction):
        """Check if it's the coordinator doing the command by the discord id user"""
        if interaction.user.id == ID_COORDINATOR:
            return True
        return False
