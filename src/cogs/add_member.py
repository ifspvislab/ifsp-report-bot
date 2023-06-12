"""
add_member
============

This module display a modal that support project member data
    
Classes:
    - ModalAddMember: Class which represent the modal that support project member data
    - SendModal: Command to display the AddMemberModal
Function:
    - setup: Add SendModal class to list of cogs to be able to use.

"""

import discord
from discord import app_commands, ui
from discord.ext import commands
from discord.interactions import Interaction

from services import verify_standards

from data import add_member


class ModalAddMember(ui.Modal, title="Adicionar Membro"):
    """
    Class which represent the modal that support project member data and add members

    Methods:
        - on_submit: Listen the modal submit event to add members

    Attributes:
        - prontuario: Represente the field prontuário
        - name: Represente the field name
        - email: Represente the field email
        - discord_id: Represente the field discord id
    """

    prontuario = ui.TextInput(label="prontuario", placeholder="SPXXXXX")
    name = ui.TextInput(label="name", min_length=5, max_length=100)
    email = ui.TextInput(label="email", placeholder="nome@email.com")
    discord_id = ui.TextInput(
        label="discord id",
        placeholder="O id do perfil do discord do membro sendo cadastrado.",
    )

    async def on_submit(self, interaction: Interaction, /):
        """
        Listen the modal submit event

        :param interaction: The Discord interaction object
        """
        standards_stats = verify_standards(
            self.prontuario.value,
            self.email.value,
            self.discord_id.value,
        )

        results = "\n".join(standards_stats)
        if len(standards_stats) == 1:
            add_member(
                self.prontuario.value.upper(),
                self.name.value,
                self.email.value,
                self.discord_id.value,
            )
        await interaction.response.send_message(results)


class SendModal(commands.Cog):
    """
    Command to display the AddMemberModal

    Methods:
        - send_modal: Sends the AddMemberModal as a modal in response to an interaction.
    """

    @app_commands.command(name="send_modal", description="send modal")
    async def send_modal(self, interaction: discord.Interaction):
        """
        Sends the AddMemberModal as a modal in response to an interaction.
        """
        await interaction.response.send_modal(ModalAddMember())


async def setup(bot):
    """
    Add SendModal class to list of cogs to be able to use.
    """
    await bot.add_cog(SendModal(bot))
