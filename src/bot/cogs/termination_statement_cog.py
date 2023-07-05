""" . """

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
    """."""

    def __init__(
        self,
        member_service: MemberService,
        project_service: ProjectService,
        participation_service: ParticipationService,
        coordinator_service: CoordinatorService,
    ):
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
        """."""

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
    .
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

        super().__init__(title="Termo de Encerramento")
        self.member_service = member_service
        self.project_service = project_service
        self.participation_service = participation_service
        self.coordinator_service = coordinator_service

    async def on_submit(self, interaction: discord.Interaction, /):
        """
        .
        """

        member = self.member_service.find_member_by_type(
            "discord_id", interaction.user.id
        )

        participations = self.participation_service.find_participation_by_type(
            "registration", member.registration
        )

        project = self.project_service.find_project_by_type(
            "discord_server_id", interaction.guild_id
        )

        coordinator = self.coordinator_service.find_coordinator_by_type(
            "coord_id", project.coordinator_id
        )
        print(participations)
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

                # start_date_project = datetime(
                #     project.data_inicio.year,
                #     project.data_inicio.month,
                #     student["project"]["start_date"].day,
                # ).date()
                # end_date_project = datetime(
                #     student["project"]["end_date"].year,
                #     student["project"]["end_date"].month,
                #     student["project"]["end_date"].day,
                # ).date()
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
                # with open(
                #     'assets/data/participations.csv', "a", encoding="UTF-8"
                # ) as file:
                #     for row in file:
                #         if participation.registration in row
                #           file.write(f""" """)
                # participation.final_date = termination_date

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
                print(error)
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
