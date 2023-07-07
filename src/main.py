"""
IFSP Report Bot

This module contains the main function to start the IFSP Report Bot.
"""

from bot import start_bot
from services import LogService, StudentService


def main():
    """
        Main function to start the IFSP Report Bot.
    ´=
        It initializes the StudentService and starts the bot by calling the start_bot function.
    """
    log_service = LogService()
    student_service = StudentService()
    start_bot(student_service, log_service)


if __name__ == "__main__":
    main()
