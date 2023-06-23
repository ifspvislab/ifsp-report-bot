"""
This module provides a class for managing project data.

Classes:
    ProjectData: A class for managing project data.

"""
from datetime import datetime


class ProjectData:
    """
    A class for managing project data.

    Methods:
        _row_to_project(row: str) -> dict:
            Convert a row of project data to a dictionary.

        _load_projects() -> list[dict]:
            Load projects from the CSV file.
    """

    def _row_to_project(self, row: str) -> dict:
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
            "title": fields[1],
            "professor": fields[2],
            "start_date": datetime.strptime(fields[3], "%d/%m/%Y").date(),
            "end_date": datetime.strptime(fields[4], "%d/%m/%Y").date(),
        }

    def _load_projects(self) -> list[dict]:
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
