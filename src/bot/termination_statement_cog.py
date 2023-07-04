""" . """

import locale
from datetime import datetime
from io import BytesIO

import discord
from discord import ui

from reports import TerminationStatement, TerminationStatementData
from services import StudentService

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")


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

    def __init__(self, student_service: StudentService) -> None:

        super().__init__(title="Termo de Encerramento")
        self.student_service = student_service

    async def on_submit(self, interaction: discord.Interaction, /):
        """
        .
        """

        student = self.student_service.find_student_by_discord_id(interaction.user.id)
        if student is None:
            await interaction.response.send_message(
                "Você não tem permissão para gerar o termo de encerramento."
            )
        else:
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

                    start_date_project = datetime(
                        student["project"]["start_date"].year,
                        student["project"]["start_date"].month,
                        student["project"]["start_date"].day,
                    ).date()
                    end_date_project = datetime(
                        student["project"]["end_date"].year,
                        student["project"]["end_date"].month,
                        student["project"]["end_date"].day,
                    ).date()
                    termination_date = datetime(
                        int(termination_date[2]),
                        int(termination_date[1]),
                        int(termination_date[0]),
                    ).date()

                    days_difference = end_date_project - start_date_project

                    input_days_difference = end_date_project - termination_date

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
                        student_name=student["name"],
                        student_code=student["registration"],
                        project_name=student["project"]["title"],
                        project_manager=student["project"]["professor"],
                        termination_date=self.termination_date.value,
                        termination_reason=self.termination_reason.value,
                    )

                    termination_statement = TerminationStatement(data)

                    document_name = f"""termo-encerramento-{student["name"]}-
                        {student['registration']}-{student["project"]["title"]}.pdf"""

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
