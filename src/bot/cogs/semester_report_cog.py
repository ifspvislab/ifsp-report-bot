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

# from reports import SemesterReport, SemesterReportData
from services import (
    CoordinatorService,
    MemberService,
    ParticipationService,
    ProjectService,
    ReportService,
)
from services.report_service import (
    InvalidMember,
    InvalidRequestPeriod,
    ParticipationDoesNotExisInServer,
    ParticipationDoesNotExist,
    ProjectDoesNotExist,
)

logger = settings.logging.getLogger(__name__)


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
        errors = []

        try:

            student = self.member_service.find_member_by_type(
                "discord_id", interaction.user.id
            )

            if student is None:
                raise InvalidMember(
                    "Você não está cadastrado em nenhum projeto de ensino!"
                )

            project = self.project_service.find_project_by_type(
                "discord_server_id", interaction.channel_id
            )

            if project is None:
                raise ProjectDoesNotExist(
                    "Este canal não está cadastrado como projeto."
                )

            invalid_request_period = self.report_service.invalid_request_period()

            valid_member_for_request = self.report_service.verifiy_member_validity(
                interaction.user.id,
                student.registration,
                interaction.channel_id,
                project.project_id,
                project.coordinator_id,
            )

            if valid_member_for_request and not invalid_request_period:
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

        except ParticipationDoesNotExist as exception:
            logger.error(
                "User %s does not participate of any project", interaction.user.name
            )
            await interaction.response.send_message(exception)

        except ParticipationDoesNotExisInServer as exception:
            logger.error(
                "User %s tried to generate the semester report in the wrong project server",
                interaction.user.name,
            )
            await interaction.response.send_message(exception)

        except InvalidMember as exception:
            logger.error(
                "User %s without permission tried to generate the semester report",
                interaction.user.id,
            )
            await interaction.response.send_message(exception)

        except InvalidRequestPeriod as exception:
            logger.error(
                "User %s tried to generate semester report outside of the allowed period",
                interaction.user.id,
            )
            await interaction.response.send_message(exception)

        except ProjectDoesNotExist as exception:
            logger.error("No project found for server %s", interaction.channel_id)
            await interaction.response.send_message(str(exception))

        if errors:
            embed = discord.Embed(
                title=":sob: Problemas com a sua requisição", color=0xFF0000
            )
            for index, error in enumerate(errors):
                embed.add_field(name=f"Erro {index+1}", value=str(error), inline=False)

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
        student = self.member_service.find_member_by_type(
            "discord_id", interaction.user.id
        )

        project = self.project_service.find_project_by_type(
            "discord_server_id", interaction.channel_id
        )

        validity = self.report_service.verifiy_member_validity(
            interaction.user.id,
            student.registration,
            interaction.channel_id,
            project.project_id,
            project.coordinator_id,
        )

        if validity:

            project_title, coordinator_name, student_name = validity

            generated_report = self.report_service.generate_semester_report(
                project_title=project_title,
                project_manager=coordinator_name,
                student_name=student_name,
                planned_activities=self.planned_activities.value.strip(),
                performed_activities=self.performed_activities.value.strip(),
                results=self.results.value.strip(),
            )

            report = generated_report

            month = datetime.now().strftime("%B")

            name_of_report = (f"RelatorioSemestral_Ensino_{month}").upper()
            name_of_report += (f"_{student.name}").upper() + ".pdf"

            student_first_name = student_name.split()[0]
            content = f"Sucesso, {student_first_name}! Aqui está"
            content += " o relatório semestral em formato PDF:"
            await interaction.response.send_message(
                content=content,
                file=discord.File(
                    BytesIO(report),
                    filename=name_of_report,
                    spoiler=False,
                ),
            )
