"""
Services for log command.
"""
import zoneinfo
from datetime import datetime

import settings
from data import Log, LogData, MemberData, ParticipationData
from reports import LogReport, LogReportData

from .member_service import MemberService
from .participation_service import ParticipationService
from .project_service import ProjectService

logger = settings.logging.getLogger(__name__)


class IncorrectDateFilter(Exception):
    """Exception raised for incorrect date filters."""


class NotCoordinator(Exception):
    """Exception raised when the user is not a coordinator."""


class IdDoesNotExist(Exception):
    """Exception raised when an ID does not exist."""


class NoStartDate(Exception):
    """Exception raised when there is no start date."""


class InvalidReportSize(Exception):
    """Exception raised for an invalid report size."""


class LogService:
    """
    Service class for log command.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        log_data: LogData,
        members_data: MemberData,
        participations_data: ParticipationData,
        project_service: ProjectService,
        member_service: MemberService,
        participation_service: ParticipationService,
    ):
        """
        Initialize the LogService.

        This class manages log information for a specific context,
        such as projects, members, and participations.

        Args:
            log_data (LogData): The data object for log information.
            members_data (MemberData): The data object for member information.
            participations_data (ParticipationData): The data object for participation information.
            project_service (ProjectService): The service object for project-related operations.
            member_service (MemberService): The service object for member-related operations.
            participation_service: The service object for participation operations.
        """
        self.database = []
        self.log_data = log_data
        self.members_data = members_data
        self.participations_data = participations_data
        self.project_service = project_service
        self.member_service = member_service
        self.participation_service = participation_service

    def datetime_format(self, date: str) -> datetime:
        """
        Format a date string to a datetime object.

        Args:
            date (str): The date string to format.

        Returns:
            datetime: The formatted datetime object.
        """
        split_date = date.split(" ")
        if len(split_date) == 2:
            return datetime.strptime(date, "%d/%m/%Y %H:%M")
        formatted_date = datetime.strptime(split_date[0], "%d/%m/%Y")
        return formatted_date

    def get_time_zone(self) -> zoneinfo.ZoneInfo:
        """
        Retrieve the time zone.

        Returns:
            zoneinfo.ZoneInfo: The time zone representing 'America/Sao_Paulo'.
        """
        return zoneinfo.ZoneInfo("America/Sao_Paulo")

    def filter_date_validation(self, date: str):
        """
        Validates the date filter based on the provided start and end dates.

        Args:
            date (str): The date to be validated.

        Raises:
            IncorrectDateFilter: If the date format is incorrect.
        """
        try:
            split_date = date.split(" ")
            if len(split_date) == 2:
                datetime.strptime(date, "%d/%m/%Y %H:%M")
            datetime.strptime(split_date[0], "%d/%m/%Y")
        except Exception as exc:
            raise IncorrectDateFilter("Formato de data incorreto") from exc

    def get_event_date(self, datetime_obj: datetime = None) -> str:
        """
        Get the event date in the formatted string.

        Args:
            datetime_obj (datetime, optional): The datetime object representing the event date.

        Returns:
            str: The formatted event date string.
        """
        zone = self.get_time_zone()
        if datetime_obj is None:
            date = datetime.now(zone).strftime("%d/%m/%Y %H:%M")
        else:
            date = datetime_obj.astimezone(zone).strftime("%d/%m/%Y %H:%M")
        return date

    def generate_log(
        self, action: str, student_id: int, project_id: str, date: datetime = None
    ) -> None:
        """
        Generate a log entry.

        Args:
            action (str): The action associated with the log entry.
            student_id (int): The ID of the student associated with the log entry.
            project_id (str): The ID of the project associated with the log entry.
            date (datetime, optional): The date of the log entry.
        """
        # pylint: disable=line-too-long
        try:
            member = self.member_service.find_member_by_type("discord_id", student_id)
            participation = self.participation_service.find_participations_by_type(
                "registration", member.registration
            )
            if (
                participation[0].project_id == project_id
                and participation[0] is not None
            ):
                date_string = self.get_event_date(datetime_obj=date)
                log_action = f"{date_string} - {action}"
                log = Log(
                    project_id=project_id,
                    registration=member.registration,
                    discord_id=student_id,
                    date=date_string,
                    action=log_action,
                )
                self.log_data.add_log(log)
        except AttributeError:
            return

    def check_size_log_report(self, report: LogReport) -> bool:
        """
        Check the size of a log report.

        Args:
            report (LogReport): The log report to check.

        Raises:
            InvalidReportSize: If the report size is invalid.

        Returns:
            bool: True if the report size is valid, False otherwise.
        """
        if report.generate() is None or len(report.generate()) > 26214400:
            raise InvalidReportSize(
                "Arquivo muito grande para o Discord. Utilize filtros."
            )
        return True

    def get_project_server_id(self, server_id: int) -> str | None:
        """
        Retrieves the project ID associated with the given Discord server ID.

        Args:
            server_id (int): The Discord server ID to search for.

        Returns:
            str: The associated project ID if found, otherwise an empty string.
        """
        project = self.project_service.find_project_by_type(
            "discord_server_id", server_id
        )
        if project is not None:
            return project.project_id
        return None

    # pylint: disable=inconsistent-return-statements
    def generate_log_report(
        self,
        server_id: int,
        discord_id: int = None,
        start_date: str = None,
        end_date: str = None,
    ) -> LogReport:
        """
        Generate a log report.

        Args:
            server_id (int): The ID of the server associated with the log report.
            discord_id (str): The ID of the student to filter the report, or None for all students.
            start_date (str): The start date of the report filter, or None for no start date.
            end_date (str): The end date of the report filter, or None for no end date.

        Returns:
            LogReport: The generated log report.

        Raises:
            IdDoesNotExist: If the provided student ID does not exist.
            NoStartDate: If no start date is provided when an end date is.
        """
        if discord_id is not None:
            if (
                self.member_service.find_member_by_type("discord_id", discord_id)
                is None
            ):
                raise IdDoesNotExist("ID não corresponde a nenhum estudante")

        if start_date is None and end_date is None:
            if discord_id is not None:
                data = LogReportData(
                    members=self.members_data.load_members(),
                    participations=self.participations_data.load_participations(),
                    logs=self.log_data.load_logs(),
                    project_id=self.get_project_server_id(server_id),
                    value=3,
                    start_date=None,
                    end_date=None,
                    discord_id=discord_id,
                )
            else:
                data = LogReportData(
                    members=self.members_data.load_members(),
                    participations=self.participations_data.load_participations(),
                    logs=self.log_data.load_logs(),
                    project_id=self.get_project_server_id(server_id),
                    value=1,
                    start_date=None,
                    end_date=None,
                    discord_id=None,
                )

        elif end_date is not None and start_date is None:
            raise NoStartDate("É preciso de uma data inicial")

        elif start_date is not None:
            if end_date is None:
                end_date = self.get_event_date()

            self.filter_date_validation(start_date)
            self.filter_date_validation(end_date)

            if discord_id is not None:
                data = LogReportData(
                    members=self.members_data.load_members(),
                    participations=self.participations_data.load_participations(),
                    logs=self.log_data.load_logs(),
                    project_id=self.get_project_server_id(server_id),
                    value=4,
                    start_date=self.datetime_format(start_date),
                    end_date=self.datetime_format(end_date),
                    discord_id=discord_id,
                )

            else:
                data = LogReportData(
                    members=self.members_data.load_members(),
                    participations=self.participations_data.load_participations(),
                    logs=self.log_data.load_logs(),
                    project_id=self.get_project_server_id(server_id),
                    value=2,
                    start_date=self.datetime_format(start_date),
                    end_date=self.datetime_format(end_date),
                    discord_id=None,
                )

        report = LogReport(data)

        if self.check_size_log_report(report):
            return report
