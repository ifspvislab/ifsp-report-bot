""" . """

import locale
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
