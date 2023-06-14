from datetime import date

import discord
from discord import ui

from data import _load_participations, _load_projects, _load_students, add_participation
from services import ProfessorService


class Participation(discord.ui.View):
    """
    Class representing the participation assingment.

    Creates a command to assign a participation.
    """

    chosen_project = ui.TextInput(
        label="Projeto:",
        style=discord.InputStyle.singleline,
        min_lenght=10,
        max_lenght=80,
        row=3,
    )  # Receives the project name.

    chosen_member = ui.TextInput(
        label="Prontuário do aluno:",
        style=discord.InputStyle.singleline,
        min_lenght=1,
        max_lenght=9,
        placeholder="SPXXXXXXX",
        row=1,
    )  # Receives the student registration.

    pday = ui.TextInput(
        label="Dia:",
        style=discord.InputStyle.singleline,
        min_length=1,
        max_length=2,
        placeholder="DD",
        row=2,
    )  # Receives the day of the participation.
    pmonth = ui.TextInput(
        label="Mês:",
        style=discord.InputStyle.singleline,
        min_length=1,
        max_length=2,
        placeholder="MM",
        row=2,
    )  # receives the month of the participation.
    pyear = ui.TextInput(
        label="Ano:",
        style=discord.InputStyle.singleline,
        min_length=4,
        max_length=4,
        placeholder="YYYY",
        row=2,
    )  # receives the year of the participation.

    def __init__(self, professor_service=ProfessorService) -> None:
        super().__init__(title="Participação")
        self.professor_service = professor_service

    async def on_verification(self, interaction=discord.Interaction, /):
        """
        This method is called when the command to add participation is called.
        It verifies if the information inputed is valid, and creates the participation as asked.
        """

        professor = self.professor_service.find_professor_by_discord_id(
            interaction.user.id
        )

        if professor is None:
            await interaction.response.send_message(
                "Você não tem permissão para registrar uma participação."
            )  # Verifies if the command was activated by a professor.
        else:
            """
            Verifies if the information inputed in the modal is valid.
            """

            projects = _load_projects()
            students = _load_students()
            referencial_date = projects["start_date"]
            final_date = projects["end_date"]
            start_participation_date = date(
                int(self.pyear), int(self.pmonth), int(self.pdate)
            )

            if start_participation_date < referencial_date:
                await interaction.response.send_message(
                    "A data inserida é inválida, pois é anterior ao início do projeto."
                )

            if final_date < start_participation_date:
                await interaction.response.send_message(
                    "A data inserida é inválida, pois é após o fim do projeto."
                )

            if str(self.chosen_project) != projects["title"]:
                await interaction.response.send_message(
                    "O projeto inserido inexiste nos registros."
                )

            if str(self.chosen_member) != students["registration"]:
                await interaction.response.send_message(
                    "O aluno inserido inexiste nos registros."
                )

            participations = _load_participations

            for participation in participations:
                if (
                    participation["registration"] == self.chosen_member
                    and participation["title"] == self.chosen_project
                ):
                    await interaction.response.send_message(
                        "O aluno já está registrado nesse projeto."
                    )

            if (
                referencial_date < start_participation_date < final_date
                and str(self.chosen_project) == projects["title"]
                and str(self.chosen_member) == students["registration"]
            ):
                add_participation()
