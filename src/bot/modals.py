"""
modals.py

This module defines classes for modal forms used in Discord bot interactions.

Classes:
- MonthyReportForm: Represents a monthly report form for generating monthly reports.

"""

from io import BytesIO

import discord
from discord import ui

from reports import MonthlyReport, MonthlyReportData, SemesterReport, SemesterReportData
from services import StudentService


class MonthyReportForm(ui.Modal):
    """
    Class representing a monthly report form.

    This class defines a modal form for generating monthly reports.

    """

    planned_activities = ui.TextInput(
        label="Atividades planejadas",
        style=discord.TextStyle.paragraph,
        min_length=200,
        max_length=500,
    )
    performed_activities = ui.TextInput(
        label="Atividades realizadas",
        style=discord.TextStyle.paragraph,
        min_length=200,
        max_length=500,
    )
    results = ui.TextInput(
        label="Resultados obtidos",
        style=discord.TextStyle.paragraph,
        min_length=200,
        max_length=500,
    )

    def __init__(
        self,
        student_service: StudentService,
    ) -> None:
        """
        Initialize the MonthyReportForm instance.

        :param student_service: An instance of the StudentService class.
        :type student_service: StudentService

        """
        super().__init__(title="Relatório Mensal")
        self.student_service = student_service

    async def on_submit(self, interaction: discord.Interaction, /):
        """
        Handle the submit event of the form.

        This method is called when the user submits the form.
        It generates the monthly report based on the form data and sends it to the user.

        :param interaction: The Discord interaction object.
        :type interaction: discord.Interaction

        """
        student = self.student_service.find_student_by_discord_id(interaction.user.id)

        if student is None:
            await interaction.response.send_message(
                "Você não tem permissão para gerar relatório mensal"
            )
        else:
            data = MonthlyReportData(
                project_title=student["project"]["title"],
                project_manager=student["project"]["professor"],
                student_name=student["name"],
                planned_activities=self.planned_activities.value.strip(),
                performed_activities=self.performed_activities.value.strip(),
                results=self.results.value.strip(),
            )

            report = MonthlyReport(data)

            student_first_name = student["name"].split()[0]
            report_name = (
                f"Relatorio-Mensal-{student_first_name}-{student['registration']}.pdf"
            )

            await interaction.response.send_message(
                content=f"{student_first_name}, aqui está o relatório mensal em formato PDF:",
                file=discord.File(
                    BytesIO(report.generate()),
                    filename=report_name,
                    spoiler=False,
                ),
            )


class SemesterReportForm(ui.Modal):
    """
    Class representing a semester report form.

    This class defines a modal form for generating semester reports.

    """

    planned_activities = ui.TextInput(
        label="Atividades planejadas",
        style=discord.TextStyle.paragraph,
        min_length=300,
        max_length=600,
    )
    performed_activities = ui.TextInput(
        label="Atividades realizadas",
        style=discord.TextStyle.paragraph,
        min_length=300,
        max_length=600,
    )
    results = ui.TextInput(
        label="Resultados obtidos",
        style=discord.TextStyle.paragraph,
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

            student_first_name = student["name"].split()[0]
            report_name = f"Relatorio-Semestral-{student_first_name}-{student['registration']}.pdf"

            await interaction.response.send_message(
                content=f"Sucesso, {student_first_name}! Aqui está o relatório \
                    semestral em formato PDF:",
                file=discord.File(
                    BytesIO(report.generate()),
                    filename=report_name,
                    spoiler=False,
                ),
            )
