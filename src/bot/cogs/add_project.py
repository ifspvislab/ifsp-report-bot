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

logger = settings.logging.getLogger(__name__)


class AddProjectModal(ui.Modal):
    """
    This modal adds a project.

    Attributes:
        coordenador (ui.TextInput): Input field for the coordenador.
        discord_server_id (ui.TextInput): Input field for the discord_server_id.
        titulo (ui.TextInput): Input field for the titulo.
        data_inicio (ui.TextInput): Input field for the data_inicio.
        data_fim (ui.TextInput): Input field for the data_fim.

    Methods:
        __init__(): Initializes the AddProjectModal.add_item.
        on_submit(interaction): Manipulate the submit event when adding a project.
    """

    coordenador = ui.TextInput(
        label="Coordenador",
        style=discord.TextStyle.short,
        placeholder="Insira o nome do Coordenador",
        required=True,
        min_length=3,
        max_length=100,
    )
    discord_server_id = ui.TextInput(
        label="Discord Server ID",
        style=discord.TextStyle.short,
        placeholder="Insira o Discord Server ID",
        required=True,
    )
    titulo = ui.TextInput(
        label="Título",
        style=discord.TextStyle.short,
        placeholder="Insira o título do projeto",
        required=True,
        min_length=5,
        max_length=150,
    )
    data_inicio = ui.TextInput(
        label="Data do Início",
        style=discord.TextStyle.short,
        placeholder="Insira a data de início (dia/mês/ano)",
        required=True,
        max_length=10,
    )
    data_fim = ui.TextInput(
        label="Data do Fim",
        style=discord.TextStyle.short,
        placeholder="Insira a data do fim (dia/mês/ano)",
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
            InvalidTimeInterval: If the time interval
            between the start and end dates is less than 1 month.
            InvalidEndDate: If the end date is earlier than the current date.
            DiscordServerIdError: If the Discord Server ID is invalid.
            ProjectAlreadyExists: If a project with the same title and dates already exists.
        """
        try:
            self.project_service.create(
                Project(
                    str(uuid4()),
                    self.coordenador.value,
                    self.discord_server_id.value,
                    self.titulo.value,
                    self.data_inicio.value,
                    self.data_fim.value,
                )
            )

            await interaction.response.send_message(
                f"O projeto {self.titulo.value} foi adicionado!"
            )

        except (
            EqualOrSmallerDateError,
            InvalidCoordinator,
            InvalidTimeInterval,
            InvalidEndDate,
            DiscordServerIdError,
            ProjectAlreadyExists,
        ) as exception:
            await interaction.response.send_message(str(exception))


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
        name="adicionar-projeto", description="Adicionar projeto via modal"
    )
    @app_commands.check(is_admin)
    async def add_project(self, interaction: discord.Interaction):
        """
        Command to add a project via modal.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        await interaction.response.send_modal(AddProjectModal(self.project_service))

        logger.info("Adicionar projeto command user %s", interaction.user.name)

    @add_project.error
    async def add_project_error(self, interaction: discord.Interaction, error):
        """
        Error handler for the add_project command.

        Args:
            interaction (discord.Interaction): The interaction object.
            error: The error that occurred.

        Returns:
             None
        """
        await interaction.response.send_message(
            "Apenas o admin pode executar esse comando!"
        )

        print(error)
