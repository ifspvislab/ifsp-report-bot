"""
Cog for handling log commands.
"""
import discord
from discord import app_commands
from discord.ext import commands

from data import LogData
from reports import LogReport
from services import IncorrectDateFilter, LogService
from services.coordinator_service import is_coordinator


class LogCommand(commands.Cog):
    """
    Cog that handles log commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="log", description="Create the log file")
    @app_commands.describe(
        start_date="Data inicial para a procura de registros. Ex:01/09/2023",
        end_date="Data final para a procura de registros. Ex:01/09/2023",
        student_id="Registros apenas com o ID inserido",
    )
    @app_commands.check(is_coordinator)
    async def log_file(
        self,
        interaction: discord.Interaction,
        start_date: str = None,
        end_date: str = None,
        student_id: str = None,
    ):
        """
        Command for creating a log file.

        Parameters:
            - interaction: The interaction object.
            - start_date: Optional start date for log filtering.
            - end_date: Optional end date for log filtering.
            - member_id: Optional member ID for log filtering.

        Returns:
            None
        """
        server_id = interaction.guild.id
        project_id = LogService.get_project_id_by_server_id(
            self=LogService, server_id=server_id
        )

        if student_id is not None and not LogService.check_student_in_project(
            self=LogService, student_id=int(student_id)
        ):
            await interaction.response.send_message(
                "ID inválido",
                ephemeral=True,
            )
            return

        if start_date is None and end_date is None:
            if student_id is not None:
                LogReport.create_pdf(
                    project_id=project_id,
                    value=3,
                    student_id=str(student_id),
                )
            else:
                LogReport.create_pdf(project_id=project_id)
        elif end_date is not None and start_date is None:
            await interaction.response.send_message(
                "É preciso de uma data de inicio. Ex:01/09/2023",
                ephemeral=True,
            )
        elif start_date is not None:
            if end_date is None:
                end_date = LogService.formatted_get_date(self=LogService)

            try:
                LogService.date_validation(
                    self=LogService,
                    date="09/10/2023",
                    start_date=start_date,
                    end_date=end_date,
                )
            except IncorrectDateFilter:
                await interaction.response.send_message(
                    "Data incorreta, digite no formato dd/MM/aaaa. Ex:01/09/2023",
                    ephemeral=True,
                )
                return

            if student_id is not None:
                LogReport.create_pdf(
                    project_id=project_id,
                    value=4,
                    start_date=start_date,
                    end_date=end_date,
                    student_id=str(student_id),
                )
            else:
                LogReport.create_pdf(
                    project_id=project_id,
                    value=2,
                    start_date=start_date,
                    end_date=end_date,
                )

        if LogData.log_file_validation(self=LogData):
            with open(
                "D:/Faculdade/VisLab/ifsp-report-bot/src/bot/cogs/log.pdf", "rb"
            ) as file:
                await interaction.response.send_message(
                    file=discord.File(file, filename="teste.pdf"), ephemeral=True
                )
        else:
            await interaction.response.send_message(
                "Arquivo possui mais de 25Mb, portanto não pode ser enviado via Discord"
                + " utilize o filtro de data ou id para compactar"
            )

    @log_file.error
    async def log_file_error(self, interaction: discord.Interaction, error):
        """Treating error if it's not the coordinator"""
        print(error)  # Pylint-problem
        await interaction.response.send_message(
            "Apenas o coordenador tem acesso ao comando!", ephemeral=True
        )


async def setup(bot):
    """
    Function to add the LogCommand cog to the bot.
    """
    await bot.add_cog(LogCommand(bot))
