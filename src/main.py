"""
IFSP Report Bot

This module contains the main function to start the IFSP Report Bot.
"""

from bot import start_bot
from data import CoordinatorData, LogData, MemberData, ParticipationData, ProjectData
from services import LogService, MemberService, ProjectService, StudentService


def main():
    """
        Main function to start the IFSP Report Bot.
    ´=
        It initializes the StudentService and starts the bot by calling the start_bot function.
    """
    coordinator_data = CoordinatorData()
    project_data = ProjectData()
    project_service = ProjectService(project_data, coordinator_data)
    member_data = MemberData()
    member_service = MemberService(member_data)
    student_service = StudentService()
    participation_data = ParticipationData()

    log_data = LogData()
    log_service = LogService(
        log_data, member_data, participation_data, project_service, member_service
    )
    student_service = StudentService()
    start_bot(student_service, log_service)


if __name__ == "__main__":
    main()
