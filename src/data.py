"""
data
====

This module provides functions for loading and processing data from CSV files.

Classes:
    - Attendances

Functions:
    - _row_to_project(row: str) -> dict: Convert a row of project data to a dictionary.
    - _row_to_student(row: str) -> dict: Convert a row of student data to a dictionary.
    - _load_projects() -> list[dict]: Load projects from the CSV file.
    - _load_students() -> list[dict]: Load students from the CSV file.
    - load_students() -> list[dict]: Load students and associate them with their projects.
    - _strtime_to_time(strtime: str) -> time: Converts from string type to time type.
    - _row_to_attend(row: str) -> Attendance: Create a Attendance from a row string.
    - _load_attend() -> list[Attendance]: Read the saved Attendances.
    - load_attend() -> list[Attendance]: Returns all saved Attendences.
    
"""

from dataclasses import dataclass
from datetime import datetime, time


def _row_to_project(row: str) -> dict:
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


def _row_to_student(row: str) -> dict:
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


def _load_projects() -> list[dict]:
    """
    Load projects from the CSV file.

    :return: A list of project dictionaries.
    :rtype: list[dict]
    """
    with open("assets/data/projects.csv", "r", encoding="utf-8") as file:
        projects = []
        for row in file:
            projects.append(_row_to_project(row))
        return projects


def _load_students() -> list[dict]:
    """
    Load students from the CSV file.

    :return: A list of student dictionaries.
    :rtype: list[dict]
    """
    with open("assets/data/students.csv", "r", encoding="utf-8") as file:
        students = []
        for row in file:
            students.append(_row_to_student(row))
        return students


def load_students() -> list[dict]:
    """
    Load students and associate them with their respective projects.

    :return: A list of student dictionaries with associated project information.
    :rtype: list[dict]
    """
    projects = _load_projects()
    students = _load_students()

    for student in students:
        for project in projects:
            if student["project_id"] == project["id"]:
                student["project"] = project
                break

    return students


@dataclass
class Attendance:
    """
    Data Class for attendances
    """

    attendance_id: str
    student_id: int
    day: datetime
    entry_time: time
    exit_time: time


def _strtime_to_time(strtime: str) -> time:
    """
    Converts from string type to time type

    :param strtime: The string data to be converted
    :type strtime: str
    :return: A time in HH:MM format
    :rtype: time
    """
    split_time = [int(part) for part in strtime.split(":")]
    return time(hour=split_time[0], minute=split_time[1])


def _strdate_to_date(strdate: str) -> datetime:
    """
    Converts from string type to datetime type
    Dates are saved in dd/mm/yyyy format

    :param strdate: The string data to be converted
    :type strdate: str
    :return: A date
    :rtype: datetime
    """
    split_date = [int(part) for part in strdate.split("/")]
    return datetime(day=split_date[0], month=split_date[1], year=split_date[2])


def _row_to_attend(row: str) -> Attendance:
    """
    Create a new Attendance from a row of data in string type

    :param row: The row of data to be made into an Attendance
    :type row: str
    :return: A Attendance instance
    :rtype: Attendance
    """
    fields = [field.strip() for field in row.split(sep=",")]
    return Attendance(
        fields[0],
        int(fields[1]),
        _strdate_to_date(fields[2]),
        _strtime_to_time(fields[3]),
        _strtime_to_time(fields[4]),
    )


def _load_attend() -> list[Attendance]:
    """
    Read the assets/data/attendances.csv file and create a list of all saved Attendances

    :return: The list of all saved Attendences
    :rtype: list[Attendance]
    """
    with open("assets/data/attendances.csv", "r", encoding="utf-8") as file:
        attendances = []
        for row in file:
            attendances.append(_row_to_attend(row))
        return attendances


def load_attend() -> list[Attendance]:
    """
    Calls _load_attendances() and send the data to the caller.

    :return: The list of all saved Attendences
    :rtype: list[Attendance]
    """
    attendances = _load_attend()
    return attendances


def save_attend(attend: Attendance) -> bool:
    """
    Saves the data sent by the student in attendances.csv

    :returns: True if the operation was a success or False if something went wrong
    :rtype: bool
    """

    line = ""
    line += f"{attend.attendance_id}"
    line += f",{attend.student_id}"
    line += f",{attend.day.strftime('%d/%m/%Y')}"
    line += f",{attend.entry_time.strftime('%H:%M')}"
    line += f",{attend.exit_time.strftime('%H:%M')}\n"

    with open("assets/data/attendances.csv", "a", encoding="utf-8") as file:
        file.write(line)

    return True
