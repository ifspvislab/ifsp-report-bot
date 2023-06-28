"""
Members data
"""

from dataclasses import dataclass


@dataclass
class Student:
    """
    Dataclass containing the student data.
    """

    uuid: str
    name: str
    registration: str
    discord_id: str
    email: str


class StudentData:
    """
    Class for managing student data.
    """

    def __init__(self) -> None:
        pass

    def _row_to_student(self, row: str) -> Student:
        """
        Convert a row of student data to a dictionary.

        :param row: The row of student data.
        :type row: str
        :return: A dictionary representing the student.
        :rtype: dict
        """
        fields = [field.strip() for field in row.split(sep=",")]
        data = Student
        data.id = fields[0]
        data.name = fields[1]
        data.registration = fields[2]
        data.name: fields[3]
        data.project_id: fields[4]
        return Student

    def load_students(self) -> list[Student]:
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

    def student_registration_to_name(self, registration: str):
        """
        Get the student first name with his registration.

        :param title: Student registration that will be searched.
        :type title: str
        :return: The student first name.
        :rtype: str
        """
        students = self.load_students()
        for student in students:
            if registration == student.registration:
                student_name = student.name.split[0]
            break
        return student_name
