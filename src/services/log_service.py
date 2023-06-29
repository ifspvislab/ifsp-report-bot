"""
Services for log command.
"""
import os
from datetime import datetime

import discord

import settings
from data.coordinator_data import CoordinatorData
from data.log_data import LogData
from data.student_data import StudentData

zone = settings.get_time_zone()
students_data = StudentData()
students = students_data.load_students()


class LogService:
    """
    Service class for log command.
    """

    def add_logs(self, project_id:int, student_id: int, date: str, action: str) -> None:
        """
        Adds logs to the log file.

        Parameters:
            - member_id: ID of the member associated with the log.
            - date: Date of the log entry.
            - action: Action performed for the log.

        Returns:
            None
        """
        log_list = [project_id,student_id, date, action]
        LogData.create_logs(self=LogData, data_list=log_list)

    def check_student_in_project(self, student_id: int, students: list[dict]=students) -> bool:
        """
        Checks if the given student ID is associated with a project.

        Parameters:
            - student_id: The student ID to be checked.
            - students: The list of student dictionaries.

        Returns:
            - True if the student ID is associated with a project.
            - False otherwise.
        """
        for student in students:
            if student["discord_id"] == student_id:
                return True
        return False

    def get_project_id_by_student_id(self, student_id: int, students: list[dict]=students) -> int:
        """
        Get the project ID associated with the given student ID.

        Parameters:
            - student_id: The student ID.
            - students: The list of student dictionaries.

        Returns:
            - The project ID associated with the student ID.
            Returns None if the student is not associated with any project.
        """
        for student in students:
            if student["discord_id"] == student_id:
                if "project" in student and "id" in student["project"]:
                    return student["project"]["id"]

        return None

    # def coordenator_id_validation(self):
    #     pass

    def date_validation(self, date: str, start_date: str, end_date: str) -> bool:
        """
        Validates a date within a specified range.

        Parameters:
            - date: Date to be validated.
            - start_date: Start date of the range.
            - end_date: End date of the range.

        Returns:
            - True if the date is within the range.
            - False otherwise.
        """
        split_date = date.split(" ")
        correct_date = datetime.strptime(split_date[0], "%d/%m/%Y")

        formatted_start_date = datetime.strptime(start_date, "%d/%m/%Y")
        split_end_date = end_date.split(" ")
        formatted_end_date = datetime.strptime(split_end_date[0], "%d/%m/%Y")

        if formatted_start_date <= correct_date <= formatted_end_date:
            return True
        return False

    # def file_validation(
    #     self,
    #     file="D:/Faculdade/VisLab/ifsp-report-bot/src/cogs/log.pdf",
    #     limit_in_bytes=25 * 1024 * 1024,
    # ) -> bool:
    #     """
    #     Validates the size of a file.

    #     Parameters:
    #         - file: File to be validated.
    #         - limit_in_bytes: Maximum file size in bytes.

    #     Returns:
    #         - True if the file size exceeds the limit.
    #         - False otherwise.
    #     """
    #     file_size = os.path.getsize(file)
    #     if file_size > limit_in_bytes:
    #         return True
    #     return False

    def get_date(
        self,
        message: discord.Message = None,
        before: discord.Message = None,
        interaction: discord.Interaction = None,
    ) -> str:
        """
        Retrieves the formatted date based on the provided message, before message, or interaction.

        Parameters:
            - message: Discord message object.
            - before: Discord message object before the edit.
            - interaction: Discord interaction object.

        Returns:
            - Formatted date as a string.
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
