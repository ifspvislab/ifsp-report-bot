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

from datetime import datetime


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
        .. method:: _row_to_project(row: str) -> dict

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

    def load_projects(self) -> list[dict]:
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
