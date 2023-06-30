"""
add_coordinator_modal.py

Este módulo contém a definição da classe AddCoordinatorModal, 
que é um modal para adicionar um coordenador.

Classes:
    AddCoordinatorModal: Um modal para adicionar um coordenador.
"""

from uuid import uuid4

import discord
from discord import app_commands, ui
from discord.ext import commands

import settings
from data import Coordinator
from services import (
    CoordinatorAlreadyExists,
    CoordinatorService,
    DiscordIdError,
    EmailError,
    RegistrationError,
    is_admin,
)

logger = settings.logging.getLogger(__name__)


class AddCoordinatorModal(ui.Modal):
    """
    Modal for adding a Coordinator.

    Attributes:
        prontuario (ui.TextInput): Input field for the prontuario.
        discord_id (ui.TextInput): Input field for the Discord ID.
        name (ui.TextInput): Input field for the name.
        email (ui.TextInput): Input field for the email.

    Methods:
        __init__(): Initializes the AddCoordinatorModal.
        on_submit(interaction): Handles the submit event when adding a coordinator.

    """

    prontuario = ui.TextInput(
        label="Prontuário:",
        style=discord.TextStyle.short,
        placeholder="Digite o prontuário",
        required=True,
        max_length=9,
    )
    discord_id = ui.TextInput(
        label="Discord id:",
        style=discord.TextStyle.short,
        placeholder="Digite o Discord Id",
        required=True,
        max_length=30,
    )
    name = ui.TextInput(
        label="Nome:",
        style=discord.TextStyle.short,
        placeholder="Digite o nome",
        required=True,
        min_length=5,
        max_length=100,
    )
    email = ui.TextInput(
        label="Email:",
        style=discord.TextStyle.short,
        placeholder="Digite o email",
        required=True,
        min_length=5,
        max_length=50,
    )

    def __init__(self, coordinator_service: CoordinatorService) -> None:
        """
        Initializes the AddCoordinatorModal.
        """
        super().__init__(title="Adicionar coordenador")
        self.coordinator_service = coordinator_service

    async def on_submit(self, interaction: discord.Interaction, /):
        """
        Handles the submit event when adding a coordinator.

        Args:
            interaction (discord.Interaction): The interaction object representing the submit event.

        """

        try:
            self.coordinator_service.create(
                Coordinator(
                    str(uuid4()),
                    self.prontuario.value,
                    self.discord_id.value,
                    self.name.value,
                    self.email.value,
                )
            )

            logger.info(
                "Coordinator '%s' successfully created by '%s'",
                self.name,
                interaction.user.name,
            )

            await interaction.response.send_message(
                "Coordenador cadastrado com sucesso!"
            )
           

        except (
            CoordinatorAlreadyExists,
            DiscordIdError,
            EmailError,
            RegistrationError,
        ) as exception:
            logger.error("An error occurred while creating a new coordinator: %s", str(exception))
            await interaction.response.send_message(str(exception))


class CoordinatorCog(commands.Cog):
    """
    Command to display the AddMemberModal

    Methods:
        - send_modal: Sends the AddMemberModal as a modal in response to an interaction.
    """

    def __init__(self, coordinator_service: CoordinatorService):
        super().__init__()
        self.coordinator_service = coordinator_service

    @app_commands.command(
        name="cadastrar-coordenador", description="registrar coordenador via modal"
    )
    @app_commands.check(is_admin)
    async def add_coordinator(self, interaction: discord.Interaction):
        """Verification and call for pop up the modal"""
        modal = AddCoordinatorModal(self.coordinator_service)
        await interaction.response.send_modal(modal)

        logger.info("cadastrar-coordenador command user %s", interaction.user.name)

    @add_coordinator.error
    async def add_coordinator_error(self, interaction: discord.Interaction, error):
        """Treating error if it's not the admin"""
        await interaction.response.send_message(
            "Peça ao administrador para executar este comando, você não está autorizado!"
        )

        print(error)