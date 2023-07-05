"""
IFSP Report Bot

This module contains the main function to start the IFSP Report Bot.
"""

from bot import start_bot
from data import CoordinatorData, MemberData, ParticipationData, ProjectData
from services import (
    CoordinatorService,
    MemberService,
    ParticipationService,
    ProjectService,
    ReportService,
    StudentService,
)


def main():
    """
    Main function to start the IFSP Report Bot.

    It initializes the StudentService,
    MemberService, ProjectService, ReportService, CoordinatorService
    and ParticipationService and starts the bot by
    calling the start_bot function.
    """
    student_service = StudentService()

    member_data = MemberData()
    member_service = MemberService(member_data)
    report_service = ReportService()

    project_data = ProjectData()
    project_service = ProjectService(project_data)

    coordinator_data = CoordinatorData()
    coordinator_service = CoordinatorService(coordinator_data)

    participation_data = ParticipationData()
    participation_service = ParticipationService(participation_data, member_data)

    start_bot(
        student_service,
        member_service,
        project_service,
        report_service,
        coordinator_service,
        participation_service,
    )


if __name__ == "__main__":
    main()
