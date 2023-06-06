"""Services for administrator"""
import discord
from discord import app_commands, ui
from discord.ext import commands

"""Environment value, undefined at this moment"""
ID_ADMIN = ...


def is_admin(interaction: discord.Interaction):
    """Check if it's the administrator doing the command by the discord id"""
    if interaction.user.id == ID_ADMIN:
        return True
    return False


class AdminService:
    def __init__(
        self,
    ):
        ...

    @app_commands.command(
        name="cadastrar-coordenador", description="registrar aluno via modal"
    )
    @app_commands.check(is_admin)
    async def add_coordenator(self, interaction: discord.Interaction):
        """Verification and call for pop up the modal"""
        await interaction.response.send_modal(
            # AddCoordenatorModal()
        )

    @add_coordenator.error
    async def add_coordenator_error(self, interaction: discord.Interaction, error):
        """Treating error if it's not the admin"""
        await interaction.response.send_message("Não permitido!")
