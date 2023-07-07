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

    coordinator_data = CoordinatorData()
    project_data = ProjectData()
    project_service = ProjectService(project_data, coordinator_data)
    coordinator_service = CoordinatorService(coordinator_data)
    member_data = MemberData()
    member_service = MemberService(member_data)
    student_service = StudentService()
    participation_data = ParticipationData()
    participation_service = ParticipationService(
        participation_data, member_data, project_service, member_service
    )
    report_service = ReportService(
        participation_data,
        participation_service,
        coordinator_service,
        coordinator_data,
    )
    start_bot(
        student_service,
        member_service,
        coordinator_service,
        project_service,
        participation_service,
        report_service,
    )


if __name__ == "__main__":
    main()
