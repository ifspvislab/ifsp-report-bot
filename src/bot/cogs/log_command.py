"""
Cog for handling log commands.
"""
from io import BytesIO

import discord
from discord import app_commands
from discord.ext import commands

import settings
from services import LogService, is_coordinator

logger = settings.logging.getLogger(__name__)


class LogCommand(commands.Cog):
    """
    Cog that handles log commands.
    """

    def __init__(self, log_service: LogService):
        self.log_service = log_service

    @app_commands.command(name="log", description="Create the log file")
    @app_commands.describe(
        start_date="Data inicial para a procura de registros. Ex:01/09/2023",
        end_date="Data final para a procura de registros. Ex:01/09/2023",
        discord_id="Registros apenas com o ID inserido",
    )
    @app_commands.check(is_coordinator)
    # pylint: disable=too-many-branches
    async def log_file(
        self,
        interaction: discord.Interaction,
        start_date: str = None,
        end_date: str = None,
        discord_id: str = None,
    ):
        """
        Command for creating a log file.

        Parameters:
            - interaction: The interaction object.
            - start_date: Optional start date for log filtering.
            - end_date: Optional end date for log filtering.
            - member_id: Optional member ID for log filtering.

        Returns:
            None
        """
        log_report = self.log_service.generate_log_report(
            interaction.guild.id, discord_id, start_date, end_date
        )
        await interaction.response.send_message(
            file=discord.File(BytesIO(log_report.generate()), filename="log.pdf"),
            ephemeral=True,
        )
        logger.info(
            "Log File successfully created by '%s'",
            interaction.user.name,
        )

    @log_file.error
    async def log_file_error(self, interaction: discord.Interaction, error):
        """
        Logs and handles errors related to file operations during an interaction.

        Args:
            interaction (discord.Interaction): The Discord interaction where the error occurred.
            error (Exception): The error object representing the encountered exception.

        Returns:
            None
        """
        if str(error) == "The check functions for command 'log' failed.":
            await interaction.response.send_message(
                "Apenas o coordenador tem acesso ao comando!", ephemeral=True
            )
        else:
            error_message = str(error).rsplit(":", maxsplit=1)[-1]
            await interaction.response.send_message(error_message, ephemeral=True)
            logger.error(
                "An error occurred while creating a log file: %s", error_message
            )
