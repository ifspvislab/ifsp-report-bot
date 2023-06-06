"""
modals.py

This module defines classes for modal forms used in Discord bot interactions.

Classes:
- MonthyReportForm: Represents a monthly report form for generating monthly reports.

"""

from io import BytesIO
from typing import Optional

import discord
from discord import ui
from discord.utils import MISSING

from reports import MonthlyReport, MonthlyReportData

<<<<<<< HEAD
from services import AdminService, StudentService

=======
from services import AdminService, StudentService

>>>>>>> 9ce33cf6fcdce6cd1b75b355b398f174b3ce3a63


class AddCoordenatorModal(ui.Modal):

    prontuario = ui.TextInput(label="Prontuário:", style=discord.TextStyle.short)
    discord_id = ui.TextInput(label="Discord id:", style=discord.TextStyle.short)
    name = ui.TextInput(label="Nome:", style=discord.TextStyle.short)
    email = ui.TextInput(label="Email:", style=discord.TextStyle.short)

    def __init__(
        self,
        admin_service: AdminService,
    ) -> None:
        super().__init__(title="Adicionar coordenador")
        self.admin_service = admin_service

    async def on_submit(self, interaction: discord.Interaction):

        admin = ...

        if admin is None:
            await interaction.response.send_message(
                "Você não tem permissão para gerar relatório mensal"
            )
        else:
            ...


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
