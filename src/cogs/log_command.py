"""Cog for LogCommand"""
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog
from services.log_service import LogService
from services.coordinator_service import CoordinatorService


class LogCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="log", description="Create the log file")
    @app_commands.check(CoordinatorService.is_coordinator)
    async def log_file(self, interaction: discord.Interaction, data: str = None):
        logs = LogService.get_logs()
        if data is None:
            LogService.create_pdf(logs, 1)

        if data is not None:
            try:
                LogService.date_validation("09/10/2023", data)
            except:
                await interaction.response.send_message(
                    "Data incorreta, digite no formato 'data_inicio-data_fim'. Ex:01/09/2023-12/10/2023",
                    ephemeral=True,
                )

            LogService.create_pdf(logs, 2, data)

        with open("D:/Faculdade/VisLab/ifsp-report-bot/src/cogs/log.pdf", "rb") as file:
            await interaction.response.send_message(
                file=discord.File(file, filename="log.pdf"), ephemeral=True
            )

    @log_file.error
    async def log_file_error(self, interaction: discord.Interaction, error):
        """Treating error if it's not the coordinator"""
        await interaction.response.send_message(
            f"Apenas o coordenador tem acesso ao comando!"
        )


async def setup(bot):
    await bot.add_cog(LogCommand(bot))
