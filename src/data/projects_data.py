"""
Projects data
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Project:
    """
    Dataclass with the project data.
    """

    uuid: str
    project_id: str
    title: str
    professor: str
    start_date: str
    final_date: str


class ProjectData:
    """
    Class for managing projects data.
    """

    def __init__(self) -> None:
        pass

    def _row_to_project(self, row: str) -> Project:
        """
        Convert a row of project data to a dataclass.

        :param row: The row of project data.
        :type row: str
        :return: A dictionary representing the project.
        :rtype: dict
        """
        data = Project
        fields = [field.strip() for field in row.split(sep=",")]
        data.id = fields[0]
        data.project_id = fields[1]
        data.title = fields[2]
        data.professor = fields[3]
        data.start_date = datetime.strptime(fields[4], "%d/%m/%Y").date()
        data.final_date = datetime.strptime(fields[5], "%d/%m/%Y").date()
        return Project

    def load_projects(self) -> list[Project]:
        """
        Load projects from the CSV file.

        :return: A list of project dictionaries.
        :rtype: list[dict]
        """
        with open("assets/data/projects.csv", "r", encoding="utf-8") as file:
            projects = []
            for row in file:
                projects.append(self._row_to_project(row))
        return projects

    def project_name_to_id(self, title: str):
        """
        Get the project ID with the project name.

        :param title: Project title that will be searched.
        :type title: str
        :return: The project ID.
        :rtype: str
        """
        projects = self.load_projects()
        for project in projects:
            if title == project.title:
                project_id = project.project_id
            break
        return project_id

    def project_name_to_final_date(self, title: str):
        """
        Get the project final date with the project name.

        :param title: Project title that will be searched.
        :type title: str
        :return: The project final date.
        :rtype: str
        """
        projects = self.load_projects()
        for project in projects:
            if title == project.title:
                final_date = project.final_date
                break
        return final_date
