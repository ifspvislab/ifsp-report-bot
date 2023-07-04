"""Services for administrator"""
import discord

from settings import get_admin_id

ID_ADMIN = int(get_admin_id())


def is_admin(interaction: discord.Interaction):
    """Check if it's the administrator doing the command by the discord id user"""
    if interaction.user.id == ID_ADMIN:
        return True
    return False
