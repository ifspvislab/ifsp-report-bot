"""
IFSP Report Bot

This module contains the main function to start the IFSP Report Bot.
"""

from bot import start_bot
from data import ProjectData
from services import ProjectService, StudentService


def main():
    """
    Main function to start the IFSP Report Bot.

    It initializes the StudentService and starts the bot by calling the start_bot function.
    """

    student_service = StudentService()
    project_data = ProjectData()
    project_service = ProjectService(project_data)
    start_bot(student_service, project_service)


if __name__ == "__main__":
    main()
