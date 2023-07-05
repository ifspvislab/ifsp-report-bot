"""
IFSP Report Bot

This module contains the main function to start the IFSP Report Bot.
"""

from bot import start_bot
from services import (
    MemberService,
    StudentService,
    ParticipationService,
    ProjectService,
    CoordinatorService
)



def main():
    """
    Main function to start the IFSP Report Bot.

    It initializes the StudentService and starts the bot by calling the start_bot function.
    """
    member_service = MemberService()
    student_service = StudentService()
    project_service = ProjectService()
    participation_service = ParticipationService()
    coordinator_service = CoordinatorService()
    start_bot(
        student_service,
        member_service,
        participation_service,
        project_service,
        coordinator_service
    )


if __name__ == "__main__":
    main()
