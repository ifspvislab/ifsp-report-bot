"""
monthly_report_cog.py

This module defines classes for modal forms used in Discord bot interactions.

Classes:
- MonthyReportForm: Represents a monthly report form for generating monthly reports.

"""
from io import BytesIO

import discord
from discord import app_commands, ui
from discord.ext import commands

import settings
from data import Member, Project
from services import (CoordinatorService, MemberService, MonthlyReportService,
                      ParticipationService, ProjectService)
from services.monthly_report_service import (CoordinatorDoesNotExist,
                                             InvalidMember,
                                             InvalidRequestPeriod,
                                             ParticipationDoesNotExisInServer,
                                             ParticipationDoesNotExist,
                                             ProjectDoesNotExist)

logger = settings.logging.getLogger(__name__)


class MonthlyReportCog(commands.Cog):
    """
    Command to display the MonthlyReportForm
    Methods:
        - send_modal: Sends the MonthlyReportForm as a modal in response to an interaction.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        member_service: MemberService,
        project_service: ProjectService,
        monthly_report_service: MonthlyReportService,
        coordinator_service: CoordinatorService,
        participation_service: ParticipationService,
    ):
        super().__init__()
        self.member_service = member_service
        self.project_service = project_service
        self.monthly_report_service = monthly_report_service
        self.coordinator_service = coordinator_service
        self.participation_service = participation_service

    @app_commands.command(
        name="relatorio-mensal",
        description="comando para abrir o formulário para gerar um relatório de ensino mensal",
    )
    async def open_monthly_report_form(self, interaction: discord.Interaction):
        """
        Command 'relatorio-mensal' to open the monthly report form.

        :param interaction: The Discord interaction object.
        :type interaction: discord.Interaction

        """
        try:

            student = self.member_service.find_member_by_type(
                "discord_id", interaction.user.id
            )

            if student is None:
                raise InvalidMember("Você não está cadastrado como membro!")

            project = self.project_service.find_project_by_type(
                "discord_server_id", interaction.guild_id
            )

            if project is None:
                raise ProjectDoesNotExist(
                    "Este servidor não está cadastrado como projeto."
                )

            invalid_request_period = (
                self.monthly_report_service.invalid_request_period()
            )

            valid_member_for_request = (
                self.monthly_report_service.verifiy_member_validity(
                    student,
                    project,
                )
            )

            if valid_member_for_request and not invalid_request_period:
                logger.info("Monthly report user %s", interaction.user.name)
                # pylint: disable=too-many-function-args
                await interaction.response.send_modal(
                    MonthlyReportForm(
                        student,
                        project,
                        self.monthly_report_service,
                        self.coordinator_service,
                        self.participation_service,
                    )
                )

        except ParticipationDoesNotExist as exception:
            logger.error(
                "User %s does not participate of any project", interaction.user.name
            )
            await interaction.response.send_message(exception)

        except ParticipationDoesNotExisInServer as exception:
            logger.error(
                "User %s tried to generate the monthly report in the wrong project server",
                interaction.user.name,
            )
            await interaction.response.send_message(exception)

        except InvalidMember as exception:
            logger.error(
                "User %s without permission tried to generate the monthly report",
                interaction.user.name,
            )
            await interaction.response.send_message(exception)

        except InvalidRequestPeriod as exception:
            logger.error(
                "User %s tried to generate monthly report outside of the allowed period",
                interaction.user.name,
            )
            await interaction.response.send_message(exception)

        except ProjectDoesNotExist as exception:
            logger.error("No project found for server %s", interaction.guild_id)
            await interaction.response.send_message(str(exception))

        except CoordinatorDoesNotExist as exception:
            logger.error(
                "No coordinator for this project was found in the coordinators database."
            )
            await interaction.response.send_message(exception)


class MonthlyReportForm(ui.Modal):
    """
    Class representing a monthly report form.

    This class defines a modal form for generating monthly reports.

    """

    placeholder1 = "Digite as atividades planejadas até o presente momento."

    placeholder2 = "Digite quais as atividades foram realizadas até o presente momento."

    placeholder3 = "Digite quais foram os resultados obtidos das atividades realizadas."

    planned_activities = ui.TextInput(
        label="Atividades planejadas",
        style=discord.TextStyle.paragraph,
        placeholder=placeholder1,
        min_length=200,
        max_length=500,
    )
    performed_activities = ui.TextInput(
        label="Atividades realizadas",
        style=discord.TextStyle.paragraph,
        placeholder=placeholder2,
        min_length=200,
        max_length=500,
    )
    results = ui.TextInput(
        label="Resultados obtidos",
        style=discord.TextStyle.paragraph,
        placeholder=placeholder3,
        min_length=200,
        max_length=500,
    )

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        member: Member,
        project: Project,
        monthly_report_service: MonthlyReportService,
        coordinator_service: CoordinatorService,
        participation_service: ParticipationService,
    ) -> None:
        """
        Initialize the MonthlyReportForm instance.

        :param member_service: An instance of the MemberService class.
        :type member_service: MemberService
        :param project_service: An instance of the ProjectService class.
        :type project_service: ProjectService
        :param coordinator_service: An instance of the CoordinatorService class.
        :type coordinator_service: CoordinatorService
        :param participation_service: An instance of the ParticipationService class.
        :type participation_service: ParticipationService
        :param monthlyreport_service: An instance of the MonthlyReportService class.
        :type monthly_report_service: MonthlyReportService
        """
        super().__init__(title="Relatório Mensal")
        self.member = member
        self.project = project
        self.coordinator_service = coordinator_service
        self.participation_service = participation_service
        self.monthly_report_service = monthly_report_service

    async def on_submit(self, interaction: discord.Interaction, /):
        """
        Handle the submit event of the form.

        This method is called when the user submits the form.
        It generates the monthly report based on the form data and sends it to the user.

        :param interaction: The Discord interaction object.
        :type interaction: discord.Interaction

        """

        valid_data_for_report = self.monthly_report_service.verifiy_member_validity(
            self.member,
            self.project,
        )

        if valid_data_for_report:

            project_title, coordinator_name, student_name = valid_data_for_report

            generated_report = self.monthly_report_service.generate_monthly_report(
                project_title=project_title,
                project_manager=coordinator_name,
                student_name=student_name,
                planned_activities=self.planned_activities.value.strip(),
                performed_activities=self.performed_activities.value.strip(),
                results=self.results.value.strip(),
            )

            report = generated_report

            name_of_report, content = self.monthly_report_service.generate_report_info(
                student_name
            )

            await interaction.response.send_message(
                content=content,
                file=discord.File(
                    BytesIO(report),
                    filename=name_of_report,
                    spoiler=False,
                ),
            )
