"""
Services for log command.
"""
from datetime import datetime

import discord

import settings
from data import CoordinatorData, ProjectData, StudentData

zone = settings.get_time_zone()
students_data = StudentData().load_students()
projects_data = ProjectData().load_projects()


class IncorrectDateFilter(Exception):
    """Incorrect date filter"""


def is_coordinator(interaction: discord.Interaction):
    """
    Check if the user is a coordinator.

    This function checks if the user associated with the provided `discord.Interaction`
    is a coordinator by comparing their Discord ID with the coordinators' Discord IDs
    stored in the coordinator data.

    :param interaction: The Discord interaction object.
    :type interaction: discord.Interaction
    :return: True if the user is a coordinator, False otherwise.
    :rtype: bool
    """
    discord_id = interaction.user.id
    coordinators = CoordinatorData.load_coordinators(self=CoordinatorData)

    for coordinator in coordinators:
        if str(coordinator.discord_id) == str(discord_id):
            return True
    return False


class LogService:
    """
    Service class for log command.
    """

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
            students = students_data

        for student in students:
            if student["discord_id"] == student_id:
                return True
        return False

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
            projects = projects_data

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
