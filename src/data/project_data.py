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
    Represents a Project.

    Attributes:
        project_id (str): The project ID.
        coordinator (str): The coordinator of the project.
        discord_server_id (int): The Discord server ID associated with the project.
        title (str): The title of the project.
        start_date (int): The start date of the project.
        end_date (int): The end date of the project.
    """

    project_id: str
    coordenador: str
    discord_server_id: int
    titulo: str
    data_inicio: int
    data_fim: int


class ProjectData:
    """
    A class for managing project data.

    Methods:
        _row_to_project(row: str) -> dict:
            Convert a row of project data to a dictionary.

        _load_projects() -> list[Project]:
            Load projects from the CSV file and return a list of Project instances.

        row_to_project(row: str) -> dict:
            Convert a row of project data to a dictionary.

        load_projects() -> list[dict]:
            Load projects from the CSV file and return a list of dictionaries.
    """

    def _row_to_project(self, row: str) -> dict:
        """
        Convert a row of project data to a dictionary.

        :param row: The row of project data.
        :type row: str
        :return: A dictionary:coordenador, discord_server_id, titulo, data_inicio and data_fim.
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

    def _load_projects(self) -> list[Project]:
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

    def row_to_project(self, row: str) -> dict:
        """
        Convert a row of project data to a dictionary.

        :param row: The row of project data.
        :type row: str
        :return: A dictionary representing the project.
        :rtype: dict
        """
        fields = [field.strip() for field in row.split(sep=",")]
        return {
            "id": fields[0],
            "professor": fields[1],
            "discord_server_id": fields[2],
            "title": fields[3],
            "start_date": datetime.strptime(fields[4], "%d/%m/%Y").date(),
            "end_date": datetime.strptime(fields[5], "%d/%m/%Y").date(),
            # "id": fields[0],
            # "title": fields[1],
            # "professor": fields[2],
            # "start_date": datetime.strptime(fields[3], "%d/%m/%Y").date(),
            # "end_date": datetime.strptime(fields[4], "%d/%m/%Y").date(),
        }

    def load_projects(self) -> list[dict]:
        """
        Load projects from the CSV file.

        :return: A list of project dictionaries.
        :rtype: list[dict]
        """
        with open("assets/data/projects.csv", "r", encoding="utf-8") as file:
            projects = []
            for row in file:
                projects.append(self.row_to_project(row))
            return projects


# """
# This module provides a class for managing project data.

# Classes:
#     ProjectData: A class for managing project data.

# """
# from datetime import datetime


# class ProjectData:
#     """
#     A class for managing project data.

#     Methods:
#         _row_to_project(row: str) -> dict:
#             Convert a row of project data to a dictionary.

#         _load_projects() -> list[dict]:
#             Load projects from the CSV file.
#     """

#     def row_to_project(self, row: str) -> dict:
#         """
#         Convert a row of project data to a dictionary.

#         :param row: The row of project data.
#         :type row: str
#         :return: A dictionary representing the project.
#         :rtype: dict
#         """
#         fields = [field.strip() for field in row.split(sep=",")]
#         return {
#             "id": fields[0],
#             "title": fields[1],
#             "professor": fields[2],
#             "start_date": datetime.strptime(fields[3], "%d/%m/%Y").date(),
#             "end_date": datetime.strptime(fields[4], "%d/%m/%Y").date(),
#         }

#     def load_projects(self) -> list[dict]:
#         """
#         Load projects from the CSV file.

#         :return: A list of project dictionaries.
#         :rtype: list[dict]
#         """
#         with open("assets/data/projects.csv", "r", encoding="utf-8") as file:
#             projects = []
#             for row in file:
#                 projects.append(self.row_to_project(row))
#             return projects
