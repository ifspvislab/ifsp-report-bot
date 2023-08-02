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

from uuid import uuid4

import discord
from discord import Member, app_commands, ui
from discord.ext import commands
from discord.interactions import Interaction

import data
import settings
from services import CoordinatorService, MemberService

logger = settings.logging.getLogger(__name__)


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

    def __init__(
        self, member_service: MemberService, coordinator_service: CoordinatorService
    ):
        super().__init__()
        self.member_service = member_service
        self.coordinator_service = coordinator_service

    registration = ui.TextInput(label="prontuario", placeholder="SPXXXXX", max_length=9)
    name = ui.TextInput(label="name", placeholder="nome", min_length=5, max_length=100)
    email = ui.TextInput(label="email", placeholder="nome@email.com")
    discord_id = ui.TextInput(label="discord id", placeholder="discord id")

    async def on_submit(self, interaction: Interaction, /):
        """
        Listen the modal submit event

        :param interaction: The Discord interaction object
        """

        member = data.Member(
            str(uuid4()),
            self.registration.value.upper(),
            self.discord_id.value,
            self.name.value,
            self.email.value,
        )
        self.member_service.add_member(member)
        await interaction.response.send_message("Membro cadastrado com sucesso.")
        logger.info(
            "Membro %s adicionado por %s",
            member.registration,
            self.coordinator_service.find_coordinator_by_type(
                "discord_id", interaction.user.id
            ).registration,
        )

    async def on_error(self, interaction: Interaction, error: Exception, /):
        logger.error(
            "Erro: %s na tentativa do usuário %s de adicionar membro",
            error,
            self.coordinator_service.find_coordinator_by_type(
                "discord_id", interaction.user.id
            ).registration,
        )
        await interaction.response.send_message(error)


class MemberCog(commands.Cog):
    """
    Command to display the AddMemberModal

    Methods:
        - send_modal: Sends the AddMemberModal as a modal in response to an interaction.
    """

    def __init__(
        self, member_service: MemberService, coordinator_service: CoordinatorService
    ):
        super().__init__()
        self.member_service = member_service
        self.coordinator_service = coordinator_service

    @app_commands.command(
        name="adicionar_membro",
        description="manda um modal para adicionar o membro",
    )
    @app_commands.describe(
        member="Usuário do servidor que deseja adicionar como membro"
    )
    async def send_modal(self, interaction: discord.Interaction, member: Member = None):
        """
        Sends the AddMemberModal as a modal in response to an interaction.
        """

        if self.coordinator_service.find_coordinator_by_type(
            "discord_id", interaction.user.id
        ):
            modal = ModalAddMember(self.member_service, self.coordinator_service)
            if member is not None:
                modal.discord_id.default = str(member.id)
            await interaction.response.send_modal(modal)
            return

        await interaction.response.send_message(
            "Você não tem permissão para adicionar membro."
        )
        logger.error(
            "Usuário (discord_id: %s)"
            + "tentou adicionar membro, porém não possui permissão.",
            interaction.user.id,
        )
