"""
admin_service
=======================

This module provides the function for managing the admin verification.

"""
import discord

from settings import get_admin_id

ID_ADMIN = get_admin_id()


def is_admin(interaction: discord.Interaction):
    if interaction.user.id == int(ID_ADMIN):
        return True
    return False
