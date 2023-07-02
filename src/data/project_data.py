""" 

This module contains the definition of the 'Project' and 'ProjectData' classes,
which are used for managing project data.

Classes:
    Project: A class that represents a Project.
    ProjectData: A class for managing project data

"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Project:
    """
    A class that represents a project.

    Attributes:
        project_id (str): the project's uuid.
        coordenador (str): the projects's coordinator.
        discord_server_id (int): the project's Discord Server ID.
        titulo (str): the project's title.
        data_inicio (int): the project's start date.
        data_fim (int): the project's end date.
    """

    project_id: str
    coordenador: str
    discord_server_id: int
    titulo: str
    data_inicio: int
    data_fim: int


# pylint: disable=too-few-public-methods
class ProjectData:
    """
    A class for managing project data.

    Methods
    -------
    _row_to_porject(row: str) -> dict
        Converts a row of data from the projects.csv file into a dictionary format.

    load_projects() -> list[dict]
        Loads project data from the projects.csv file and returns a list of dictionaries.
    """

    def _row_to_project(self, row: str) -> dict:
        """
        Convert a row of project data to a dictionary.

        :param row: The row of project data.
        :type row: str
        :return: A dictionary representing the project's coordenador,
        discord_server_id, titulo, data_inicio and data_fim.
        :rtype: dict
        """

        fields = [field.strip() for field in row.split(sep=",")]
        project = Project(
            fields[0],
            fields[1],
            int(fields[2]),
            fields[3],
            datetime.strptime(fields[4], "%d/%m/%Y").date(),
            datetime.strptime(fields[5], "%d/%m/%Y").date(),
        )
        return project

    def load_projects(self) -> list[Project]:
        """
        Load projects from the CSV file and return a list of dictionaries.

        :return: A list of project dictionaries, where each dictionary represents a project.
        :rtype: list[dict]
        """

        with open("assets/data/projects.csv", "r", encoding="utf-8") as file:
            projects = []
            for row in file:
                projects.append(self._row_to_project(row))
            return projects
