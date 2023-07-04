"""
:mod: project_data
==================

Module for managing project data stored in a CSV file.

Module Dependencies:
    - ``csv``: A module for working with CSV files.
    - ``datetime``: A module for working with dates and times.

Classes:
    - :class:`ProjectData`: Class for managing project data.
"""

from dataclasses import dataclass
from datetime import date, datetime


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
    data_inicio: date
    data_fim: date


# pylint: disable=too-few-public-methods
class ProjectData:
    """
    :class: ProjectData
    ===================

    Class for managing project data stored in a CSV file.

    Module Dependencies:
        - ``csv``: A module for working with CSV files.
        - ``datetime``: A module for working with dates and times.

    Methods:
        - ``_row_to_project(row: str) -> dict``: Convert a row of project data to a dictionary.
        - ``load_projects() -> list[dict]``: Load projects from the CSV file.
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
        .. method:: load_projects() -> list[dict]

        Load projects from the CSV file.

        :return: A list of project dictionaries.
        :rtype: list[dict]
        """
        with open("assets/data/projects.csv", "r", encoding="utf-8") as file:
            projects = []
            for row in file:
                projects.append(self._row_to_project(row))
            return projects
