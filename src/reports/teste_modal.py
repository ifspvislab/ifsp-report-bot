"""
teste_modal.py

This module is a test to see if the modal is functioning correctly for the creation
of a semester report.

Classes:
- SemesterReportForm: Represents a semester report form for generating semester reports.

"""

from datetime import datetime
from io import BytesIO

import discord
import semester_report
from decouple import config
from discord import app_commands, ui
from discord.ext import commands

# from reports import SemesterReport, SemesterReportData


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

"""This class sets the bot as online"""


class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=1110680471987298356))
        self.synced = True
        print(f"Bot {bot.user.name} is online")


bot = abot()
tree = app_commands.CommandTree(bot)

"""This class represents the form/modal that generates the semester report"""


class SemesterReportForm(ui.Modal, title="Relatório Semestral"):

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

    async def on_submit(self, interaction: discord.Interaction):

        data = semester_report.SemesterReportData(
            planned_activities=self.planned_activities.value.strip(),
            performed_activities=self.performed_activities.value.strip(),
            results=self.results.value.strip(),
        )

        report = semester_report.SemesterReport(data)
        # now = datetime.now()
        month_name = datetime.now().strftime("%B")
        report_name = f"Relatorio-Semestral-{month_name}.pdf"

        await interaction.response.send_message(
            content="Aqui está o relatório semestral em formato PDF:",
            file=discord.File(
                BytesIO(report.generate()),
                filename=report_name,
                spoiler=False,
            ),
        )


@tree.command(
    name="relatorio_semestral",
    description="Gera um relatório de ensino semestral",
    guild=discord.Object(id=1110680471987298356),
)
async def modal(interaction: discord.Interaction):
    await interaction.response.send_modal(SemesterReportForm())


DISCORD_BOT_TOKEN = config("DISCORD_BOT_TOKEN")
bot.run(DISCORD_BOT_TOKEN)
