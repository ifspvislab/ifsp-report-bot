"""
project_service
=======================

This module provides the classes and exceptions for managing project data.

Classes:
    - InvalidCoordinator: Exception raised when coordinator does not exist.
    - EqualOrSmallerDateError: Exception raised when the end date is equal or less than the start date.
    - InvalidTimeInterval: Exception raised when the time interval between the end date and the start date is less than than 1 month.
    - InvalidEndDate: Exception raised when the end date is less than the current data.
    - DiscordServerIdError: Exception raised when the Discord Server ID is invalid.
    - ProjectAlreadyExists: Exception raised when the project already exists.
"""
from datetime import date, datetime, timedelta

from data import Coordinator, CoordinatorData, Project, ProjectData


class InvalidCoordinator(Exception):
    """
    Exception raised when coordinator does not exist.
    """


class EqualOrSmallerDateError(Exception):
    """
    Exception raised when the end date is equal or less than the start date.
    """


class InvalidTimeInterval(Exception):
    """
    Exception raised when the time interval between the end date and the start date is less than than 1 month.
    """


class InvalidEndDate(Exception):
    """
    Exception raised when the end date is less than the current data.
    """


class DiscordServerIdError(Exception):
    """
    Exception raised when the Discord Server ID is invalid.
    """


class ProjectAlreadyExists(Excpetion):
    """
    Exception raised when the project already exists.
    """


class ProjectService:
    """
    A service for managing projects
    """

    def __init__(self, coordinator_data: CoordinatorData, project_data: ProjectData):
        self.coordinator_data = coordinator_data
        self.project_data = project_data
        self.database = self.project_data.load_projects()

    def find_project_by_type(self, attr_type, value):
        for project in self.database:
            if getattr(project, attr_type) == value:
                return project

        return None

    def verify_coordenador(self, coordenador, nome):
        for coordinator in self.coordinator_data.load_coordinators():
            if coordenador != coordenador.nome:
                raise InvalidCoordinator(
                    "O coordenador informado não está presente em nenhum projeto."
                )

    def verify_data(self, data_inicio: date, data_fim: date):
        if data_inicio >= data_fim:
            raise EqualOrSmallerDateError(
                "A data de fim é menor ou igual a data de início!"
            )

    def verify_intervalo_data(self, data_inicio: date, data_fim: date):
        diferenca = data_fim - data_inicio
        if diferenca < timedelta(days=30):
            raise InvalidTimeInterval(
                "O intervalo entre a data de início e a data de fim é menor que 1 mês"
            )

    def verify_data_atual(self, data_fim: date, data_atual: date):
        data_atual = datetime.now()
        if data_fim < data_atual:
            raise InvalidEndDate("A data de fim é menor que a data atual")

    def verify_discord_server_id(self, value):
        if not value.isnumeric():
            raise DiscordServerIdError("Discord Server ID inválido")

    def verify_projeto(self, titulo, data_inicio: date, data_fim: date):
        for project in self.project_data.load_projects():
            if (
                titulo == project.titulo
                and data_inicio == project.data_inicio
                and data_fim == project.data_fim
            ):
                raise ProjectAlreadyExists("Esse projeto já existe!")

    def create(self, projeto: Project):
        self.verify_coordenador(projeto.coordenador, coordenador.nome)
        self.verify_data(projeto.data_inicio, projeto.data_fim)
        self.verify_intervalo_data(projeto.data_inicio, projeto.data_fim)
        self.verify_data_atual(projeto.data_inicio, projeto.data_fim)
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
