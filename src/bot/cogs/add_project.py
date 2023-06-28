"""
add_project
===============

This module displays the definition of AddProjectModal class, 
that is a modal to add a project. 

Classes:
    - AddProjectModal: a modal that add a project.
"""

import discord
from discord import app_commands, ui
from discord.ext import commands

import settings
from data import Project, ProjectData
from services import DiscordServerIdError, ProjectAlreadyExists

logger = settings.logging.getLogger(__name__)


class AddProjectModal(ui.Modal):
    """
    This modal adds a project.

    Attributes:
        coordenador (ui.TextInput): Input field for the coordenador.
        discord_server_id (ui.TextInput): Input a field for the discord_server_id
        titulo (ui.TextInput): Input field for the titulo.
        data_inicio (ui.TextInput): Input field for the data_inicio.
        data_fim (ui.TextImput): Input field for the data_fim.

    Methods:
        __init__(): Initializes the AddProjectModal.add_item
        on_submit(interaction): Manipulate theb submit event when adding a project.
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
        placeholder="Insira o titulo do projeto",
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

    def __init__(self) -> None:
        super().__init__(title="Adicionar Projeto")

    async def on_submit(self, interaction: discord.Interaction):
        project_data = ProjectData()
        project_service = ProjectService(project_data)
        project = Project(
            self.coordenador.value,
            self.discord_server_id.value,
            self.titulo.value,
            self.data_inicio.value,
            self.data_fim.value,
        )

        try:
            self.project_service.create(project)

            await interaction.response.send_message(
                f"O projeto {self.titulo.value} foi adicionado!"
            )

        except (
            ProjectAlreadyExists,
            DiscordServerIdError,
        ) as e:
            await interaction.response.send_message(str(e))


class ProjectCog(commands.Cog):
    """
    This command displays the AddProjectModal

    Methods:
        - send_modal: sends the AddProjectModal as a modal in response to an interaction.
    """

    @app_commands.command(
        name="adicionar-projeto", description="adicionar projeto via modal"
    )
    @app_commands.check(is_admin)
    async def add_project(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AddProjectModal())

        logger.info("adicionar projeto command user %s", interaction.user.name)

    @add_project.error
    async def add_project_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(
            "Apenas o admin pode executar esse comando!"
        )

        print(error)


async def setup(bot):
    await bot.add_cog(ProjectCog(bot))
