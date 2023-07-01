"""
report_service
=======================

This module provides the ReportService class for managing interactions with the 
semester report.

Classes:
    - ReportService: Service class for managing report data.

"""


from datetime import datetime


# pylint: disable=too-few-public-methods
class ReportService:
    """
    A service class for generating reports.

    This class provides functionality to check the validity of interactions regarding the
    generation of semester reports.

    Methods:
    - invalid_request_period: Check if the request is within the allowed period.

    """

    def invalid_request_period(self):
        """
        Check if the request for generating the semester report is within the allowed period.

        :return: False if the request is within the allowed period, True otherwise.
        :rtype: bool
        """
        current_date = datetime.now().date()
        current_month = current_date.month
        current_day = current_date.day

        if current_month == 7 and 23 <= current_day <= 31:
            return False

        if current_month == 12 and 1 <= current_day <= 10:
            return False

        return True
