"""
Discord Bot

This script initializes and runs a Discord bot for various functionalities.

Functions:
- start_bot: Starts the Discord bot.

"""

import os
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

import settings
from bot.modals import AddCoordinatorModal, MonthyReportForm
from services import AdminService, CoordinatorService, StudentService

logger = settings.logging.getLogger(__name__)


def teste(interaction: discord.Interaction):
    return False


def start_bot(student_service: StudentService):
    """
    Start bot.

    This function initializes and starts the Discord bot with the provided StudentService.

    :param student_service: An instance of the StudentService class.
    :type student_service: StudentService

    """
    intents = discord.Intents.all()
    intents.message_content = True
    bot = commands.Bot(intents=intents, command_prefix="!")

    @bot.event
    async def on_ready():
        """
        Event handler for when the bot is ready.

         This function is called when the bot has successfully connected to Discord
         and is ready to start processing events.
         It performs the synchronization of the command tree, ensuring that the bot has
         the latest information about all available commands and their respective settings.

        """

        # await bot.load_extension("cogs.add_coordinator")

        # updates the bot's command representation
        await bot.tree.sync()
        logger.info("Bot %s is ready", bot.user)

    @bot.tree.command(
        name="cadastrar-coordenador", description="registrar coordenador via modal"
    )
    @app_commands.check(AdminService.is_admin)
    async def add_coordinator(interaction: discord.Interaction):
        """Verification and call for pop up the modal"""
        await interaction.response.send_modal(AddCoordinatorModal())

        logger.info("cadastrar-coordenador command user %s", interaction.user.name)

    @add_coordinator.error
    async def add_coordinator_error(interaction: discord.Interaction, error):
        """Treating error if it's not the admin"""
        await interaction.response.send_message(
            "Peça ao administrador para executar este comando, você não está autorizado!"
        )

    @bot.tree.command(name="ping", description="Verifica se o bot está no ar")
    async def ping(interaction: discord.Interaction):
        await bot.tree.sync(guild=interaction.guild)
        """
        Command ping to 'send' a 'pong' response.

        :param interaction: The Discord interaction object.
        :type interaction: discord.Interaction

        """
        logger.info("Ping command user %s", interaction.user.name)
        await interaction.response.send_message(f":ping_pong: {interaction.user.name}")

    @bot.tree.command(
        name="relatorio-mensal",
        description="Abre o formulário para gerar relatório mensal de ensino.",
    )
    async def open_monthy_report_form(interaction: discord.Interaction):
        """
        Command 'relatorio-mensal' to open the monthly report form.

        :param interaction: The Discord interaction object.
        :type interaction: discord.Interaction

        """

        def invalid_request_period():
            """
            Check if the request for generating the monthly report is within the allowed period.

            :return: True if the request is outside the allowed period, False otherwise.
            :rtype: bool
            """
            current_day = datetime.now().day
            start_day = 23

            if current_day < start_day:
                return True

            return False

        errors = []
        student = student_service.find_student_by_discord_id(interaction.user.id)

        if student is None:
            errors.append("Você não tem permissão para gerar relatório mensal")
            logger.warning(
                "User %s without permission tried to generate monthy report",
                interaction.user.name,
            )

        if invalid_request_period():
            errors.append("O período para gerar o relatório mensal inicia no dia 23")
            logger.warning(
                "User %s attempted to generate the monthly report outside the allowed period.",
                interaction.user.name,
            )

        if not errors:
            logger.info("Monthy report user %s", interaction.user.name)
            await interaction.response.send_modal(MonthyReportForm(student_service))
        else:
            embed = discord.Embed(title=":cry: Problemas com a sua requisição")
            for index, error in enumerate(errors):
                embed.add_field(name=f"Erro {index+1}", value=error, inline=False)

            await interaction.response.send_message(embed=embed)

    bot.run(settings.get_discord_bot_token())
