"""
data
====

This module provides functions for loading and processing data from CSV files.

Functions:
    - _row_to_project(row: str) -> dict: Convert a row of project data to a dictionary.
    - _row_to_student(row: str) -> dict: Convert a row of student data to a dictionary.
    - _load_projects() -> list[dict]: Load projects from the CSV file.
    - _load_students() -> list[dict]: Load students from the CSV file.
    - load_students() -> list[dict]: Load students and associate them with their projects.
    
"""

from datetime import datetime


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


def _row_to_coordinator(row: str) -> dict:
    """
    Convert a row of member data to a dictionary.

    :param row: The row of member data.
    :type row: str
    :return: A dictionary representing the member.
    :rtype: dict
    """
    fields = [field.strip() for field in row.split(sep=",")]
    return {
        "prontuario": fields[0],
        "discord_id": int(fields[1]),
        "name": fields[2],
        "email": fields[3],
    }


def load_coordinators() -> list[dict]:
    """
    Load members from the CSV file.

    :return: A list of member dictionaries.
    :rtype: list[dict]
    """
    with open("assets/data/coordinators.csv", "r", encoding="utf-8") as file:
        coordinators = []
        for row in file:
            coordinators.append(_row_to_coordinator(row))
        return coordinators


def add_coordinator(prontuario, name, email, discord_id):
    """
    Add project member data to the CVS file

    :param prontuario: member prontuario
    :param prontuario: member name
    :param prontuario: member email
    :param prontuario: member discord_id
    """
    with open(
        "assets/data/coordinators.csv", "a", encoding="UTF-8"
    ) as coordinator_data:
        coordinator_data.write(f"{prontuario}, {discord_id}, {name}, {email}\n")
