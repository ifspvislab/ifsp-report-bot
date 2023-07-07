"""
report_service
=======================

This module provides the ReportService class for managing interactions with 
the semester report.

Classes:
- ReportService: Service class for managing report data.

Exceptions:
- InvalidRequestPeriod: Custom exception for handling requests made during 
    an invalid date period.
- InvalidMember: Custom exception for handling a member who doesn't exist.
- ProjectDoesNotExist: Custom exception for handling a project that doesn't exist.
- ParticipationDoesNotExist: Custom exception for handling a participation that doesn't exist.
- ParticipationDoesNotExisInServer: Custom exception for when a student participates 
    in a project but is in the wrong project server.
- CoordinatorDoesNotExist: Custom exception for when a coordinator does not exist.

Methods:
- invalid_request_period: Checks if the current date is within the valid request period.
- verifiy_member_validity: Checks if the student can request the semester report.
- generate_semester_report: Creates the semester report in bytes format.
"""


from datetime import datetime

from data import CoordinatorData, MemberData, ParticipationData, ProjectData

# ParticipationData
from reports import SemesterReport, SemesterReportData

from .coordinator_service import CoordinatorService
from .member_service import MemberService
from .participation_service import ParticipationService
from .project_service import ProjectService

# from .project_service import ProjectService


class InvalidRequestPeriod(Exception):
    """
    Custom exception for handling requests made during an invalid date period.
    """


class InvalidMember(Exception):
    """
    Custom exception for handling an invalid member requesting the semester report.
    """


class ProjectDoesNotExist(Exception):
    """
    Custom exception for handling a project that does not exist.
    """


class ParticipationDoesNotExist(Exception):
    """
    Custom exception for handling when a member doesn't participate of any projects.
    """


class ParticipationDoesNotExisInServer(Exception):
    """
    Custom exception for handling when a student participates of a project, but
    is in the wrong project server.
    """


class CoordinatorDoesNotExist(Exception):
    """
    Handles the exception of when a coordinator does not exist.
    """


# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
class ReportService:
    """
    Service class for managing report data.

    This class provides methods for generating semester reports, verifying member validity,
    and checking the request period.

    Attributes:
        member_data (MemberData):
        An instance of the MemberData class for accessing member data.
        member_service (MemberService):
        An instance of the MemberService class for managing member interactions.
        participation_data (ParticipationData):
        An instance of the ParticipationData class for accessing participation data.
        participation_service (ParticipationService):
        An instance of the ParticipationService class for managing participation interactions.
        project_service (ProjectService):
        An instance of the ProjectService class for managing project interactions.
        project_data (ProjectData):
        An instance of the ProjectData class for accessing project data.
        coordinator_service (CoordinatorService):
        An instance of the CoordinatorService class for managing coordinator interactions.
        coordinator_data (CoordinatorData):
        An instance of the CoordinatorData class for accessing coordinator data.

        Methods:
        __init__(self, member_data, member_service, participation_data,
        participation_service, project_service, project_data, coordinator_service,
        coordinator_data): Initializes the ReportService object.
        invalid_request_period(self):
        Checks if the current date is within the valid request period.
        verifiy_member_validity(self, member_discord_id, student_registration,
        project_server_id, project_id, coordinator_id):
        Checks if the student can request the semester report.
        generate_semester_report(self, project_title, project_manager, student_name,
        planned_activities, performed_activities, results):
        Generates the semester report in bytes format.
    """

    # pylint: disable=too-many-arguments

    def __init__(
        self,
        member_data: MemberData,
        member_service: MemberService,
        participation_data: ParticipationData,
        participation_service: ParticipationService,
        project_service: ProjectService,
        project_data: ProjectData,
        coordinator_service: CoordinatorService,
        coordinator_data: CoordinatorData,
    ) -> None:
        """
        Initializes the ReportService class.

        Args:
            member_data (MemberData):
            An instance of the MemberData class for accessing member data.
            member_service (MemberService):
            An instance of the MemberService class for managing member interactions.
            participation_data (ParticipationData):
            An instance of the ParticipationData class for accessing participation data.
            participation_service (ParticipationService):
            An instance of the ParticipationService class for managing participation interactions.
            project_service (ProjectService):
            An instance of the ProjectService class for managing project interactions.
            project_data (ProjectData):
            An instance of the ProjectData class for accessing project data.
            coordinator_service (CoordinatorService):
            An instance of the CoordinatorService class for managing coordinator interactions.
            coordinator_data (CoordinatorData):
            An instance of the CoordinatorData class for accessing coordinator data.
        """
        self.member_data = member_data
        self.participation_data = participation_data
        self.project_data = project_data
        self.coordinator_data = coordinator_data

        self.database = self.participation_data.load_participations()
        self.members = self.member_data.load_members()
        self.projects = self.project_data.load_projects()
        self.coordinators = self.coordinator_data.load_coordinators()

        self.member_service = member_service
        self.project_service = project_service
        self.participation_service = participation_service
        self.coordinator_service = coordinator_service

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
        july_day_range = range(6, 32)
        december_day_range = range(1, 11)

        if not (
            (current_month == 7 and current_day in july_day_range)
            or (current_month == 12 and current_day in december_day_range)
        ):
            raise InvalidRequestPeriod(
                "O período de submissões ocorre entre os dias 23 a 31 de julho e"
                " 1 a 10 de dezembro."
            )

    # pylint: disable=too-many-arguments
    def verifiy_member_validity(
        self,
        member_discord_id: int,
        student_registration: str,
        project_server_id: int,
        project_id: str,
        coordinator_id: str,
    ):
        """
        Checks if the student can request the semester report.

        Args:
            member_discord_id (int): The Discord ID of the student.
            student_registration (str): The registration number of the student.
            project_server_id (int): The Discord server ID of the project.
            project_id (str): The ID of the project.
            coordinator_id (str): The ID of the coordinator.

        Raises:
            CoordinatorDoesNotExist:
            If the coordinator of the project does not exist.
            ParticipationDoesNotExist:
            If the student does not participate in any project.
            ParticipationDoesNotExisInServer:
            If the student does not participate in the project registered in the channel.

        Returns:
            tuple: A tuple containing the coordinator's name, project's title,
            and student's name.
        """

        student = self.member_service.find_member_by_type(
            "discord_id", member_discord_id
        )

        project = self.project_service.find_project_by_type(
            "discord_server_id", project_server_id
        )

        coordinator = self.coordinator_service.find_coordinator_by_type(
            "coord_id", coordinator_id
        )

        if coordinator is None:
            raise CoordinatorDoesNotExist(
                "O coordenador deste projeto não está cadastrado no database!"
            )

        participations = self.participation_service.find_participations_by_type(
            "registration", student_registration
        )

        if participations is None:
            raise ParticipationDoesNotExist(
                "Você não participa de nenhum projeto de ensino atualmente!"
            )

        participation_exists_in_server = any(
            p.project_id == project_id for p in participations
        )

        if not participation_exists_in_server:
            raise ParticipationDoesNotExisInServer(
                "Você não participa do projeto cadastrado neste canal!"
                " Verifique se você está no canal correto e tente novamente."
            )

        return (
            coordinator.name,
            project.project_title,
            student.name,
        )

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
        Generates the semester report in bytes format.

        Args:
            project_title (str): The title of the project.
            project_manager (str): The name of the project manager.
            student_name (str): The name of the student.
            planned_activities (str): The planned activities of the semester.
            performed_activities (str): The performed activities of the semester.
            results (str): The results of the performed activites.

        Returns:
            bytes: The semester report in bytes format.
        """

        data = SemesterReportData(
            project_title=project_title,
            project_manager=project_manager,
            student_name=student_name,
            planned_activities=planned_activities,
            performed_activities=performed_activities,
            results=results,
        )

        report = SemesterReport(data)

        return report.generate()
