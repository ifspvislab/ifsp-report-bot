"""
attendance_cog
====

Has the commands and the tasks necessary to create attendance sheets

Classes:
    - AttendanceCog: The cog that unifies all attendance sheet code that is 
    related to the bot

"""


import calendar
from datetime import datetime, time, timedelta, timezone
from io import BytesIO

import discord
from discord import File, app_commands
from discord.ext import commands, tasks

import settings
from data import MONTHS
from services import AttendanceService, StudentService

from .bot_utils import show_errors
from .modals import AttendanceSheetForm

logger = settings.logging.getLogger(__name__)


# Brasília timezone
current_timezone = timezone(offset=timedelta(hours=-3))


class AttendanceCog(commands.Cog):
    """
    Class that unifies all attendance sheet code that is related to the bot

    """

    def __init__(
        self,
        bot: commands.Bot,
        student_service: StudentService,
    ) -> None:
        """
        Loads instance with the needed information and starts the sheet creation task

        """
        self.bot = bot
        self.student_service = student_service
        self.attendance_service = AttendanceService()
        # pylint: disable-next=no-member
        self.is_last_day.start()

    @app_commands.command(
        name="adicionar-presenca",
        description="Adiciona uma nova presença na folha de frequência",
    )
    async def add_student_attendance(self, interaction: discord.Interaction) -> None:
        """
        Command that exibits a modal to insert and send data from a new attendance.
        Only exibits said modal if the user is allowed.
        Calls attendance_service for data validation
        """
        errors = []
        student = self.student_service.find_student_by_discord_id(interaction.user.id)

        if student is None:
            errors.append("Você não tem permissão para gerenciar a folha de presença")
            logger.warning(
                "User %s without permission tried to add new data into attendance sheet",
                interaction.user.name,
            )
        if not errors:
            logger.info("Attendance sheet user %s", interaction.user.name)
            await interaction.response.send_modal(
                AttendanceSheetForm(self.attendance_service)
            )
        else:
            await interaction.response.send_message(embed=show_errors(errors))

    @tasks.loop(time=time(hour=12, minute=0, tzinfo=current_timezone))
    async def is_last_day(self):
        """
        Verifies every 12:00 AM if the current day is the last day of the month
        If it is, calls create_all_attendance_sheets
        """
        today = datetime.now()
        # last_day recieves a tuple with the last weekday[0] and the last day[1]
        last_day = calendar.monthrange(year=today.year, month=today.month)
        if today.day == last_day[1]:
            logger.info("Creating and sending all attendance sheets")
            await self.create_all_attendance_sheets()
            logger.info("Attendance sheets task finished")

    async def create_all_attendance_sheets(self) -> None:
        """
        Gets all the students inside the attendances database, creates all attendance sheets
        and send them to each student
        """
        all_students_id = self.attendance_service.get_all_students_id()
        for student_id in all_students_id:
            student = self.student_service.find_student_by_discord_id(student_id)
            if student is None:
                continue

            # If the user saved doesn't exist, it won't create the sheet
            user = self.bot.get_user(student_id)
            if user is None:
                continue

            file = self.attendance_service.create_sheet(
                student_id=student_id,
                student_registration=student["registration"],
                student_name=student["name"],
                project_name=student["project"]["title"],
            )

            first_name = student["name"].split()[0]
            month_str = MONTHS[datetime.now().month - 1]

            # Breaking line to not exceed 100 characters
            sheet_name = "folha-de-frequencia-"
            sheet_name += f"{month_str}-{first_name}-{student['registration']}.pdf"

            await user.send(
                content=f"{first_name}, aqui está a sua folha de presença em formato PDF:",
                file=File(
                    BytesIO(file),
                    filename=sheet_name,
                    spoiler=False,
                ),
            )
