"""
add_participation.py

Este módulo contém a definição da classe AddParticipationModal.
que é um que registra a participação na database.

Classes:
AddParticipationModal: Um modal para adicionar participação.
"""
# pylint: disable-next=unused-import
from datetime import date, datetime
from uuid import uuid4

import discord
from discord import app_commands, ui
from discord.ext import commands

import settings
from data import Participation
from services import (
    CoordinatorService,
    DateError,
    MemberError,
    ParticipationAlreadyExists,
    ParticipationService,
    ProjectService,
    RegistrationError,
)

logger = settings.logging.getLogger(__name__)


class AddParticipationModal(ui.Modal):
    """
    Modal for adding a Participation.

    Attributes:
        prontuario (ui.TextInput): Input field for the prontuario.
        project (ui.TextInput): Input field for the project title.
        date (ui.TextInput): Input field for the entering date in the project.

    Methods:
        __init__(): Initializes the AddParticipationModal.
        on_submit(interaction): Handles the submit event when adding a coordinator.
    """

    registration = ui.TextInput(
        label="Prontuário:", placeholder="SPXXXXXXX", min_length=9, max_length=9
    )

    project_title = ui.TextInput(
        label="Título do projeto:",
        placeholder="Ex: IFSP Vislab",
        min_length=5,
        max_length=100,
    )

    today = str(date.today()).split(sep="-")
    date = ui.TextInput(
        label="Data de entrada:",
        placeholder=f"{today[2]}/{today[1]}/{today[0]}",
        min_length=10,
        max_length=10,
    )

    def __init__(
        self,
        participation_service: ParticipationService,
        project_service: ProjectService,
    ) -> None:
        """Initializes the participation and project services."""
        super().__init__(title="Adicionar Participação")
        self.participation_service = participation_service
        self.project_service = project_service

    async def on_submit(self, interaction: discord.Interaction, /):
        """
        Handles the submit event when adding a coordinator.

        Args:
            interaction (discord.Interaction): The interaction object representing the submit event.
        """

        try:
            project = self.project_service.find_project_by_type(
                "project_title", self.project_title.value
            )
            if project is None:
                logger.error("O projeto inserido inexiste nos registros.")
                await interaction.response.send_message(
                    "O projeto inexiste nos registros!"
                )

            else:
                self.participation_service.create(
                    Participation(
                        str(uuid4()),
                        self.registration.value.upper(),
                        project.project_id,
                        datetime.strptime(self.date.value, "%d/%m/%Y").date(),
                        project.end_date,
                    )
                )
                logger.info(
                    "Participation sucesssfully created by %s", interaction.user.name
                )

                await interaction.response.send_message(
                    "Participação criada com sucesso!"
                )
        except (
            ParticipationAlreadyExists,
            DateError,
            RegistrationError,
            MemberError,
        ) as erro:
            logger.error("%s", erro)
            await interaction.response.send_message(f"{erro}")


class ParticipationCog(commands.Cog):
    """
    Command to display the AddParticipationModal.

    Methods:
        - send_modal: Sends the AddParticipationModal as a modal in response to an interaction.
    """

    def __init__(
        self,
        participation_service: ParticipationService,
        coordinator_service: CoordinatorService,
        project_service: ProjectService,
    ) -> None:
        super().__init__()
        self.participation_service = participation_service
        self.coordinator_service = coordinator_service
        self.project_service = project_service

    @app_commands.command(
        name="adicionar-participação",
        description="registra a participação de um aluno em um projeto.",
    )
    async def add_participation_modal(self, interaction: discord.Interaction):
        """
        Verification and call of the add participation modal.
        """
        coordinator = self.coordinator_service.find_coordinator_by_type(
            "discord_id", interaction.user.id
        )
        if coordinator is None:
            logger.warning(
                "Usuário %s sem autorização tentou adicionar participação.",
                interaction.user.name,
            )
            await interaction.response.send_message(
                "Você não está autorizado a utilizar esse comando! Peça a um coordenador."
            )
        else:
            modal = AddParticipationModal(
                self.participation_service, self.project_service
            )
            await interaction.response.send_modal(modal)

        logger.info("adicionar-participação command user %s", interaction.user.name)
