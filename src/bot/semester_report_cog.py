"""
semester_report_cog.py

This module defines classes for modal forms used in Discord bot interactions.

Classes:
- SemesterReportForm: Represents a monthly report form for generating monthly reports.

"""
from datetime import datetime
from io import BytesIO

import discord
from discord import ui

import settings
from reports import SemesterReport, SemesterReportData
from services import StudentService

logger = settings.logging.getLogger(__name__)


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

    def __init__(
        self,
        student_service: StudentService,
    ) -> None:
        """
        Initialize the SemesterReportForm instance.

        :param student_service: An instance of the StudentService class.
        :type student_service: StudentService

        """
        super().__init__(title="Relatório Semestral")
        self.student_service = student_service

    async def on_submit(self, interaction: discord.Interaction, /):
        """
        Handle the submit event of the form.

        This method is called when the user submits the form.
        It generates the semester report based on the form data and sends it to the user.

        :param interaction: The Discord interaction object.
        :type interaction: discord.Interaction

        """
        student = self.student_service.find_student_by_discord_id(interaction.user.id)

        if student is None:
            await interaction.response.send_message(
                "Você não tem permissão para gerar relatório semestral"
            )
        else:
            data = SemesterReportData(
                project_title=student["project"]["title"],
                project_manager=student["project"]["professor"],
                student_name=student["name"],
                planned_activities=self.planned_activities.value.strip(),
                performed_activities=self.performed_activities.value.strip(),
                results=self.results.value.strip(),
            )

            report = SemesterReport(data)
            month = datetime.now().strftime("%B")

            name_of_report = (f"RelatorioSemestral_Ensino_{month}").upper()
            name_of_report += (f"_{student['name']}").upper() + ".pdf"

            student_first_name = student["name"].split()[0]
            report_name = name_of_report
            content = f"Sucesso, {student_first_name}! Aqui está"
            content += " o relatório semestral em formato PDF:"
            await interaction.response.send_message(
                content=content,
                file=discord.File(
                    BytesIO(report.generate()),
                    filename=report_name,
                    spoiler=False,
                ),
            )
