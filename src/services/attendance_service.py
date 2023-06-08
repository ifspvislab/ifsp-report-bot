"""
attendance_service
=======================

This module provides the AttendanceService class for managing Attendance data.

Classes:
    - AttendanceService: Service class for managing attendance data.
"""
from datetime import datetime, time

from data import Attendance, load_attend


class AttendanceService:
    """
    Service class for managing attendance data.

    Methods:
        - __init__(): Initialize the AttendanceService object.
        - find_attendances_by_discord_id(self, discord_id: int) -> list[Attendance]:
        Find all attendances by Discord ID in the attendances database.

    Attributes:
        - database: List to store attendance data.
    """

    def __init__(self) -> None:
        """
        Initialize the AttendanceService object.

        Sets up the initial state by creating an empty `database` list to store attendance data.
        """
        self.database = []

    def find_attendances_by_discord_id(self, discord_id: int) -> list[Attendance]:
        """
        Find all attendances associated with a Discord ID in the attendances database.

        :param discord_id: The discord id of a student
        :type discord_id: int
        :return: A list of all Attendances associated with a student's discord id
        :rtype: list[Attendance]
        """
        if not self.database:
            self.database = load_attend()
        student_attendances = []
        for attendance in self.database:
            if discord_id == attendance.student_id:
                student_attendances.append(attendance)
        return student_attendances

    def is_valid_day(self, test_day: str) -> bool:
        """
        Verifies if the day passed by the user is valid.
        Ex: Verifies if the day is a sunday or a existent date (based on the current month)

        :param test_day: The day to be verified
        :type test_day: str
        :return: True if it is valid or False if it is invalid
        :rtype: bool
        """
        curr_day = datetime.now()
        try:
            date = datetime(year=curr_day.year, month=curr_day.month, day=int(test_day))
        except ValueError:  # if the day is out of range, it will raise a ValueError
            return False
        except Exception as ex:
            raise ex
        if date.weekday() == 6:  # The campus is closed at sundays
            return False
        return True

    def is_valid_time(self, weekday: int, param_time: str) -> bool:
        """
        Verifies if the time passed by the user is valid.
        Ex: Verifies if the time is before 6:30 or after 23:30 (13h on saturdays)

        :param weekday: The weekday calculated by the program (0 = monday, 1 = tuesday,...)
        :type weekday: int
        :param param_time: The time to be verified
        :type param_time: str
        :return: True if it is valid or False if it is invalid
        :rtype: bool
        """
        try:
            split_time = [int(part) for part in param_time.split(":")]
            test_time = time(hour=split_time[0], minute=split_time[0])
        except ValueError:  # if the time is invalid (ex: hour > 23), it will raise a ValueError
            return False
        except Exception as ex:
            raise ex
        # The campus opens at 6:30
        if test_time < time(hour=6, minute=30):
            return False
        # The campus closes at 23:30 between Monday and Friday
        if test_time > time(hour=23, minute=30) and 0 <= weekday <= 4:
            return False
        # The campus closes at 13:00 at Saturdays
        if test_time > time(hour=13, minute=0) and weekday == 5:
            return False
        return True
