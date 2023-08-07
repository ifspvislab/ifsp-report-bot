""" 

This module contains the definition of the 'Project' and 'ProjectData' classes,
which are used for managing project data.

Classes:
    Project: A class that represents a Project.
    ProjectData: A class for managing project data

"""

from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Project:
    """
    A class that represents a project.

    Attributes:
        project_id (str): the project's uuid.
        coordinator_registration (str): the projects's coordinator registration.
        discord_server_id (int): the project's Discord Server ID.
        project_title (str): the project's title.
        start_date (int): the project's start date.
        end_date (int): the project's end date.
    """

    project_id: str
    coordinator_registration: str
    discord_server_id: int
    project_title: str
    start_date: date
    end_date: date


class ProjectData:
    """
    A class for managing project data.

    Methods
    -------
    _row_to_porject(row: str) -> dict
        Converts a row of data from the projects.csv file into a dictionary format.

    load_projects() -> list[dict]
        Loads project data from the projects.csv file and returns a list of dictionaries.

    add_project(project_id, coordinator, discord_server_id, title, start_date, end_date)
        Adds a new project to the projects.csv file.
    """

    def _row_to_project(self, row: str) -> dict:
        """
        Convert a row of project data to a dictionary.

        :param row: The row of project data.
        :type row: str
        :return: A dictionary representing the project's coordinator,
        discord_server_id, title, start_date and end_date.
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

    def add_project(self, project: Project) -> None:
        """
        Add project data to the CVS file

        :param coordinator: project coordinator
        :type coordinator: str
        :param discord_server_id: project discord_server_id
        :type discord_server_id: int
        :param title: project title
        :type title: str
        :param start_date: project start_date
        :type start_date: int
        :param end_date: project end_date
        :type end_date: int
        """

        with open("assets/data/projects.csv", "a", encoding="UTF-8") as project_data:
            project_data.write(
                f"{project.project_id},{project.coordinator_registration},"
                + f"{project.discord_server_id},{project.project_title},"
                + f"{project.start_date},{project.end_date}\n"
            )
