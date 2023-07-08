"""
Termination Service

Module responsible for handling termination statement generation, overwriting participations.csv

"""

import csv
from datetime import datetime

from reports import TerminationStatement, TerminationStatementData

from .coordinator_service import CoordinatorService
from .member_service import MemberService
from .participation_service import ParticipationService
from .project_service import ProjectService


class MemberNotFound(Exception):
    """
    Custom exception executed when a member is not found in
    the system's data
    """


class ProjectNotFound(Exception):
    """
    Custom exception executed when a project is not found in
    the system's data
    """


class ParticipationNotFound(Exception):
    """
    Custom exception executed when a participation is not found in
    the system's data
    """


class ParticipationNotFoundInServer(Exception):
    """
    Custom exception executed when a participation is not found in
    the server
    """


class CoordinatorNotFound(Exception):
    """
    Custom exception executed when a coordinator is not found in
    the system's data
    """


class SlashAbsence(Exception):
    """
    Custom exception executed when the user don't put slashes on
    the right positions in termination date
    """


class InvalidLiteralTerminationDate(Exception):
    """
    Custom exception executed when the user don't put numbers in the
    fields day/month/year.
    """


class InvalidMonth(Exception):
    """
    Custom exception executed when the user don't put a month between
    1 and 12.
    """


class InvalidDayForMonth(Exception):
    """
    Custom exception executed when the day inserted isn't valid
    for the month and year provided by the user.
    """


class YearOutOfRange(Exception):
    """
    Custom exception executed when the year inserted by the user is
    negative.
    """


class OutofRangeTerminationDate(Exception):
    """
    Custom exception executed when the user provides a date that isn't
    inside the project schedule or a date in the past.
    """


