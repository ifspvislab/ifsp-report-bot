"""
report_service
=======================

This module provides the ReportService class for
    managing interactions with the semester report.

Classes:
- ReportService: Service class for managing report data.

Exceptions:
- InvalidRequestPeriod: Custom exception class for handling requests
    made during an invalid date period.

Functions:
- invalid_request_period: Checks if the current date is within the valid request period.

"""


from datetime import datetime

from data import MemberData

# ParticipationData
from reports import SemesterReport, SemesterReportData

# from .coordinator_service import CoordinatorService
from .member_service import MemberService

# from .project_service import ProjectService


class InvalidRequestPeriod(Exception):
    """
    Custom class for handling requests made during an invalid date period.
    """


class InvalidMember(Exception):
    """
    Exception for handling a member who doesn't exist
    """


class ProjectDoesNotExist(Exception):
    """
    Exception for handling a project that doesn't exist
    """


class ParticipationDoesNotExist(Exception):
    """
    Exception for handling a participation that doesn't exist
    """


# pylint: disable=too-few-public-methods
class ReportService:
    """
    Service class for managing report data.

    This class provides methods for generating semester reports, verifying member validity,
    and checking the request period.

    Attributes:
        member_data (MemberData): An instance of the MemberData class for accessing member data.
        member_service (MemberService): An instance of the MemberService class for
        managing member interactions.

    Exceptions:
        InvalidRequestPeriod: Custom exception class for handling requests made during an
        invalid date period.
        MemberDoesNotExist: Custom exception for handling invalid member.

    Methods:
        __init__(self, member_data, member_service): Initializes the ReportService object.
        invalid_request_period(self): Checks if the current date is within the valid
        request period.
        verifiy_member_validity(self, member_discord_id): Checks if the student can

        request the semester report.
        generate_semester_report(self, project_title, project_manager, student_name,
        planned_activities, performed_activities, results):
        Creates the semester report in bytes format.
    """

    def __init__(self, member_data: MemberData, member_service: MemberService) -> None:
        """
        Initializes the ReportService class.

        Args:
            member_data (MemberData): An instance of the MemberData class for
            accessing member data.
            member_service (MemberService): An instance of the MemberService class for
            managing member interactions.
        """
        self.member_data = member_data
        self.members = self.member_data.load_members()
        self.member_service = member_service

    def invalid_request_period(self):
        """
        Checks if the current date is within the valid request period.

        Raises:
            InvalidRequestPeriod: If the current date is outside the valid request period.

        Returns:
            bool: False if the current date is within the valid request period.
        """
        current_date = datetime.now().date()
        current_month = current_date.month
        current_day = current_date.day

        if current_month == 7 and 6 <= current_day <= 31:
            return False

        if current_month == 12 and 1 <= current_day <= 10:
            return False

        error = InvalidRequestPeriod(
            "O período de submissões ocorre entre os dias 23 a 31 "
            "de julho e 01 a 10 de dezembro."
        )
        raise error

    def verifiy_member_validity(self, member_discord_id: int):
        """
        Checks if the student can request the semester report
        """
        # this is the first step to return the student's name, their project's name and
        # coordinator's name

        student = self.member_service.find_member_by_type(
            "discord_id", member_discord_id
        )

        if student is None:
            raise InvalidMember("Você não é membro!")
        return student

    # pylint: disable=too-many-arguments
    def generate_semester_report(
        self,
        project_title: str,
        project_manager: str,
        student_name: str,
        planned_activities: str,
        performed_activities: str,
        results: str,
    ) -> bytes:
        """
        Creates the semester report in bytes format
        """

        data = SemesterReportData(
            project_title=project_title,
            project_manager=project_manager,
            student_name=student_name,
            planned_activities=planned_activities,
            performed_activities=performed_activities,
            results=results,
        )

        report = SemesterReport(data)  # Create a SemesterReport object with the data

        return report.generate()
