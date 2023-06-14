"""
data
====

This module provides functions for loading and processing data from CSV files.

Functions:
    - _row_to_project(row: str) -> dict: Convert a row of project data to a dictionary.
    - _row_to_student(row: str) -> dict: Convert a row of student data to a dictionary.
    - _row_to_professor(row: str) -> dict: Convert a row of professor data to a dictionary.
    - _row_to_participation(row: str) -> dict: Convert a row of participation data to a dictionary.
    - _load_projects() -> list[dict]: Load projects from the CSV file.
    - _load_students() -> list[dict]: Load students from the CSV file.
    - _load_professors() -> list[dict]: Load professors from the CSV file.
    - _load_participations() -> list[dict]: Load participations from the CSV file.
    - load_students() -> list[dict]: Load students and associate them with their projects.
    - add_participation(
    chosen_project, chosen_member, pday, pmonth, pyear
    ): Add participations to the CSV file.
    
"""

from datetime import datetime
from uuid import uuid4


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


def _row_to_professor(row: str) -> dict:
    fields = [field.strip() for field in row.split(sep=",")]
    return {"discord_id": int(fields[0]), "professor_name": fields[1]}


def row_to_participation(row: str) -> list[dict]:
    """
    Converts the participation data into a dictionary.
    """
    fields = [field.strip() for field in row.split(sep=",")]
    return {
        "registration": fields[0],
        "project": fields[1],
        "project_id": fields[2],
        "start_date": fields[3],
        "uuid": fields[4],
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


def _load_professors():
    with open("assets/data/professors.csv", "r", encoding="utf-8") as file:
        professors = []
        for row in file:
            professors.append(_row_to_professor(row))
        return professors


def _load_participations():
    with open("assets/data/participations.csv", "r", "utf-8") as file:
        participations = []
        for row in file:
            participations.append(row_to_participation(row))
        return participations


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


def add_participation(p_project, member, day, month, year):
    """
    Add participation to the CSV file.

    :param chosen_project: project the student is currently in
    :param chosen_member: student to be registered
    :param pday, pmonth, pyear: date that the student started at the project"""

    start_date = datetime.date(year, month, day)
    start_date = datetime.strftime("%d/%m/%y")
    student = str(member)
    _project = str(p_project)

    projects = _load_projects()
    for project in projects:
        if p_project == project["title"]:
            p_id = project["id"]
            break

    uuid = uuid4()

    with open("assets/data/participations.csv", "a", "utf-8") as participation_data:
        participation_data.write(f"{student},{_project},{p_id},{start_date},{uuid}\n")
