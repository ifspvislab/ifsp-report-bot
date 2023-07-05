"""
report_service
=======================

This module provides the ReportService class for 
    managing interactions with the semester report.

Classes:
- ReportService: Service class for managing report data.

Exceptions:
- InvalidRequestPeriod: Custom exception class for handling requests 
    made during an invalid date period.

Functions:
- invalid_request_period: Checks if the current date is within the valid request period.

"""


from datetime import datetime

from data import MemberData


class InvalidRequestPeriod(Exception):
    """
    Custom class for handling requests made during an invalid date period.
    """


# pylint: disable=too-few-public-methods
class ReportService:
    """
    Attributes:
    member_data (MemberData): An instance of the MemberData class for accessing member data.

    Methods:
        __init__(self): Initializes the ReportService object.
        invalid_request_period(self): Checks if the current date is within the
            valid request period.
    """

    def __init__(self) -> None:
        """
        Initialize the AttendanceService object.
        """
        self.member_data = MemberData()
        self.database = self.member_data.load_members()

    def invalid_request_period(self):
        """
        Checks if the current date is within the valid request period.

        Raises:
            InvalidRequestPeriod: If the current date is outside the valid request period.

        Returns:
            bool: False if the current date is within the valid request period.
        """
        current_date = datetime.now().date()
        current_month = current_date.month
        current_day = current_date.day

        if current_month == 7 and 23 <= current_day <= 31:
            return False

        if current_month == 12 and 1 <= current_day <= 10:
            return False

        error = InvalidRequestPeriod(
            "O período de submissões ocorre entre os dias 23 a 31 "
            "de julho e 01 a 10 de dezembro."
        )
        raise error
