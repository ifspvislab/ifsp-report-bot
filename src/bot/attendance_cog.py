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
from discord import File, app_commands, ui
from discord.ext import commands, tasks

import settings
from data.attendances_data import MONTHS
from services import AttendanceService, StudentService
from services.attendance_service import (
    DayOutOfRange,
    EntryTimeAfterExitTime,
    InvalidDate,
    InvalidTime,
    TimeOutOfRange,
)

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
        student = self.student_service.find_student_by_discord_id(interaction.user.id)

        if student is None:
            logger.warning(
                "User %s without permission tried to add new data into attendance sheet",
                interaction.user.name,
            )
            await interaction.response.send_message(
                "Você não tem permissão para adicionar novas presenças"
            )

        else:
            logger.info("Attendance sheet user %s", interaction.user.name)
            await interaction.response.send_modal(
                AttendanceSheetForm(self.attendance_service)
            )

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
                log_msg = f"Student with id {student_id}"
                log_msg += "in attendances database not inside the students database"
                logger.info(log_msg)
                continue

            # If the user saved doesn't exist, it won't create the sheet
            user = self.bot.get_user(student_id)
            if user is None:
                log_msg = f"Student with id {student_id}"
                log_msg += "in attendances database couldn't be found by discord bot"
                logger.info(log_msg)
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

            log_msg = f"Attendance data for the student with id {student_id}"
            log_msg += "was successfuly created. Sending..."
            logger.info(log_msg)

            await user.send(
                content=f"{first_name}, aqui está a sua folha de presença em formato PDF:",
                file=File(
                    BytesIO(file),
                    filename=sheet_name,
                    spoiler=False,
                ),
            )


class AttendanceSheetForm(ui.Modal):
    """
    A Class modal that represents a form for adding a new project attendance
    """

    day_field = ui.TextInput(
        label="Data da presença", placeholder="Dia do mês", required=False
    )
    entry_time_field = ui.TextInput(label="Hora de entrada", placeholder="hh:mm")
    exit_time_field = ui.TextInput(label="Hora de saída", placeholder="hh:mm")

    def __init__(self, attendance_service: AttendanceService, /):
        """
        Initialize the AttendanceSheetForm instance.

        :param attendance_service: An instance of the AttendanceService class.
        :type attendance_service: AttendanceService

        """
        super().__init__(title="Folha de frequência")
        self.attendance_service = attendance_service

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        """
        Handle the submit event of the form.

        This method is called when the user submits the form.
        It tests the data sent by the user and if it is valid, creates a new attendance register

        :param interaction: The Discord interaction object.
        :type interaction: discord.Interaction

        """

        try:
            self.attendance_service.create(
                day=self.day_field.value,
                entry_time=self.entry_time_field.value,
                exit_time=self.exit_time_field.value,
                user=interaction.user.id,
            )

            await interaction.response.send_message("Tudo certo! Presença cadastrada")

        except (
            InvalidDate,
            InvalidTime,
            DayOutOfRange,
            TimeOutOfRange,
            EntryTimeAfterExitTime,
        ) as exception:
            await interaction.response.send_message(exception.args[0])
