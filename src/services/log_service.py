"""
Services for log command.
"""

from datetime import datetime

import discord

import settings
from data.log_data import LogData
from data.project_data import ProjectData
from data.student_data import StudentData

zone = settings.get_time_zone()
students_data = StudentData()
students_list = students_data.load_students()
projects_data = ProjectData()
projects_list = projects_data.load_projects()


class IncorrectDateFilter(Exception):
    """Incorrect date filter"""


class LogService:
    """
    Service class for log command.
    """

    def add_logs(
        self, project_id: int, student_id: int, date: str, action: str
    ) -> None:
        """
        Adds logs to the log file.

        :param project_id: ID of the project associated with the log.
        :type project_id: int
        :param student_id: ID of the student associated with the log.
        :type student_id: int
        :param date: Date of the log entry.
        :type date: str
        :param action: Action performed for the log.
        :type action: str
        :return: None
        """

        log_list = [project_id, student_id, date, action]
        LogData.create_logs(self=LogData, data_list=log_list)

    def check_student_in_project(
        self, student_id: int, students: list[dict] = None
    ) -> bool:
        """
        Checks if the given student ID is associated with a project.

        :param student_id: The student ID to be checked.
        :type student_id: int
        :param students: The list of student dictionaries.
                        Defaults to None.
        :type students: list[dict] or None
        :return: True if the student ID is associated with a project, False otherwise.
        :rtype: bool
        """
        if students is None:
            students = students_list

        for student in students:
            if student["discord_id"] == student_id:
                return True
        return False

    def get_project_id_by_student_id(
        self, student_id: int, students: list[dict] = None
    ) -> int:
        """
        Get the project ID associated with the given student ID.

        :param student_id: The student ID.
        :type student_id: int
        :param students: The list of student dictionaries.
        :type students: list[dict]
        :return: The project ID associated with the student ID.
                 Returns None if the student is not associated with any project.
        :rtype: int or None
        """
        if students is None:
            students = students_list

        for student in students:
            if student["discord_id"] == student_id:
                if "project" in student and "id" in student["project"]:
                    return student["project"]["id"]
        return None

    def get_project_id_by_server_id(
        self, server_id: int, projects: list[dict] = None
    ) -> int:
        """
        Get the project ID associated with the given server ID.

        :param server_id: The server ID.
        :type server_id: int
        :param projects: The list of project dictionaries.
        :type projects: list[dict]
        :return: The project ID associated with the server ID.
                 Returns None if no project is associated with the server.
        :rtype: int or None
        """
        if projects is None:
            projects = projects_list

        for project in projects:
            if project["discord_server_id"] == str(server_id):
                return project["id"]
        return None

    def date_validation(self, date: str, start_date: str, end_date: str) -> bool:
        """
        Validates a date within a specified range.

        :param date: Date to be validated.
        :type date: str
        :param start_date: Start date of the range.
        :type start_date: str
        :param end_date: End date of the range.
        :type end_date: str
        :return: True if the date is within the range, False otherwise.
        :rtype: bool
        """

        split_date = date.split(" ")
        correct_date = datetime.strptime(split_date[0], "%d/%m/%Y")

        formatted_start_date = datetime.strptime(start_date, "%d/%m/%Y")
        split_end_date = end_date.split(" ")
        formatted_end_date = datetime.strptime(split_end_date[0], "%d/%m/%Y")

        if formatted_start_date <= correct_date <= formatted_end_date:
            return True
        return False

    def formatted_get_date(
        self,
        message: discord.Message = None,
        before: discord.Message = None,
        interaction: discord.Interaction = None,
    ) -> str:
        """
        Retrieves the formatted date based on the provided message, before message, or interaction.

        :param message: Discord message object.
        :type message: discord.Message or None
        :param before: Discord message object before the edit.
        :type before: discord.Message or None
        :param interaction: Discord interaction object.
        :type interaction: discord.Interaction or None
        :return: Formatted date as a string.
        :rtype: str
        """

        if message is not None:
            formatted_date = message.created_at.astimezone(zone).strftime(
                "%d/%m/%Y %H:%M"
            )
        elif before is not None:
            formatted_date = before.created_at.astimezone(zone).strftime(
                "%d/%m/%Y %H:%M"
            )
        elif interaction is not None:
            formatted_date = interaction.created_at.astimezone(zone).strftime(
                "%d/%m/%Y %H:%M"
            )
        else:
            formatted_date = datetime.now(zone).strftime("%d/%m/%Y %H:%M")

        return str(formatted_date)
