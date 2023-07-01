"""
Classes:
    - SemesterReportForm: A form that allows the user to send the needed data to create
    the semester report.
"""


from datetime import datetime
from io import BytesIO

import discord
from discord import ui

import settings
from reports import SemesterReport, SemesterReportData
from services.member_service import MemberService

# from discord.ext import commands


# from services.report_service import ReportService

logger = settings.logging.getLogger(__name__)

# class SemesterReportCog(commands.Cog):
#     def __init__(
#         self,
#         bot: commands.Bot,
#         member_service: MemberService,
#     ) -> None:

#         self.bot = bot
#         self.member_service = member_service

#     @commands.command(
#         name="relatorio-semestral",
#         description="Gera um relatório de ensino semestral",
#     )

#     async def open_semester_report_form(self, interaction: discord.Interaction):
#         """
#         Command 'relatorio-semestral' to open the semester report form.

#         :param interaction: The Discord interaction object.
#         :type interaction: discord.Interaction

#         """
#         student = self.member_service.find_member_by_type(
#             "discord_id", interaction.user.id
#         )

#         errors = []
#         if student is None:
#             errors.append("Você não tem permissão para gerar relatório semestral")
#             logger.warning(
#                 "User %s without permission tried to generate monthly report",
#                 interaction.user.name,
#             )

#         report_service = ReportService()
#         if report_service.invalid_request_period():
#             errors.append(
#                 "O período de submissões ocorre entre os dias 23 a 31 "
#                 "de julho e 01 a 10 de dezembro."
#             )
#             logger.warning(
#                 "User %s attempted to generate the semester report outside the allowed period.",
#                 interaction.user.name,
#             )

#         if not errors:
#             logger.info("Semester report user %s", interaction.user.name)
#             await interaction.response.send_modal(SemesterReportForm(self.member_service))
#         else:
#             embed = discord.Embed(title=":sob: Problemas com a sua requisição")
#             for index, error in enumerate(errors):
#                 embed.add_field(name=f"Erro {index+1}", value=error, inline=False)

#             await interaction.response.send_message(embed=embed)


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
        # bot: commands.Bot,
        # student_service: StudentService,
        member_service: MemberService,
    ) -> None:
        """
        Initialize the SemesterReportForm instance.

        :param member_service: An instance of the MemberService class.
        :type member_service: MemberService
        """
        super().__init__(title="Relatório Semestral")
        # self.student_service = student_service
        # self.bot = bot
        self.member_service = member_service

    async def on_submit(self, interaction: discord.Interaction, /):
        """
        Handle the submit event of the form.

        This method is called when the user submits the form.
        It generates the semester report based on the form data and sends it to the user.

        :param interaction: The Discord interaction object.
        :type interaction: discord.Interaction

        """
        student = self.member_service.find_member_by_type(
            "discord_id", interaction.user.id
        )

        if student is None:
            await interaction.response.send_message(
                "Você não tem permissão para gerar relatório semestral"
            )
        else:
            data = SemesterReportData(
                # apenas testando com student.name para ver se os campos são preenchidos
                # corretamente
                project_title=student.name,
                project_manager=student.name,
                student_name=student.name,
                planned_activities=self.planned_activities.value.strip(),
                performed_activities=self.performed_activities.value.strip(),
                results=self.results.value.strip(),
            )

            report = SemesterReport(data)
            month = datetime.now().strftime("%B")

            name_of_report = (f"RelatorioSemestral_Ensino_{month}").upper()
            name_of_report += (f"_{student.name}").upper() + ".pdf"

            student_first_name = student.name.split()[0]
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
