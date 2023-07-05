""" 
Classes:
    - TerminationStatementCog: Cog that manages the interactions 
    related to the termination statement
    - TerminationStatementForm: Form tha allows the user to send
    the needed data to create the semester report.


"""

import locale
from datetime import datetime
from io import BytesIO

import discord
from discord import app_commands, ui
from discord.ext import commands

from reports import TerminationStatement, TerminationStatementData
from services import (
    CoordinatorService,
    MemberService,
    ParticipationService,
    ProjectService,
)

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")


class TerminationStatementCog(commands.Cog):
    """
    Command to display the TerminationStatementForm

    """

    def __init__(
        self,
        member_service: MemberService,
        project_service: ProjectService,
        participation_service: ParticipationService,
        coordinator_service: CoordinatorService,
    ):
        """
        Loads the services needed to create the termination statement form
        """
        super().__init__()
        self.member_service = member_service
        self.project_service = project_service
        self.participation_service = participation_service
        self.coordinator_service = coordinator_service

    @app_commands.command(
        name="termo-encerramento",
        description="Gera um termo de encerramento das atividades em um projeto.",
    )
    async def open_termination_statement_form(self, interaction: discord.Interaction):
        """
        Command 'termo-encerramento' to open the termination statement form.

        :param interaction: The Discord interaction object.
        :type interaction: discord.Interaction
        """

        member = self.member_service.find_member_by_type(
            "discord_id", interaction.user.id
        )

        if member is None:
            await interaction.response.send_message(
                "Você não tem permissão para gerar o termo de encerramento."
            )
        else:
            await interaction.response.send_modal(
                TerminationStatementForm(
                    self.member_service,
                    self.project_service,
                    self.participation_service,
                    self.coordinator_service,
                )
            )


class TerminationStatementForm(ui.Modal):
    """
    Class that represents a termination statement form,
    defining a modal form.
    """

    termination_date = ui.TextInput(
        label="Data para o encerramento",
        min_length=10,
        max_length=10,
        placeholder="dd/mm/aaaa",
        style=discord.TextStyle.short,
    )
    termination_reason = ui.TextInput(
        label="Motivo do encerramento",
        style=discord.TextStyle.paragraph,
        min_length=60,
        max_length=250,
    )

    def __init__(
        self,
        member_service: MemberService,
        project_service: ProjectService,
        participation_service: ParticipationService,
        coordinator_service: CoordinatorService,
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
        self.member_service = member_service
        self.project_service = project_service
        self.participation_service = participation_service
        self.coordinator_service = coordinator_service

    async def on_submit(self, interaction: discord.Interaction, /):
        """
        Submits the modal into the form

        :param interaction: Discord interaction object
        :type interaction: discord.Interaction
        """

        member = self.member_service.find_member_by_type(
            "discord_id", interaction.user.id
        )

        if member is None:
            return []

        project = self.project_service.find_project_by_type(
            "discord_server_id", interaction.guild_id
        )

        if project is None:
            return []

        participations = self.participation_service.find_participation_by_type(
            "project_id", project.project_id
        )

        if participations is None:
            return []

        coordinator = self.coordinator_service.find_coordinator_by_type(
            "coord_id", project.coordinator_id
        )

        if (
            self.termination_date.value[2] != "/"
            or self.termination_date.value[5] != "/"
        ):
            await interaction.response.send_message(
                "Coloque as barras da data, conforme no modelo dd/mm/aaaa"
            )
        else:
            try:
                termination_date = self.termination_date.value.split(sep="/")

                termination_date = datetime(
                    int(termination_date[2]),
                    int(termination_date[1]),
                    int(termination_date[0]),
                ).date()

                days_difference = project.end_date - project.start_date

                input_days_difference = project.end_date - termination_date

                if (
                    input_days_difference >= days_difference
                    or input_days_difference.days <= 0
                ):
                    await interaction.response.send_message(
                        "Insira uma data dentro do período de execução do projeto!"
                    )
                current_time = datetime.now().date()
                if current_time > termination_date:
                    await interaction.response.send_message(
                        "Insira o dia de hoje ou uma data futura!"
                    )

                data = TerminationStatementData(
                    student_name=member.name,
                    student_code=member.registration,
                    project_name=project.title,
                    project_manager=coordinator.name,
                    termination_date=self.termination_date.value,
                    termination_reason=self.termination_reason.value,
                )

                termination_statement = TerminationStatement(data)

                document_name = f"""termo-encerramento-{member.name}-
                    {member.registration}-{project.title}.pdf"""

                await interaction.response.send_message(
                    content="Termo de Encerramento gerado.",
                    file=discord.File(
                        BytesIO(termination_statement.generate()),
                        filename=document_name,
                        spoiler=False,
                    ),
                )
            except ValueError as expection:
                error = str(expection)

                if "invalid literal" in error:
                    await interaction.response.send_message(
                        "Coloque um número nos campos **dia**/**mês**/**ano**!"
                    )
                if "1..12" in error:
                    await interaction.response.send_message(
                        "Coloque um mês de 01 a 12."
                    )
                if "day" in error:
                    await interaction.response.send_message(
                        "Coloque um dia válido para o mês inserido."
                    )
                else:
                    await interaction.response.send_message(
                        "Ocorreu um erro inesperado na sua solicitação, tente novamente."
                    )
