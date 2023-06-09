"""
IFSP Report Bot

This module contains the main function to start the IFSP Report Bot.
"""

from bot import start_bot
from services import AttendanceService, StudentService


def main():
    """
    Main function to start the IFSP Report Bot.

    It initializes the StudentService and starts the bot by calling the start_bot function.
    """

    student_service = StudentService()
    attendance_service = AttendanceService()
    start_bot(student_service, attendance_service)


if __name__ == "__main__":
    main()
