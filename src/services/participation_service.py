"""
=====================
Participation Service
=====================

This package provides services for managing participation data. 
"""
from datetime import datetime

from data import MemberData, Participation, ParticipationData

from .member_service import MemberService
from .project_service import ProjectService
from .validation import verify_member, verify_registration


class ParticipationAlreadyExists(Exception):
    """
    Exception raised when the participation inputed already exists.
    """


class DateError(Exception):
    """
    Exception raised when an invalid date is encountered.
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

        self.database = self.participation_data.load_participations()
        self.members = self.member_data.load_members()

        self.member_service = member_service
        self.project_service = project_service

    def find_participations_by_type(
        self, attr_type, value
    ) -> list[Participation] | None:
        """
        a
        """
        for participation in self.database:
            if getattr(participation, attr_type) == value:
                return list[Participation]

        return None

    def check_ocurrence(self, value, value_):
        """
        a
        """
        project = self.project_service.find_project_by_type("titulo", value)
        member = self.member_service.find_member_by_type("registration", value_)
        for participation in self.database:
            if (
                participation.project == project.titulo
                and participation.prontuario == member.registration
            ):
                raise ParticipationAlreadyExists("Essa participação já existe!")

    def verify_date(self, value, value_):
        """
        Verifies if the date is valid.

        Args:
            value(date): The date to be verified.
            value_(str): A project title, to search in the registers.

        Raises:
            DateError: If the date is invalid.
        """

        project = self.project_service.find_project_by_type("titulo", value_)
        if not datetime.strptime(value, "%d/%m/%Y") > project.data_inicio:
            raise DateError(
                "A data inserida é inválida! Ela fica antes do início do projeto."
            )
        if not datetime.strptime(value, "%d/%m/%Y") < project.data_fim:
            raise DateError(
                "A data inserida é inválida! Ela fica após o fim do projeto."
            )

    def create(self, participation: Participation):
        """
        a
        """
        verify_registration(participation.prontuario)
        verify_member(participation.prontuario, self.members)
        self.verify_date(participation.data_inicio, participation.project)
        self.check_ocurrence(participation.project, participation.prontuario)

        self.participation_data.add_participation(participation)
        self.database.append(participation)
