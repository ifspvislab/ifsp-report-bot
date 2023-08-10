"""
project_service
=======================

This module provides the classes and exceptions for managing project data.

Classes:
    - InvalidCoordinator: Exception raised when coordinator does not manage any projects.
    - EqualOrSmallerDateError: Exception raised when the end date is equal or 
    less than the start date.
    - InvalidTimeInterval: Exception raised when the time interval 
    between the end date and the start date is less than than 1 month.
    - InvalidEndDate: Exception raised when the end date is less than the current data.
    - DiscordServerIdError: Exception raised when the Discord Server ID is invalid.
    - ProjectAlreadyExists: Exception raised when the project already exists.
"""

from datetime import datetime, timedelta

import settings
from data import Project, ProjectData

from .coordinator_service import CoordinatorService

logger = settings.logging.getLogger(__name__)


class InvalidCoordinator(Exception):
    """
    Exception raised when coordinator does not manage any projects.
    """


class EqualOrSmallerDateError(Exception):
    """
    Exception raised when the end date is equal to or earlier than the start date.
    """


class InvalidTimeInterval(Exception):
    """
    Exception raised when the time interval
    between the end date and the start date is less than 1 month.
    """


class InvalidEndDate(Exception):
    """
    Exception raised when the end date is earlier than the current date.
    """


class DiscordServerIdError(Exception):
    """
    Exception raised when the Discord Server ID is invalid.
    """


class ProjectAlreadyExists(Exception):
    """
    Exception raised when the project already exists.
    """


class ProjectService:
    """
    A service for managing projects.
    """

    def __init__(
        self,
        project_data: ProjectData,
        coordinator_service: CoordinatorService,
    ):
        """
        Initializes the ProjectService instance.

        Args:
            project_data (ProjectData): The project data object for managing project data.
        """
        self.project_data = project_data
        self.coordinator_service = coordinator_service

        self.database = self.project_data.load_projects()
        self.coordinators = self.coordinator_service.database

    def find_project_by_type(self, attr_type, value):
        """
        Finds a project by the specified attribute type and value.

        Args:
            attr_type (str): The attribute type to search for.
            value: The value to match with the attribute.

        Returns:
            Project or None: The matching project or None if not found.
        """
        for project in self.database:
            if getattr(project, attr_type) == value:
                return project

        return None

    def verify_coordinator(self, registration_coordinator_id):
        """
        Verifies if the coordinator exists.

        Args:
            registration_coordinator_id (str): The coordinator to verify.

        Raises:
            InvalidCoordinator: If the coordinator does not manage any projects.
        """
        coordinator = self.coordinator_service.find_coordinator_by_type(
            "registration", registration_coordinator_id
        )

        if coordinator is None:
            raise InvalidCoordinator("O coordenador não está cadastrado no bot!")

        return coordinator.coord_id

    def verify_date(self, start_date, end_date):
        """
        Verifies if the end date is greater than the start date.

        Args:
            data_inicio (date): The start date.
            data_fim (date): The end date.

        Raises:
            EqualOrSmallerDateError: If the end date is equal to or earlier than the start date.
        """
        if (
            datetime.strptime(start_date, "%d/%m/%Y").date()
            >= datetime.strptime(end_date, "%d/%m/%Y").date()
        ):
            raise EqualOrSmallerDateError(
                "A data de fim é menor ou igual a data de início!"
            )

    def verify_date_range(self, start_date, end_date):
        """
        Verifies if the time interval between the start and end dates is greater than 1 month.

        Args:
            data_inicio (date): The start date.
            data_fim (date): The end date.

        Raises:
            InvalidTimeInterval: If the time interval
            between the start and end dates is less than 1 month.
        """
        difference = (
            datetime.strptime(end_date, "%d/%m/%Y").date()
            - datetime.strptime(start_date, "%d/%m/%Y").date()
        )
        if difference < timedelta(days=30):
            raise InvalidTimeInterval(
                "O intervalo de tempo entre a data de início e a data de fim é menor que 1 mês!"
            )

    def verify_current_date(self, end_date):
        """
        Verifies if the end date is greater than the current date.

        Args:
            data_fim (date): The end date.
            data_atual (date): The current date.

        Raises:
            InvalidEndDate: If the end date is earlier than the current date.
        """
        current_date = datetime.now().date()
        if datetime.strptime(end_date, "%d/%m/%Y").date() < current_date:
            raise InvalidEndDate("A data de fim é menor que a data atual!")

    def verify_discord_server_id(self, value):
        """
        Verifies if the Discord Server ID is valid (numeric).

        Args:
            value: The Discord Server ID.

        Raises:
            DiscordServerIdError: If the Discord Server ID is invalid.
        """
        if not value.isnumeric():
            raise DiscordServerIdError("Discord Server ID inválido.")

    def verify_project(self, project_title, start_date, end_date):
        """
        Verifies if a project with the same title and dates already exists.

        Args:
            title (str): The title of the project.
            data_inicio (date): The start date of the project.
            data_fim (date): The end date of the project.

        Raises:
            ProjectAlreadyExists: If a project with the same title and dates already exists.
        """
        for project in self.project_data.load_projects():
            if (
                project_title == project.project_title
                and datetime.strptime(start_date, "%d/%m/%Y").date()
                == project.start_date
                and datetime.strptime(end_date, "%d/%m/%Y").date() == project.end_date
            ):
                raise ProjectAlreadyExists("Esse projeto já existe!")

    def create(self, projeto: Project):
        """
        Creates a new project.

        Args:
            projeto (Project): The project object to be created.

        Raises:
            EqualOrSmallerDateError: If the end date is equal to or earlier than the start date.
            InvalidCoordinator: If the coordinator does not manage any projects.
            InvalidTimeInterval: If the time interval
            between the start and end dates is less than 1 month.
            InvalidEndDate: If the end date is earlier than the current date.
            DiscordServerIdError: If the Discord Server ID is invalid.
            ProjectAlreadyExists: If a project with the same title and dates already exists.
        """

        self.verify_date(projeto.start_date, projeto.end_date)
        self.verify_date_range(projeto.start_date, projeto.end_date)
        self.verify_current_date(projeto.end_date)
        self.verify_discord_server_id(projeto.discord_server_id)
        self.verify_project(projeto.project_title, projeto.start_date, projeto.end_date)
        project = Project(
            projeto.project_id,
            projeto.coordinator_id,
            int(projeto.discord_server_id),
            projeto.project_title,
            projeto.start_date,
            projeto.end_date,
        )
        self.project_data.add_project(project)
        self.database.append(project)
