"""
IFSP Report Bot

This module contains the main function to start the IFSP Report Bot.
"""

from bot import start_bot
from data import CoordinatorData, ParticipationData
from services import CoordinatorService, ParticipationService, StudentService


def main():
    """
    Main function to start the IFSP Report Bot.

    It initializes the StudentService and starts the bot by calling the start_bot function.
    """

    participation_data = ParticipationData
    coordinator_data = CoordinatorData
    student_service = StudentService()
    coordinator_service = CoordinatorService(coordinator_data)
    participation_service = ParticipationService(participation_data)
    start_bot(student_service, participation_service, coordinator_service)


if __name__ == "__main__":
    main()
