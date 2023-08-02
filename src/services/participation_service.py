"""
=====================
Participation Service
=====================

This package provides services for managing participation data. 
"""

from data import MemberData, Participation, ParticipationData

from .member_service import MemberService
from .project_service import ProjectService
from .validation import verify_registration_format


class ParticipationAlreadyExists(Exception):
    """
    Exception raised when the participation inputed already exists.
    """


class OpenParticipation(Exception):
    """
    Exception raised when the participation inputed conflicts with a participation already existing.
    """


class DateError(Exception):
    """
    Exception raised when an invalid date is encountered.
    """


class MemberError(Exception):
    """
    Exception raised when an member isn't encountered.
    """


class ParticipationService:
    """
    Class for managing participation data.

    Args:
        participation_data (ParticipationData): An instance of ParticipationData class for
    accessing participation data.
        member_data (MemberData): An instance of MemberData class for accessing member data.
        project_service (ProjectService): An instance of ProjectService for acessing project data.
        member_service (MemberService): An instance of MemberService for acessing member data.
    Attributes:
        participation_data (ParticipationData): An instance of ParticipationData class for
    accessing participation data.
        member_data (MemberData): An instance of MemberData class for accessing member data.
        project_service (ProjectService): An instance of ProjectService for acessing project data.
        member_service (MemberService): An instance of MemberService for acessing member data.
    """

    def __init__(
        self,
        participation_data: ParticipationData,
        member_data: MemberData,
        project_service: ProjectService,
        member_service: MemberService,
    ) -> None:
        """ """
        self.member_data = member_data
        self.participation_data = participation_data

        self.member_service = member_service
        self.project_service = project_service

        self.database = self.participation_data.load_participations()
        self.members = self.member_service.database

    def find_participations_by_type(
        self, attr_type, value
    ) -> list[Participation] | None:
        """
        Find all the participations in the database based on the specified attribute type and value.

        Args:
            attr_type (str): The attribute type to be checked.
            value: The value of the attribute to be matched.

        Returns:
            A participations list if found, None otherwise.
        """
        participations = []
        for participation in self.database:
            if getattr(participation, attr_type) == value:
                participations.append(participation)
        if participations:
            return participations
        return None

    def check_ocurrence(self, project_id, registration, initial_date):
        """
        Check if a participation with the given registration in the given project is open.

        :param value: The project to check for existence.
        :param second_value: The registation to check for existence.
        :param third_value: The entry date to check if the participation is open.
        :raises ParticipationAlreadyExists: If a participation with the given prontuario
        and project already exists.
        """
        project = self.project_service.find_project_by_type("project_id", project_id)
        member = self.member_service.find_member_by_type("registration", registration)
        for participation in self.database:
            if (
                participation.project_id == project.project_id
                and participation.registration == member.registration
            ):
                if initial_date < participation.final_date:
                    raise ParticipationAlreadyExists("Essa participação já existe!")

    def verify_date(self, initial_date, project_id):
        """
        Verifies if the date is valid.

        Args:
            value(date): The date to be verified.
            value_(str): A project title, to search in the registers.

        Raises:
            DateError: If the date is invalid.
        """

        project = self.project_service.find_project_by_type("project_id", project_id)
        if not initial_date > project.start_date:
            raise DateError(
                "A data inserida é inválida! Ela fica antes do início do projeto."
            )
        if not initial_date < project.end_date:
            raise DateError(
                "A data inserida é inválida! Ela fica após o fim do projeto."
            )

    def verify_member_exists(self, registration):
        """
        Verify if the member exists in the registers.
        Args:
            registration(str): The registration to be verified.

        Raises:
            MemberError: If the member isn't in the registers.
        """

        for member in self.members:
            if member.registration == registration:
                return None

        raise MemberError("O membro inexiste nos registros!")

    def create(self, participation: Participation):
        """
        Add a new participation to the database.

        :param participation: The participation dataclass.
        """
        verify_registration_format(participation.registration)
        self.verify_member_exists(participation.registration)
        self.verify_date(participation.initial_date, participation.project_id)
        self.check_ocurrence(
            participation.project_id,
            participation.registration,
            participation.initial_date,
        )

        self.participation_data.add_participation(participation)
        self.database.append(participation)
