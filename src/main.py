"""
IFSP Report Bot

This module contains the main function to start the IFSP Report Bot.
"""

from bot import start_bot
from data.member_data import MemberData
from data.project_data import ProjectData
from services import StudentService
from services.member_service import MemberService
from services.project_service import ProjectService
from services.report_service import ReportService


def main():
    """
    Main function to start the IFSP Report Bot.

    It initializes the StudentService,
    MemberService, ProjectService and ReportService
    and starts the bot by calling the start_bot function.
    """
    student_service = StudentService()
    member_data = MemberData()
    member_service = MemberService(member_data)
    project_data = ProjectData()
    project_service = ProjectService(project_data)
    report_service = ReportService()

    start_bot(student_service, member_service, project_service, report_service)


if __name__ == "__main__":
    main()
