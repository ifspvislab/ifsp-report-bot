# import discord
# from discord import app_commands
# from discord.ext import commands

# from bot.modals import AddCoordinatorModal

# class AdminCommands(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @app_commands.command(
#         name="cadastrar-coordenador", description="registrar coordenador via modal"
#     )
#     @app_commands.check(is_admin)
#     async def add_coordinator(self, interaction: discord.Interaction):
#         """Verification and call for pop up the modal"""
#         await interaction.response.send_modal(
#             AddCoordinatorModal()
#         )

#     @add_coordinator.error
#     async def add_coordinator_error(self, interaction: discord.Interaction, error):
#         """Treating error if it's not the admin"""
#         await interaction.response.send_message("Peça ao administrador para executar este comando, você não está autorizado!")


# async def setup(bot):
#     await bot.add_cog(AdminCommands(bot))
