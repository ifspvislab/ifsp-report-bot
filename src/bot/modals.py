"""
modals.py

This module defines classes for modal forms used in Discord bot interactions.

Classes:
- MonthyReportForm: Represents a monthly report form for generating monthly reports.
- AttendanceSheetForm: A Class modal that represents a form for adding a new project attendance

"""

from datetime import datetime, time

from io import BytesIO

import discord
from discord import ui

from reports import MonthlyReport, MonthlyReportData
from services import AttendanceService, StudentService


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


class AttendanceSheetForm(ui.Modal):
    """
    A Class modal that represents a form for adding a new project attendance
    """

    day_field = ui.TextInput(label="Data da presença", placeholder="Dia do mês", required=False)
    entry_time_field = ui.TextInput(label="Hora de entrada", placeholder="hh:mm")
    exit_time_field = ui.TextInput(label="Hora de saída", placeholder="hh:mm")

    def __init__(self, attendance_service: AttendanceService):
        super().__init__(title="Folha de frequência")
        self.attendance_service = attendance_service
    

    async def on_submit(self, interaction: discord.Interaction) -> None:
        errors = []

        if self.day_field.value is None:
            day = datetime.now()
        else:
            day = self.attendance_service.validate_day(self.day_field.value)
            if day is None:
                # If the day is invalid, we can't get it's weekday, so the program
                # returns just this error without appending it in the errors list
                embed = discord.Embed(title="Opa, parece que encontramos problemas!")
                embed.add_field(name="Erro 1", value="O dia passado é inválido", inline=False)
                await interaction.response.send_message(embed=embed)
                return  
        
        entry_time = self.attendance_service.validate_time(
            weekday=day.weekday(),
            param_time=self.entry_time_field.value
        )
        if entry_time is None:
            errors.append("O horário de entrada é inválido.")

        exit_time = self.attendance_service.validate_time(
            weekday=day.weekday(),
            param_time=self.exit_time_field.value
        )
        if exit_time is None:
            errors.append("O horário de saída é inválido.")

        if entry_time is not None and exit_time is not None:
            if self.attendance_service.is_entry_before(entry_time, exit_time):
                errors.append("O horário de saída não pode ser anterior ao de entrada.")

        if not errors:
            await interaction.response.send_message("Dados válidos")
        else:
            embed = discord.Embed(title="Opa, parece que encontramos problemas!")
            for index, error in enumerate(errors):
                embed.add_field(name=f"Erro {index+1}", value=error, inline=False)

            await interaction.response.send_message(embed=embed)
        