class TerminationStatementService:
    """
    Service class for managing termination statement data, providing methods for
    generating the termination statement, overwriting participations.csv with the
    termination date inserted by the user and verifying validations.

    Attributes:
        member_service (MemberService): An instance of MemberService for acessing
        member data.
        project_service (ProjectService): An instance of ProjectService for acessing
        project data.
        participation_service (ParticipationService): An instance of ParticipationService
        for acessing participation data.
        coordinator_service (CoordinatorService): An instance of CoordinatorService
        for acessing participation data.

    """

    def __init__(
        self,
        member_service: MemberService,
        project_service: ProjectService,
        participation_service: ParticipationService,
        coordinator_service: CoordinatorService,
    ):
        self.member_service = member_service
        self.project_service = project_service
        self.participation_service = participation_service
        self.coordinator_service = coordinator_service

    def verify_member(self, attr_type, value):
        """
        Verifies the member's database to check if the user requesting the termination
        statement is a member

        Returns:
            member if the member is found

        Raises:
            MemberNotFound if the user isn't cataloged in the system
        """
        member = self.member_service.find_member_by_type(attr_type, value)
        if member:
            return member
        raise MemberNotFound(
            "Você não tem permissão para gerar o termo de encerramento."
        )

    def verify_project(self, attr_type, value):
        """
        Verifies the project's database

        Returns:
            project if the project is found

        Raises:
            ProjectNotFound if the project isn't cataloged in the system
        """
        project = self.project_service.find_project_by_type(attr_type, value)
        if project:
            return project
        raise ProjectNotFound("Projeto não encontrado dentro do sistema.")

    def verify_participation(self, attr_type, value):
        """
        Verifies the participations's database

        Returns:
            participations if the project is found

        Raises:
            ParticipationNotFound if the project isn't cataloged in the system
        """
        participations = self.participation_service.find_participations_by_type(
            attr_type, value
        )
        if participations:
            return participations
        raise ParticipationNotFound(
            "Participação em projeto não encontrada no sistema."
        )

    def verify_if_member_in_participation(self, project_id, participations):
        """
        Verifies if project id matches with the participation's project id

        Returns:
            true if an association between project id and participation's project id
            is found

        Raises:
            ParticipationtNotFoundInServer if the participation's project id isn't related
            to project id
        """
        member_in_participation = any(
            project_id == p.project_id for p in participations
        )
        if not member_in_participation:
            raise ParticipationNotFoundInServer(
                "Você não participa do projeto do server."
            )

    def verify_coordinator(self, attr_type, value):
        """
        Verifies the coordinator's database

        Returns:
            coordinator if the coordinator is found

        Raises:
            CoordinatorNotFound if the coordinator isn't cataloged in the system
        """
        coordinator = self.coordinator_service.find_coordinator_by_type(
            attr_type, value
        )
        if coordinator:
            return coordinator
        raise CoordinatorNotFound("Coordenador do projeto não encontrado no sistema.")

    def verify_termination_date_slashes(self, termination_date):
        """
        Verify if there are slashes on the right positions in the termination date
        provided by the user.

        Args:
            termination_date (str): The date inserted by the user

        Raises:
            SlashAbsence when the slashes aren't in the correct position.
        """

        if termination_date[2] != "/" or termination_date[5] != "/":
            raise SlashAbsence(
                "Coloque as barras da data, conforme no modelo dd/mm/aaaa"
            )

    def verify_termination_date_format_error(self, termination_date):
        """
        Verify what error on the format of the termination date
        occured.

        Args:
            termination_date (str): The date containing the error

        Returns:
            error if the error is detected
            None if the error is not detected

        """
        error = None

        if "invalid literal" in termination_date:
            error = "Coloque um número inteiro nos campos **dia**/**mês**/**ano**!"

        elif "1..12" in termination_date:
            error = "Coloque um mês de 01 a 12."

        elif "day" in termination_date:
            error = "Coloque um dia válido para o mês inserido."

        elif "year" in termination_date:
            error = "Insira um ano positivo."

        return error

    def verify_termination_date_period(
        self, project_start_date, project_end_date, termination_date
    ):
        """
        Verify if the period of the termination date is within
        the project execution period or if it is a future date or
        today.

        Args:
            project_start_date (date): The start date of the project
            project_end_date (date): The end date of the project
            termination_date (date): The termination date inserted by the member
        Raises:
            OutofRangeTerminationDate when the date isn't in the project schedule or
            a date that already passed.

        """

        termination_date = termination_date.split(sep="/")

        termination_date = datetime(
            int(termination_date[2]),
            int(termination_date[1]),
            int(termination_date[0]),
        ).date()

        days_difference = project_end_date - project_start_date

        input_days_difference = project_end_date - termination_date

        current_time = datetime.now().date()

        if input_days_difference >= days_difference or input_days_difference.days <= 0:
            raise OutofRangeTerminationDate(
                "Insira uma data dentro do período de execução do projeto!"
            )

        if current_time > termination_date:
            raise OutofRangeTerminationDate(
                "Insira a data de hoje ou uma data futura dentro do período de execução do projeto!"
            )

    def write_termination_date_in_participations(
        self, participations, guild_project_id, termination_date
    ):
        """
        Writes the termination date inserted by a member on
        participations.csv, overwriting the termination date associated
        with the member's participation

        Args:
            projects_id: The projects IDs associated with the member's
            participations.
            guild_project_id: The ID of the server where the request was
            made.
            termination_date: The termination date inserted by the member
        """
        projects_id = []
        for participation in participations:
            projects_id.append(participation.project_id)

        participation_project_id = str()
        for project_id in projects_id:
            if project_id == guild_project_id:
                participation_project_id = project_id
        i = 0
        line = 0

        with open("assets/data/participations.csv", "r", encoding="UTF-8") as file:
            for row in file:
                if participation_project_id in row:
                    modified_lines = []
                    line = i
                    with open(
                        "assets/data/participations.csv",
                        "r",
                        encoding="UTF-8",
                    ) as file:
                        reader = csv.reader(file)
                        for row in reader:
                            modified_lines.append(row)

                    modified_lines[line][4] = termination_date

                    with open(
                        "assets/data/participations.csv",
                        "w",
                        encoding="UTF-8",
                        newline="",
                    ) as file:
                        writer = csv.writer(file)
                        writer.writerows(modified_lines)
                    break
                i += 1

    # pylint: disable=too-many-arguments
    def generate_document(
        self, member, project, coordinator, termination_date, termination_reason
    ):
        """
        Generates the termination statement in bytes format.

        Args:
            member (Member): The member utilized in the TerminationStatementData,
            fulfilling the student name and student registration fields.
            project (Project): The project utilized in the TerminationStatementData,
            fulfilling the project name field.
            coordinator (Coordinator): The coordinator utilized in the
            TerminationStatementData, fulfilling the project manager field.
            termination_date (str): The termination date provided by the user.
            termination_reason (str): The termination reason provided by the user.

        Returns
            bytes: The termination statement in bytes format produced by the method
            generate() of TerminationStatement
        """

        data = TerminationStatementData(
            student_name=member.name,
            student_code=member.registration,
            project_name=project.project_title,
            project_manager=coordinator.name,
            termination_date=termination_date,
            termination_reason=termination_reason,
        )

        termination_statement = TerminationStatement(data)

        return termination_statement.generate()
