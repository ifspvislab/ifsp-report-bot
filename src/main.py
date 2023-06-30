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

    project_data = ProjectData()
    project_service = ProjectService(project_data)
    student_service = StudentService()
    start_bot(project_service, student_service)


if __name__ == "__main__":
    main()
