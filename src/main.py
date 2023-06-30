"""
IFSP Report Bot

This module contains the main function to start the IFSP Report Bot.
"""

from bot import start_bot
from services import MemberService, StudentService
from services.participation_service import ParticipationService
from services.project_service import ProjectService


def main():
    """
    Main function to start the IFSP Report Bot.

    It initializes the StudentService and starts the bot by calling the start_bot function.
    """

    member_service = MemberService()
    student_service = StudentService()
    project_service = ProjectService()
    participation_service = ParticipationService()
    start_bot(
        student_service,
        member_service,
        participation_service,
        project_service,
    )


if __name__ == "__main__":
    main()
