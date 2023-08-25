"""
attendance_cog
====

Has the commands and the tasks necessary to create attendance sheets

Classes:
    - AttendanceCog: The cog that unifies all attendance sheet code that is 
    related to the bot
    - AttendanceSheetForm: A form that allows the user to send the needed data to create
    an attendance

"""


import calendar
from datetime import datetime, time, timedelta, timezone
from io import BytesIO

import discord
from discord import File, app_commands, ui
from discord.ext import commands, tasks

import settings
from data import MONTHS, Member
from services import (
    AttendanceService,
    MemberService,
    ParticipationService,
    ProjectService,
)
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


class ServerNotFound(Exception):
    """
    Indicates that the discord server wasn't found in any project
    """


class MemberNotFound(Exception):
    """
    Exception for when the user wasn't found in the members database
    """


class AttendanceCog(commands.Cog):
    """
    Class that unifies all attendance sheet code that is related to the bot

    """

    def __init__(
        self,
        bot: commands.Bot,
        member_service: MemberService,
        participation_service: ParticipationService,
        project_service: ProjectService,
    ) -> None:
        """
        Loads instance with the needed services and the bot, then starts the sheet creation task

        """
        self.bot = bot
        self.attendance_service = AttendanceService()
        self.member_service = member_service
        self.participation_service = participation_service
        self.project_service = project_service

        # pylint: disable-next=no-member
        self.is_last_day.start()

    @app_commands.command(
        name="cadastrar-presenca",
        description="cadastra uma nova presença na folha de frequência",
    )
    async def add_student_attendance(self, interaction: discord.Interaction) -> None:
        """
        Command that exibits a modal to insert and send data from a new attendance.
        Only exibits said modal if the user is allowed.
        Calls attendance_service for data validation
        """
        student = self.member_service.find_member_by_type(
            "discord_id", interaction.user.id
        )

        if student is None:
            logger.warning(
                "User %s without permission tried to add new data into attendance sheet",
                interaction.user.name,
            )
            await interaction.response.send_message(
                "Você não tem permissão para adicionar novas presenças."
            )

        else:
            logger.info("Attendance sheet user %s", interaction.user.name)
            await interaction.response.send_modal(
                AttendanceSheetForm(
                    self.attendance_service, self.member_service, self.project_service
                )
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
            student = self.member_service.find_member_by_type("member_id", student_id)
            if student is None:
                log_msg = f"Student with id {student_id}"
                log_msg += " in attendances database not inside the students database"
                logger.warning(log_msg)
                continue

            # If the user saved doesn't exist, it won't create the sheet
            user = self.bot.get_user(student.discord_id)
            if user is None:
                log_msg = f"Student with id {student_id}"
                log_msg += " in attendances database couldn't be found by discord bot"
                logger.warning(log_msg)
                continue

            files = self._create_attendance_sheet(student)
            if not files:
                log_msg = (
                    f"Student with id {student_id} had no attendance, proceeding..."
                )
                logger.info(log_msg)
                continue

            log_msg = f"Attendance sheets for the student with id {student_id}"
            log_msg += " were successfuly created. Sending..."
            logger.info(log_msg)

            first_name = student.name.split()[0]

            for file in files:
                await user.send(
                    content=f"{first_name}, aqui está a sua folha de presença em formato PDF:",
                    file=file,
                )

    def _create_attendance_sheet(self, student: Member) -> list[File]:
        """
        Get all attendances for a student, dividing them for each project and then create each
        sheet
        """
        all_participations = self.participation_service.find_participations_by_type(
            "registration", student.registration
        )
        if all_participations is None:
            return []

        all_projects_id = set()
        for participation in all_participations:
            all_projects_id.add(participation.project_id)

        first_name = student.name.split()[0]
        month_str = MONTHS[datetime.now().month - 1]

        files = []
        for project_id in all_projects_id:

            project = self.project_service.find_project_by_type(
                "project_id", project_id
            )
            if project is None:
                # Breaking line to not exceed 100 chars
                log_msg = f"The project with id {project_id}"
                log_msg += "doesn't exist but it is saved in participation"
                logger.warning(log_msg)
                continue

            proj_attends = self.attendance_service.find_attends_by_member_and_project(
                student.member_id, project_id
            )

            if not proj_attends:
                continue

            file = self.attendance_service.create_sheet(
                student_registration=student.registration,
                student_name=student.name,
                project_name=project.project_title,
                attendances=proj_attends,
            )

            # Breaking line to not exceed 100 characters
            sheet_name = "folha-de-frequencia-"
            sheet_name += f"{month_str}-{first_name}-{student.registration}"
            sheet_name += f"-{project.project_title}.pdf"

            files.append(
                File(
                    BytesIO(file),
                    filename=sheet_name,
                    spoiler=False,
                )
            )

        return files


class AttendanceSheetForm(ui.Modal):
    """
    A Class modal that represents a form for sending the needed data to create a new attendance
    """

    day_field = ui.TextInput(
        label="Dia da presença",
        placeholder="Dia do mês",
        required=False,
    )
    entry_time_field = ui.TextInput(
        label="Hora de entrada", placeholder="Formato hh:mm"
    )
    exit_time_field = ui.TextInput(label="Hora de saída", placeholder="Formato hh:mm")

    def __init__(
        self,
        attendance_service: AttendanceService,
        member_service: MemberService,
        project_service: ProjectService,
    ):
        """
        Initialize the AttendanceSheetForm instance with the needed services.
        """
        super().__init__(title="Folha de frequência")
        self.attendance_service = attendance_service
        self.member_service = member_service
        self.project_service = project_service

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        """
        Handle the submit event of the form.

        This method is called when the user submits the form.
        Sends all the data to the service to create the attendance
        """

        try:
            project = self.project_service.find_project_by_type(
                "discord_server_id", interaction.guild_id
            )
            member = self.member_service.find_member_by_type(
                "discord_id", interaction.user.id
            )

            if project is None:
                raise ServerNotFound("Este servidor não está cadastrado em um projeto")
            if member is None:
                raise MemberNotFound("O seu usuário não está cadastrado")

            self.attendance_service.create_attendance(
                day=self.day_field.value,
                entry_time=self.entry_time_field.value,
                exit_time=self.exit_time_field.value,
                user_id=member.member_id,
                proj_id=project.project_id,
            )

            log_msg = f"Success: user {interaction.user.name} created a new attendance"
            logger.info(log_msg)
            await interaction.response.send_message("Presença cadastrada com sucesso!")

        except ServerNotFound as exception:
            # Splitting string to not exceed 100 chars
            log_msg = (
                "Error during attendance creation: The server where the request was made"
                + " isn't related to any project"
            )
            logger.error(log_msg)
            await interaction.response.send_message(exception)

        except MemberNotFound as exception:
            log_msg = (
                "Error during attendance creation: The user isn't in the members database."
                + " This error should not happen as the code prevents it before"
            )
            logger.error(log_msg)
            await interaction.response.send_message(exception)

        except InvalidDate as exception:
            log_msg = (
                "Error during attendance creation: The date sent couldn't be recognized as"
                + " a valid date (in numbers, between 1 and the last day of the month)"
            )
            logger.error(log_msg)
            await interaction.response.send_message(exception)

        except InvalidTime as exception:
            log_msg = (
                "Error during attendance creation: The time sent couldn't be recognized as"
                + " a valid time (HH:MM between 00:00 and 23:59)"
            )
            logger.error(log_msg)
            await interaction.response.send_message(exception)

        except DayOutOfRange as exception:
            log_msg = (
                "Error during attendance creation: The date sent was recognized as a date"
                + " but isn't valid, since IFSP is closed (IFSP closes at sundays)"
            )
            logger.error(log_msg)
            await interaction.response.send_message(exception)

        except TimeOutOfRange as exception:
            log_msg = (
                "Error during attendance creation: The time sent was recognized as a time"
                + " but isn't valid, since IFSP is closed (see IFSP working hours)"
            )
            logger.error(log_msg)
            await interaction.response.send_message(exception)

        except EntryTimeAfterExitTime as exception:
            log_msg = (
                "Error during attendance creation: The entry time sent was after"
                + " the exit time"
            )
            logger.error(log_msg)
            await interaction.response.send_message(exception)
