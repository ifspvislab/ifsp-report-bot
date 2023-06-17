"""
:mod: student_data
==================

Module for managing student data stored in a CSV file.

Module Dependencies:
    - ``csv``: A module for working with CSV files.
    - ``project_data``: A module for accessing project data.

Classes:
    - :class:`StudentData`: Class for managing student data.
"""
from .project_data import ProjectData


# pylint: disable=too-few-public-methods
class StudentData:
    """
    Class for managing student data stored in a CSV file.

    Module Dependencies:
        - csv: A module for working with CSV files.
        - project_data: A module for accessing project data.

    Methods:
        - _row_to_student(row: str) -> dict: Convert a row of student data to a dictionary.
        - _load_students() -> list[dict]: Load students from the CSV file.
        - load_students() -> list[dict]: Load students and associate them
          with their respective projects.

    """

    def _row_to_student(self, row: str) -> dict:
        """
        Convert a row of student data to a dictionary.

        :param row: The row of student data.
        :type row: str
        :return: A dictionary representing the student.
        :rtype: dict
        """
        fields = [field.strip() for field in row.split(sep=",")]
        return {
            "discord_id": int(fields[0]),
            "registration": fields[1],
            "name": fields[2],
            "project_id": fields[3],
        }

    def _load_students(self) -> list[dict]:
        """
        Load students from the CSV file.

        :return: A list of student dictionaries.
        :rtype: list[dict]
        """
        with open("assets/data/students.csv", "r", encoding="utf-8") as file:
            students = []
            for row in file:
                students.append(self._row_to_student(row))
            return students

    def load_students(self) -> list[dict]:
        """
        Load students and associate them with their respective projects.

        :return: A list of student dictionaries with associated project information.
        :rtype: list[dict]
        """
        project_data = ProjectData()
        projects = project_data.load_projects()
        students = self._load_students()

        for student in students:
            for project in projects:
                if student["project_id"] == project["id"]:
                    student["project"] = project
                    break

        return students
