""" 
termination_statement
============

Classes:
    - TerminationStatementCog: Cog that manages the interactions 
    related to the termination statement
    - TerminationStatementForm: Form tha allows the user to send
    the needed data to create the semester report.


"""

import locale
from io import BytesIO

import discord
from discord import app_commands, ui
from discord.ext import commands

import settings
from services import (
    CoordinatorNotFound,
    MemberNotFound,
    OutofRangeTerminationDate,
    ParticipationNotFound,
    ParticipationNotFoundInServer,
    ProjectNotFound,
    SlashAbsence,
    TerminationStatementService,
)

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

logger = settings.logging.getLogger(__name__)


class TerminationStatementCog(commands.Cog):
    """
    Command to display the TerminationStatementForm

    """

    def __init__(
        self,
        termination_service: TerminationStatementService,
    ):
        """
        Loads the services needed to create the termination statement form
        """
        super().__init__()
        self.termination_service = termination_service

    @app_commands.command(
        name="termo-encerramento",
        description="gera um termo de encerramento das atividades em um projeto.",
    )
    async def open_termination_statement_form(self, interaction: discord.Interaction):
        """
        Command 'termo-encerramento' to open the termination statement form.

        :param interaction: The Discord interaction object.
        :type interaction: discord.Interaction
        """

        try:

            member = self.termination_service.verify_member(
                "discord_id", interaction.user.id
            )

            project = self.termination_service.verify_project(
                "discord_server_id", interaction.guild_id
            )

            participations = self.termination_service.verify_participation(
                "registration", member.registration
            )

            self.termination_service.verify_if_member_in_participation(
                project.project_id, participations
            )

            coordinator = self.termination_service.verify_coordinator(
                "coord_id", project.coordinator_id
            )
            await interaction.response.send_modal(
                TerminationStatementForm(
                    self.termination_service,
                    member,
                    project,
                    participations,
                    coordinator,
                )
            )

        except MemberNotFound as exception:
            logger.warning(
                "User %s without permission tried to generate termination statement",
                interaction.user.name,
            )
            await interaction.response.send_message(exception)

        except ProjectNotFound as exception:
            logger.error(
                "Project not found while doing termination statement requested by user %s",
                interaction.user.name,
            )
            await interaction.response.send_message(exception)

        except ParticipationNotFound as exception:
            logger.error(
                "Participation not found while doing termination statement requested by user %s",
                interaction.user.name,
            )
            await interaction.response.send_message(exception)

        except CoordinatorNotFound as exception:
            logger.error(
                "Coordinator not found while doing termination statement requested by user %s",
                interaction.user.name,
            )
            await interaction.response.send_message(exception)

        except ParticipationNotFoundInServer as exception:
            logger.warning(
                "User %s does not have a participation on server %s",
                interaction.user.name,
                interaction.guild,
            )
            await interaction.response.send_message(exception)


class TerminationStatementForm(ui.Modal):
    """
    Class that represents a termination statement form,
    defining a modal form.
    """

    termination_date = ui.TextInput(
        label="Data para o encerramento",
        min_length=10,
        max_length=10,
        placeholder="Digite a data de encerramento (dd/mm/aaaa)",
        style=discord.TextStyle.short,
    )
    termination_reason = ui.TextInput(
        label="Motivo do encerramento",
        style=discord.TextStyle.paragraph,
        min_length=60,
        max_length=250,
    )
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        termination_service,
        member,
        project,
        participations,
        coordinator,
    ) -> None:
        """
        Initialize the TerminationStatementForm instance

        :param member_service: Instance of the MemberService class.
        :type member_service: MemberService
        :param project_service: Instance of the ProjectService class.
        :type project_service: ProjectService
        :param participation_service: An instance of the ParticipationService class.
        :type participation_service: ParticipationService
        :param coordinator_service: An instance of the CoordinatorService class.
        :type coordinator_service: CoordinatorService

        """

        super().__init__(title="Termo de Encerramento")
        self.termination_service = termination_service
        self.member = member
        self.project = project
        self.participations = participations
        self.coordinator = coordinator

    async def on_submit(self, interaction: discord.Interaction, /):
        """
        Submits the modal into the form

        :param interaction: Discord interaction object
        :type interaction: discord.Interaction
        """

        try:
            self.termination_service.verify_termination_date_slashes(
                self.termination_date.value
            )

            self.termination_service.verify_termination_date_period(
                self.project.start_date,
                self.project.end_date,
                self.termination_date.value,
            )

            self.termination_service.write_termination_date_in_participations(
                self.participations,
                self.project.project_id,
                self.termination_date.value,
            )

            termination_statement = self.termination_service.generate_document(
                self.member,
                self.project,
                self.coordinator,
                self.termination_date.value,
                self.termination_reason.value,
            )

            document_name = f"""termo-encerramento-{self.member.name}-
                {self.member.registration}-{self.project.project_title}.pdf"""

            logger.info(
                "Termination statement successfully created by user %s",
                interaction.user.name,
            )

            await interaction.response.send_message(
                content="Termo de Encerramento gerado.",
                file=discord.File(
                    BytesIO(termination_statement),
                    filename=document_name,
                    spoiler=False,
                ),
            )

        except SlashAbsence as exception:
            await interaction.response.send_message(exception)

        except ValueError as exception:
            logger.warning(
                " User %s inserted an invalid termination date format",
                interaction.user.name,
            )
            date_format_error = (
                self.termination_service.verify_termination_date_format_error(
                    str(exception)
                )
            )
            if date_format_error is not None:
                await interaction.response.send_message(date_format_error)
            else:
                logger.error(
                    "An unexpected error occurred in termination date input by user %s",
                    interaction.user.name,
                )
            await interaction.response.send_message(date_format_error)

        except OutofRangeTerminationDate as exception:
            await interaction.response.send_message(exception)
