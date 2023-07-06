"""
Classes:
    - SemesterReportCog: The cog that handles all interactions related to the semester report.
    - SemesterReportForm: A form that allows the user to send the needed data to create
    the semester report.
"""


from datetime import datetime
from io import BytesIO

import discord
from discord import app_commands, ui
from discord.ext import commands

import settings
from reports import SemesterReport, SemesterReportData
from services import (
    CoordinatorService,
    MemberService,
    ParticipationService,
    ProjectService,
)
from services.report_service import InvalidRequestPeriod, ReportService

logger = settings.logging.getLogger(__name__)


class WrongServerError(Exception):
    """
    Handles the exception of when the semester report request is made
    in the wrong server.
    """


class SemesterReportCog(commands.Cog):
    """
    Command to display the SemesterReportForm
    Methods:
        - send_modal: Sends the SemesterReportForm as a modal in response to an interaction.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        member_service: MemberService,
        project_service: ProjectService,
        report_service: ReportService,
        coordinator_service: CoordinatorService,
        participation_service: ParticipationService,
    ):
        super().__init__()
        self.member_service = member_service
        self.project_service = project_service
        self.report_service = report_service
        self.coordinator_service = coordinator_service
        self.participation_service = participation_service

    @app_commands.command(
        name="relatorio-semestral",
        description="Abre o formulário para gerar um relatório de ensino semestral",
    )
    async def open_semester_report_form(self, interaction: discord.Interaction):
        """
        Command 'relatorio-semestral' to open the semester report form.

        :param interaction: The Discord interaction object.
        :type interaction: discord.Interaction

        """
        try:
            errors = []

            student = self.member_service.find_member_by_type(
                "discord_id", interaction.user.id
            )

            if student is None:
                errors.append(
                    "Você não tem permissão para gerar relatório semestral,"
                    " pois não está cadastrado em nenhum projeto de ensino!"
                )
                logger.warning(
                    "User %s without permission tried to generate semester report",
                    interaction.user.name,
                )

            project = self.project_service.find_project_by_type(
                "discord_server_id", interaction.channel_id
            )

            if project is None:
                errors.append("Este projeto não está cadastrado no database.")
                logger.warning(
                    "Project not found for server ID %s",
                    interaction.channel_id,
                )

            self.report_service.invalid_request_period()

        except InvalidRequestPeriod as error:
            errors.append(error)
            logger.warning(
                "User %s tried to generate semester report outside of allowed period.",
                interaction.user.name,
            )

        if not errors:
            logger.info("Semester report user %s", interaction.user.name)
            # pylint: disable=too-many-function-args
            await interaction.response.send_modal(
                SemesterReportForm(
                    self.member_service,
                    self.project_service,
                    self.report_service,
                    self.coordinator_service,
                    self.participation_service,
                )
            )
        else:
            embed = discord.Embed(
                title=":sob: Problemas com a sua requisição", color=0xFF0000
            )
            for index, error in enumerate(errors):
                embed.add_field(name=f"Erro {index+1}", value=error, inline=False)

            await interaction.response.send_message(embed=embed)


class SemesterReportForm(ui.Modal):
    """
    Class representing a semester report form.

    This class defines a modal form for generating semester reports.

    """

    placeholder1 = "Aqui, você deve inserir as atividades"
    placeholder1 += " planejadas até o presente momento."

    placeholder2 = "Aqui, você deve inserir quais as atividades"
    placeholder2 += " foram realizadas até o presente momento."

    placeholder3 = "Aqui, você deve discorrer sobre quais foram"
    placeholder3 += " os resultados obtidos das atividades realizadas."

    planned_activities = ui.TextInput(
        label="Atividades planejadas",
        style=discord.TextStyle.paragraph,
        placeholder=placeholder1,
        min_length=300,
        max_length=600,
    )
    performed_activities = ui.TextInput(
        label="Atividades realizadas",
        style=discord.TextStyle.paragraph,
        placeholder=placeholder2,
        min_length=300,
        max_length=600,
    )
    results = ui.TextInput(
        label="Resultados obtidos",
        style=discord.TextStyle.paragraph,
        placeholder=placeholder3,
        min_length=300,
        max_length=600,
    )

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        member_service: MemberService,
        project_service: ProjectService,
        report_service: ReportService,
        coordinator_service: CoordinatorService,
        participation_service: ParticipationService,
    ) -> None:
        """
        Initialize the SemesterReportForm instance.

        :param member_service: An instance of the MemberService class.
        :type member_service: MemberService
        :param project_service: An instance of the ProjectService class.
        :type project_service: ProjectService
        :param coordinator_service: An instance of the CoordinatorService class.
        :type coordinator_service: CoordinatorService
        :param participation_service: An instance of the ParticipationService class.
        :type participation_service: ParticipationService
        :param report_service: An instance of the ReportService class.
        :type report_service: ReportService
        """
        super().__init__(title="Relatório Semestral")
        self.member_service = member_service
        self.project_service = project_service
        self.coordinator_service = coordinator_service
        self.participation_service = participation_service
        self.report_service = report_service

    async def on_submit(self, interaction: discord.Interaction, /):
        """
        Handle the submit event of the form.

        This method is called when the user submits the form.
        It generates the semester report based on the form data and sends it to the user.

        :param interaction: The Discord interaction object.
        :type interaction: discord.Interaction

        """

        project = self.project_service.find_project_by_type(
            "discord_server_id", interaction.channel_id
        )
        student = self.member_service.find_member_by_type(
            "discord_id", interaction.user.id
        )
        coordinator = self.coordinator_service.find_coordinator_by_type(
            "coord_id", project.coordinator_id
        )

        if student:
            total_participations = (
                self.participation_service.find_participations_by_type(
                    "registration", student.registration
                )
            )
        return_values = None

        if total_participations:
            for participation in total_participations:
                if participation.registration == student.registration:
                    if participation.project_id == project.project_id:
                        if project.coordinator_id == coordinator.coord_id:
                            return_values = (
                                project.project_title,
                                coordinator.name,
                                student.name,
                            )
                            break

        if return_values is None:
            logger.warning(
                "User %s tried to generate semester report in incorrect server",
                interaction.user.name,
            )
            raise WrongServerError(
                await interaction.response.send_message(
                    "Verifique se você está no servidor correspondente ao seu projeto!"
                )
            )

        if return_values is not None:
            data = SemesterReportData(
                project_title=return_values[0],
                project_manager=return_values[1],
                student_name=return_values[2],
                planned_activities=self.planned_activities.value.strip(),
                performed_activities=self.performed_activities.value.strip(),
                results=self.results.value.strip(),
            )

            report = SemesterReport(data)
            month = datetime.now().strftime("%B")

            name_of_report = (f"RelatorioSemestral_Ensino_{month}").upper()
            name_of_report += (f"_{student.name}").upper() + ".pdf"

            student_first_name = student.name.split()[0]
            content = f"Sucesso, {student_first_name}! Aqui está"
            content += " o relatório semestral em formato PDF:"
            await interaction.response.send_message(
                content=content,
                file=discord.File(
                    BytesIO(report.generate()),
                    filename=name_of_report,
                    spoiler=False,
                ),
            )
