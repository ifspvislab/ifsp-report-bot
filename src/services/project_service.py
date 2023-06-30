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
from datetime import date, datetime, timedelta

from data import CoordinatorData, Project, ProjectData


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

    def __init__(self, project_data: ProjectData):
        """
        Initializes the ProjectService instance.

        Args:
            project_data (ProjectData): The project data object for managing project data.
        """
        self.project_data = project_data
        self.coordinator_data = CoordinatorData
        self.database = self.project_data.load_projects(self)

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

    def verify_coordinator(self, coordenador):
        """
        Verifies if the coordinator exists.

        Args:
            coordenador (str): The coordinator to verify.

        Raises:
            InvalidCoordinator: If the coordinator does not manage any projects.
        """
        self.coordinator_data = self.coordinator_data.load_coordinators()

        for coordinator_entry in self.coordinator_data:
            if coordenador == coordinator_entry.nome:
                return

        raise InvalidCoordinator("O coordenador não administra nenhum projeto!")

    def verify_data(self, data_inicio: date, data_fim: date):
        """
        Verifies if the end date is greater than the start date.

        Args:
            data_inicio (date): The start date.
            data_fim (date): The end date.

        Raises:
            EqualOrSmallerDateError: If the end date is equal to or earlier than the start date.
        """
        if data_inicio >= data_fim:
            raise EqualOrSmallerDateError(
                "A data de fim é menor ou igual a data de início!"
            )

    def verify_intervalo_data(self, data_inicio: date, data_fim: date):
        """
        Verifies if the time interval between the start and end dates is greater than 1 month.

        Args:
            data_inicio (date): The start date.
            data_fim (date): The end date.

        Raises:
            InvalidTimeInterval: If the time interval
            between the start and end dates is less than 1 month.
        """
        diferenca = data_fim - data_inicio
        if diferenca < timedelta(days=30):
            raise InvalidTimeInterval(
                "O intervalo de tempo entre a data de início e a data de fim é menor que 1 mês!"
            )

    def verify_data_atual(self, data_fim: date):
        """
        Verifies if the end date is greater than the current date.

        Args:
            data_fim (date): The end date.
            data_atual (date): The current date.

        Raises:
            InvalidEndDate: If the end date is earlier than the current date.
        """
        data_atual = datetime.now().date()
        if data_fim < data_atual:
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

    def verify_projeto(self, titulo, data_inicio: date, data_fim: date):
        """
        Verifies if a project with the same title and dates already exists.

        Args:
            titulo (str): The title of the project.
            data_inicio (date): The start date of the project.
            data_fim (date): The end date of the project.

        Raises:
            ProjectAlreadyExists: If a project with the same title and dates already exists.
        """
        for project in self.project_data.load_projects():
            if (
                titulo == project.titulo
                and data_inicio == project.data_inicio
                and data_fim == project.data_fim
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
        self.verify_coordinator(projeto.coordenador)
        self.verify_data(projeto.data_inicio, projeto.data_fim)
        self.verify_intervalo_data(projeto.data_inicio, projeto.data_fim)
        self.verify_data_atual(projeto.data_fim)
        self.verify_discord_server_id(projeto.discord_server_id)
        self.verify_projeto(projeto.titulo, projeto.data_inicio, projeto.data_fim)
        project = Project(
            projeto.project_id,
            projeto.coordenador,
            projeto.discord_server_id,
            projeto.titulo,
            projeto.data_inicio,
            projeto.data_fim,
        )
        self.project_data.add_project(project)
        self.database.append(project)
