"""
Services for log command.
"""
import zoneinfo
from datetime import datetime

import settings
from data import Log, LogData, ProjectData, StudentData
from reports import LogReport, LogReportData

from .validation import verify_discord_id

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

    def __init__(self):
        self.database = []
        self.log_data = LogData()
        self.projects_data = ProjectData()
        self.students_data = StudentData()

    def check_student_in_project(self, student_id: int) -> bool:
        """
        Check if a student is part of a project.

        This function checks if a student with the provided ID is part of a project.

        :param student_id: The ID of the student to check.
        :type student_id: int
        :return: True if the student is part of a project, False otherwise.
        :rtype: bool
        """
        self.database = self.students_data.load_students()

        for student in self.database:
            if student["discord_id"] == student_id:
                return True
        return False

    def get_project_id_by_server_id(self, server_id: int) -> str:
        """
        Get the project ID associated with a server ID.

        This function retrieves the project ID associated with the provided server ID.

        :param server_id: The server ID.
        :type server_id: int
        :return: The project ID associated with the server ID, or None if not found.
        :rtype: str
        """
        self.database = self.projects_data.load_projects()

        for project in self.database:
            if project["discord_server_id"] == str(server_id):
                return project["id"]
        return None

    def datetime_format(self, date: str) -> datetime:
        """
        Format a date string to a datetime object.

        This function formats a date string to a datetime object.

        :param date: The date string to format.
        :type date: str
        :return: The formatted datetime object.
        :rtype: datetime
        """
        split_date = date.split(" ")
        if len(split_date) == 2:
            datetime.strptime(date, "%d/%m/%Y %H:%M")
        formatted_date = datetime.strptime(split_date[0], "%d/%m/%Y")

        return formatted_date

    def get_time_zone(self) -> zoneinfo.ZoneInfo:
        """
        Retrieve the time zone.

        This function retrieves the time zone.

        :return: The time zone representing 'America/Sao_Paulo'.
        :rtype: zoneinfo.ZoneInfo
        """
        return zoneinfo.ZoneInfo("America/Sao_Paulo")

    def filter_date_validation(self, date: str) -> None:
        """
        Validates the date filter based on the provided start and end dates.

        This function validates the date filter based on the provided start and end dates.

        :param date: The date to be validated.
        :type date: str
        :raises IncorrectDateFilter: If the date format is incorrect.
        :return: None
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

        This function retrieves the event date in the formatted string.

        :param datetime_obj: The datetime object representing the event date.
        :type datetime_obj: datetime, optional
        :return: The formatted event date string.
        :rtype: str
        """
        zone = self.get_time_zone()
        if datetime_obj is None:
            date = datetime.now(zone).strftime("%d/%m/%Y %H:%M")
        else:
            date = datetime_obj.astimezone(zone).strftime("%d/%m/%Y %H:%M")
        return date

    def generate_log(self, action: str, student_id: int, date: datetime = None):
        """
        Generate a log entry.

        This function generates a log entry with the provided action, student ID, and date.

        :param action: The action associated with the log entry.
        :type action: str
        :param student_id: The ID of the student associated with the log entry.
        :type student_id: int
        :param date: The date of the log entry.
        :type date: datetime, optional
        """
        if self.check_student_in_project(student_id):
            date_string = self.get_event_date(datetime_obj=date)
            log_action = f"{date_string} - {action}"
            log = Log(
                discord_id=student_id,
                date=date_string,
                action=log_action,
            )
            self.log_data.add_log(log)

    def check_size_log_report(self, report: LogReport):
        """
        Check the size of a log report.

        This function checks the size of a log report. If the size exceeds the maximum limit,
        an exception is raised.

        :param report: The log report to check.
        :type report: LogReport
        :raises InvalidReportSize: If the report size is invalid.
        :return: True if the report size is valid, False otherwise.
        :rtype: bool
        """
        if report.generate() is None or len(report.generate()) > 26214400:
            raise InvalidReportSize(
                "Arquivo muito grande para o Discord. Utilize filtros."
            )
        return True

    # pylint: disable=inconsistent-return-statements
    def generate_log_report(
        self,
        server_id: int,
        student_id: str = None,
        start_date: str = None,
        end_date: str = None,
    ) -> LogReport:
        """
        Generate a log report.

        This function generates a log report based on the provided parameters.

        :param server_id: The ID of the server associated with the logreport.
        :type server_id: int
        :param student_id: The ID of the student to filter the report by, or None for all students.
        :type student_id: str, optional
        :param start_date: The start date of the report filter, or None for no start date.
        :type start_date: str, optional
        :param end_date: The end date of the report filter, or None for no end date.
        :type end_date: str, optional
        :return: The generated log report.
        :rtype: LogReport
        :raises IdDoesNotExist: If the provided student ID does not exist.
        :raises NoStartDate: If no start date is provided when an end date is.
        """
        project_id = self.get_project_id_by_server_id(server_id)

        if student_id is not None:
            verify_discord_id(student_id)
            if not self.check_student_in_project(student_id=int(student_id)):
                raise IdDoesNotExist("ID não corresponde a nenhum estudante")

        if start_date is None and end_date is None:
            if student_id is not None:
                data = LogReportData(
                    students=self.students_data.load_students(),
                    logs=self.log_data.load_logs(),
                    project_id=project_id,
                    value=3,
                    start_date=None,
                    end_date=None,
                    student_id=str(student_id),
                )
            else:
                data = LogReportData(
                    students=self.students_data.load_students(),
                    logs=self.log_data.load_logs(),
                    project_id=project_id,
                    value=1,
                    start_date=None,
                    end_date=None,
                    student_id=None,
                )

        elif end_date is not None and start_date is None:
            raise NoStartDate("É preciso de uma data inicial")

        elif start_date is not None:
            if end_date is None:
                end_date = self.get_event_date()

            self.filter_date_validation(start_date)
            self.filter_date_validation(end_date)

            if student_id is not None:
                data = LogReportData(
                    students=self.students_data.load_students(),
                    logs=self.log_data.load_logs(),
                    project_id=project_id,
                    value=4,
                    start_date=self.datetime_format(start_date),
                    end_date=self.datetime_format(end_date),
                    student_id=str(student_id),
                )

            else:
                data = LogReportData(
                    students=self.students_data.load_students(),
                    logs=self.log_data.load_logs(),
                    project_id=project_id,
                    value=2,
                    start_date=self.datetime_format(start_date),
                    end_date=self.datetime_format(end_date),
                    student_id=None,
                )

        report = LogReport(data)

        if self.check_size_log_report(report):
            return report
