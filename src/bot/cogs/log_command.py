"""
Cog for handling log commands.
"""
from io import BytesIO

import discord
from discord import Member, app_commands
from discord.ext import commands

import settings
from services import (CoordinatorService, IdDoesNotExist, IncorrectDateFilter,
                      InvalidReportSize, LogService, NoStartDate)
from services.validation import DiscordIdError

logger = settings.logging.getLogger(__name__)


class LogCommand(commands.Cog):
    """
    Cog that handles log commands.
    """

    def __init__(
        self, log_service: LogService, coordinator_service: CoordinatorService
    ):
        super().__init__()
        self.log_service = log_service
        self.coordinator_service = coordinator_service

    @app_commands.command(name="log", description="Cria o arquivo log")
    @app_commands.describe(
        start_date="Data inicial para a procura de registros. Ex:01/09/2023",
        end_date="Data final para a procura de registros. Ex:01/09/2023",
        member="Apenas registros do membro inserido",
    )
    async def log_file(
        self,
        interaction: discord.Interaction,
        start_date: str = None,
        end_date: str = None,
        member: Member = None,
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
        if self.coordinator_service.find_coordinator_by_type(
            "discord_id", interaction.user.id
        ):
            try:
                if member is not None:
                    log_report = self.log_service.generate_log_report(
                        interaction.guild.id, member.id, start_date, end_date
                    )
                else:
                    log_report = self.log_service.generate_log_report(
                        interaction.guild.id, member, start_date, end_date
                    )
                await interaction.response.send_message(
                    file=discord.File(
                        BytesIO(log_report.generate()), filename="log.pdf"
                    ),
                    ephemeral=True,
                )
                logger.info(
                    "Log File successfully created by '%s'",
                    interaction.user.name,
                )
            except (
                IdDoesNotExist,
                NoStartDate,
                InvalidReportSize,
                IncorrectDateFilter,
                DiscordIdError,
            ) as exception:
                await interaction.response.send_message(exception)

        else:
            await interaction.response.send_message(
                "Você não tem permissão para executar esse comando."
            )
