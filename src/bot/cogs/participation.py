"""
Receives the inputs of the participation, verify and validates, and then create the participation
in a doc.
"""

from datetime import datetime

import discord
from discord import app_commands, ui
from discord.ext import commands

import settings
from data import ParticipationData, StudentData
from services import (
    CoordinatorService,
    DateError,
    InputAlreadyExists,
    ParticipationService,
    ProjectError,
    StudentError,
)

logger = settings.logging.getLogger(__name__)


class ParticipationModal(discord.ui.Modal):
    """
    Modal for adding a participation.

    Attributes:
        prontuario(ui.TextInput): Input field for the prontuario.
        project(ui.TextInput): Input field for the project.
        day(ui.TextInput): Input field for the day.
        month(ui.TextInput): Input field for the month.
        year(ui.TextInput): Input field for the year.

    Methods:
        __init__(): Initializes the AddParticipationModal.
        on_submit(interaction): Handles the submit event when adding a participation.

    """

    prontuario = ui.TextInput(
        label="Prontuário do aluno:",
        style=discord.TextStyle.short,
        min_length=9,
        max_length=9,
        placeholder="SPXXXXXXX",
        row=1,
    )  # Receives the student registration.

    project = ui.TextInput(
        label="Projeto:",
        style=discord.TextStyle.short,
        min_length=5,
        max_length=150,
        row=2,
    )  # Receives the project name.

    day = ui.TextInput(
        label="Dia:",
        style=discord.TextStyle.short,
        min_length=2,
        max_length=2,
        placeholder="DD",
        row=3,
    )  # Receives the day of the participation.
    month = ui.TextInput(
        label="Mês:",
        style=discord.TextStyle.short,
        min_length=2,
        max_length=2,
        placeholder="MM",
        row=3,
    )  # receives the month of the participation.
    year = ui.TextInput(
        label="Ano:",
        style=discord.TextStyle.short,
        placeholder="YYYY",
        min_length=4,
        max_length=4,
        row=3,
    )  # receives the year of the participation.

    def __init__(self) -> None:

        super().__init__(title="Participação")
        self.participation_service = ParticipationService

        # pylint: disable=unused-variable
        async def on_submit(self, interaction=discord.Interaction, /):
            """
            Handles the submit event when creating a participation.

            Args:
            interaction(discord.Interaction): The interaction object that handles the submit event.

            """
            participation_data = ParticipationData()
            participation_service = ParticipationService(participation_data)

            try:
                participation_service.create(
                    participation=(
                        None,
                        self.prontuario.value,
                        self.project.value,
                        datetime.date(self.year, self.month, self.day),
                        None,
                    )
                )

                name = StudentData.student_registration_to_name(
                    self, registration=self.prontuario
                )
                title = self.project

                await interaction.response.send_message(
                    content=f"A participação do aluno/a {name} no projeto {title} foi registrada."
                )
                logger.warning("A participação de %s foi registrada com sucesso.", name)

            except (InputAlreadyExists, DateError, ProjectError, StudentError) as erro:
                await interaction.response.send_message(content=f"{erro}")
                logger.warning("Participação não registrada. Erro: %s", erro)


class ParticipationCommand(commands.Cog):
    """
    Class containing the command that sends the 'create participation' modal.
    """

    def __init__(
        self,
        participation_service=ParticipationService,
        coordinator_service=CoordinatorService,
    ):
        super().__init__()
        self.participation_service = participation_service
        self.coordinator_service = coordinator_service

    @app_commands.command(
        name="adicionar-participacao",
        description="Registra a participação de um aluno em um projeto.",
    )
    async def call_participation_modal(self, interaction: discord.Interaction):
        """
        Verifies if the command was used by authorized personnel
        And calls for the pop up of the modal.
        """

        if (
            self.coordinator_service.find_coordinator_by_type(
                self, "discord_id", interaction.user.id
            )
            is None
        ):
            logger.warning(
                "User %s without permission tried to register a participation",
                interaction.user.name,
            )
            await interaction.response.send_message(
                "Você não tem permissão para registrar uma participação."
            )
        else:
            modal = ParticipationModal
            await interaction.response.send_modal(modal)

            logger.info(
                "adicionar-participação command user: %s", interaction.user.name
            )


async def setup(bot):
    """Adds ParticpationCommand to the list of cogs to be able to use."""
    await bot.add_cog(ParticipationCommand(bot))
