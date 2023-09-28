"""
Discord Bot

This script initializes and runs a Discord bot for various functionalities.

Functions:
- start_bot: Starts the Discord bot.

"""

import discord
from discord.ext import commands

import settings
from services import (
    CoordinatorService,
    LogService,
    MemberService,
    MonthlyReportService,
    ParticipationService,
    ProjectService,
    ReportService,
    TerminationStatementService,
)

from .cogs import (
    AttendanceCog,
    CoordinatorCog,
    Events,
    LogCommand,
    MemberCog,
    MonthlyReportCog,
    ParticipationCog,
    ProjectCog,
    SemesterReportCog,
    TerminationStatementCog,
)

logger = settings.logging.getLogger(__name__)

# pylint: disable=too-many-arguments
def start_bot(
    monthly_report_service: MonthlyReportService,
    member_service: MemberService,
    coordinator_service: CoordinatorService,
    project_service: ProjectService,
    participation_service: ParticipationService,
    report_service: ReportService,
    termination_service: TerminationStatementService,
    log_service: LogService,
):
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
        await bot.add_cog(
            TerminationStatementCog(
                termination_service,
            )
        )
        await bot.add_cog(
            ParticipationCog(
                participation_service, coordinator_service, project_service
            )
        )
        await bot.add_cog(MemberCog(member_service, coordinator_service))
        await bot.add_cog(CoordinatorCog(coordinator_service))
        await bot.add_cog(ProjectCog(project_service))

        await bot.add_cog(
            AttendanceCog(
                bot,
                member_service,
                participation_service,
                project_service,
            )
        )

        # updates the bot's command representation
        await bot.add_cog(Events(log_service))
        await bot.add_cog(LogCommand(log_service, coordinator_service))
        await bot.add_cog(
            SemesterReportCog(
                member_service,
                project_service,
                report_service,
                coordinator_service,
                participation_service,
            )
        )
        await bot.add_cog(
            MonthlyReportCog(
                member_service,
                project_service,
                monthly_report_service,
                coordinator_service,
                participation_service,
            )
        )
        await bot.tree.sync()
        logger.info("Bot %s is ready", bot.user)

    @bot.tree.command(name="ping", description="Verifica se o bot está no ar")
    async def ping(interaction: discord.Interaction):
        """
        Command ping to 'send' a 'pong' response.

        :param interaction: The Discord interaction object.
        :type interaction: discord.Interaction

        """
        await bot.tree.sync(guild=interaction.guild)
        logger.info("Ping command user %s", interaction.user.name)
        await interaction.response.send_message(f":ping_pong: {interaction.user.name}")

    bot.run(settings.get_discord_bot_token())
