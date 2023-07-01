"""
IFSP Report Bot

This module contains the main function to start the IFSP Report Bot.
"""

from bot import start_bot
from data.member_data import MemberData
from services import StudentService
from services.member_service import MemberService


def main():
    """
    Main function to start the IFSP Report Bot.

    It initializes the StudentService and starts the bot by calling the start_bot function.
    """
    student_service = StudentService()
    member_data = MemberData()
    member_service = MemberService(member_data)

    start_bot(student_service, member_service)


if __name__ == "__main__":
    main()
