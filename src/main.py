"""
IFSP Report Bot

This module contains the main function to start the IFSP Report Bot.
"""

from bot import start_bot
from data import CoordinatorData
from services import CoordinatorService, StudentService


def main():
    """
    Main function to start the IFSP Report Bot.

    It initializes the StudentService and starts the bot by calling the start_bot function.
    """

    student_service = StudentService()
    coordinator_data = CoordinatorData()
    coordinator_service = CoordinatorService(coordinator_data)
    start_bot(student_service, coordinator_service)


if __name__ == "__main__":
    main()
