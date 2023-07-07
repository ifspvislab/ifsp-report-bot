"""
IFSP Report Bot

This module contains the main function to start the IFSP Report Bot.
"""

from bot import start_bot
from services import (
    CoordinatorService,
    MemberService,
    ParticipationService,
    ProjectService,
    StudentService,
    TerminationStatementService,
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
    termination_service = TerminationStatementService(
        member_service,
        project_service,
        participation_service,
        coordinator_service,
    )
    start_bot(
        student_service,
        termination_service,
    )


if __name__ == "__main__":
    main()
