"""

add_project

===============


This module displays the definition of AddProjectModal class, 
that is a modal to add a project. 

Classes:
    - AddProjectModal: a modal that add a project.

"""

from uuid import uuid4

import discord
from discord import app_commands, ui
from discord.ext import commands

import settings
from data import Project
from services import (
    DiscordServerIdError,
    EqualOrSmallerDateError,
    InvalidCoordinator,
    InvalidEndDate,
    InvalidTimeInterval,
    ProjectAlreadyExists,
    ProjectService,
    is_admin,
)
from services.validation import RegistrationError, verify_registration_format

logger = settings.logging.getLogger(__name__)


class AddProjectModal(ui.Modal, title="Adicionar Projeto"):
    """
    This modal adds a project.

    Attributes:
        coordinator_id (ui.TextInput): Input field for the coordinator registration.
        discord_server_id (ui.TextInput): Input field for the discord_server_id.
        title (ui.TextInput): Input field for the title.
        start_date (ui.TextInput): Input field for the start_date.
        end_date (ui.TextInput): Input field for the end_date.

    Methods:
        __init__(): Initializes the AddProjectModal.add_item.
        on_submit(interaction): Manipulate the submit event when adding a project.
    """

    registration_coordinator_id = ui.TextInput(
        label="Prontuário do Coordenador",
        style=discord.TextStyle.short,
        placeholder="Digite o Prontuário (SPXXXXX) do Coordenador",
        required=True,
        max_length=9,
    )
    discord_server_id = ui.TextInput(
        label="Discord Server ID",
        style=discord.TextStyle.short,
        placeholder="Digite o Discord Server ID",
        required=True,
        max_length=30,
    )
    project_title = ui.TextInput(
        label="Título",
        style=discord.TextStyle.short,
        placeholder="Digite o título do projeto",
        required=True,
        min_length=5,
        max_length=150,
    )
    start_date = ui.TextInput(
        label="Data do Início",
        style=discord.TextStyle.short,
        placeholder="Digite a data de início (dd/mm/aaaa)",
        required=True,
        max_length=10,
    )
    end_date = ui.TextInput(
        label="Data do Fim",
        style=discord.TextStyle.short,
        placeholder="Digite a data do fim (dd/mm/aaaa)",
        required=True,
        max_length=10,
    )

    def __init__(self, project_service: ProjectService) -> None:
        super().__init__(title="Adicionar Projeto")
        self.project_service = project_service

    async def on_submit(self, interaction: discord.Interaction, /):
        """
        Manipulate the submit event when adding a project.

        Args:
            interaction (discord.Interaction): The interaction object.

        Raises:
            EqualOrSmallerDateError: If the end date is equal to or earlier than the start date.
            InvalidCoordinator: If the coordinator does not manage any projects.
            InvalidTimeInterval: If the time interval
            between the start and end dates is less than 1 month.
            InvalidEndDate: If the end date is earlier than the current date.
            DiscordServerIdError: If the Discord Server ID is invalid.
            ProjectAlreadyExists: If a project with the same title and dates already exists.
        """

        try:
            verify_registration_format(self.registration_coordinator_id.value)
            coordinator_id = self.project_service.verify_coordinator(
                self.registration_coordinator_id.value
            )

            self.project_service.create(
                Project(
                    str(uuid4()),
                    coordinator_id,
                    self.discord_server_id.value,
                    self.project_title.value.upper(),
                    self.start_date.value,
                    self.end_date.value,
                )
            )

            await interaction.response.send_message("Projeto cadastrado com sucesso!")

        except (
            EqualOrSmallerDateError,
            InvalidCoordinator,
            InvalidTimeInterval,
            InvalidEndDate,
            DiscordServerIdError,
            ProjectAlreadyExists,
            RegistrationError,
        ) as exception:
            logger.error(
                "An error occurred while creating a new project: %s", str(exception)
            )
            await interaction.response.send_message(str(exception))
        except ValueError as error:
            logger.error("%s", error)
            await interaction.response.send_message(
                "Formato de data inválido. Siga o formato DD/MM/YYYY."
            )


class ProjectCog(commands.Cog):
    """
    This command displays the AddProjectModal.

    Methods:
        - send_modal: sends the AddProjectModal as a modal in response to an interaction.
    """

    def __init__(self, project_service: ProjectService):
        super().__init__()
        self.project_service = project_service

    @app_commands.command(
        name="adicionar-projeto", description="comando para registrar projeto via modal"
    )
    async def add_project(self, interaction: discord.Interaction):
        """
        Command to add a project via modal.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        if is_admin(interaction.user.id):
            modal = AddProjectModal(self.project_service)
            await interaction.response.send_modal(modal)

            logger.info("adicionar-projeto command user %s", interaction.user.name)
            return

        await interaction.response.send_message(
            "Você não tem permissão para adicionar projeto."
        )
        logger.error(
            "User (discord_id: %s)"
            + "tried to add a project, but does not have permission.",
            interaction.user.id,
        )
