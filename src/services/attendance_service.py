"""
attendance_service
=======================

This module provides the AttendanceService class for managing Attendance data.

Classes:
    - AttendanceService: Service class for managing attendance data.
"""
import uuid
from datetime import datetime, time

from data import Attendance, AttendanceData
from reports import AttendanceSheet, AttendanceSheetData


class InvalidDate(Exception):
    """
    Custom exception for invalid dates, such as 60/15/-133 or "abc"
    """


class InvalidTime(Exception):
    """
    Custom exception for invalid times, such as 28:75 or "idk"
    """


class DayOutOfRange(Exception):
    """
    Custom exception for sundays, since IFSP is closed these weekdays
    """


class TimeOutOfRange(Exception):
    """
    Custom exception for times outside of the IFSP's buiseness hours
    """


class EntryTimeAfterExitTime(Exception):
    """
    Custom exception for when the entry time is after the exit time
    """


class AttendanceService:
    """
    Service class for managing attendance data.

    Methods:
        - __init__(): Initialize the AttendanceService object.
        - find_attendances_by_discord_id(self, discord_id: int) -> list[Attendance]:
        Find all attendances by Discord ID in the attendances database.
        - _is_valid_day(self, test_day: str) -> None | datetime:
        Verifies if the day passed by the user is valid.
        - _is_valid_time(self, weekday: int, param_time: str) -> None | time:
        Verifies if the time passed by the user is valid.
        - _is_entry_before(self, entry_time: time, exit_time: time) -> bool:
        Tests if the exit time passed by the user is before the entry time
        - validate_data(self, day: str, entry_time: str, exit_time: str) -> list[str]:
        Validates the day, entry time and exit time sent by the user and return the errors


    Attributes:
        - database: List to store attendance data.
    """

    def __init__(self) -> None:
        """
        Initialize the AttendanceService object.

        Sets up the initial state by creating an empty `database` list to store attendance data.
        """
        self.attend_data = AttendanceData()
        self.database = self.attend_data.load_attend()

    def find_attendances_by_member_id(self, member_id: str) -> list[Attendance]:
        """
        Find all attendances associated with a member in the attendances database.

        :param member_id: The member id of a student
        :type member_id: str
        :return: A list of all Attendances associated with a student's id
        :rtype: list[Attendance]
        """

        student_attendances: list[Attendance] = []
        for attendance in self.database:
            if member_id == attendance.student_id:
                student_attendances.append(attendance)
        return student_attendances

    def find_attends_by_member_and_project(
        self, member_id: str, proj_id: str
    ) -> list[Attendance]:
        """
        Method that gets all attendances related to a specific member and project

        :param member_id: The member uuid of a student
        :type member_id: str
        :param member_id: The project uuid
        :type member_id: str
        :return: A list of all Attendances associated with the member and the project
        :rtype: list[Attendance]
        """
        student_attendances: list[Attendance] = []
        for attendance in self.database:
            if member_id == attendance.student_id:
                if proj_id == attendance.project_id:
                    student_attendances.append(attendance)
        return student_attendances

    def _validate_day(self, test_day: str) -> datetime:
        """
        Verifies if the day passed by the user is valid.
        Ex: Verifies if the day is a sunday or a existent date (based on the current month)

        :param test_day: The day to be verified
        :type test_day: str
        :return: the date if it is valid or None if it is invalid
        :rtype: None | datetime
        """
        curr_day = datetime.now()
        try:
            date = datetime(year=curr_day.year, month=curr_day.month, day=int(test_day))
        except ValueError as exc:
            raise InvalidDate(
                "A data passada não é válida (precisa ser um número entre os dias do mês)."
            ) from exc

        if date.weekday() == 6:  # The campus is closed at sundays
            raise DayOutOfRange("O campus não está aberto de domingo.")
        return date

    def _validate_time(self, weekday: int, param_time: str) -> time:
        """
        Verifies if the time passed by the user is valid.
        Ex: Verifies if the time is before 6:30 or after 23:30 (13h on saturdays)

        :param weekday: The weekday calculated by the program (0 = monday, 1 = tuesday,...)
        :type weekday: int
        :param param_time: The time to be verified
        :type param_time: str
        :return: the time if it is valid or None if it is invalid
        :rtype: None | time
        """
        try:
            split_time = [int(part) for part in param_time.split(":")]
            test_time = time(hour=split_time[0], minute=split_time[1])
        # if the time is invalid (ex: hour > 23), it will raise a ValueError
        except ValueError as exc:
            raise InvalidTime(
                "Tempo inválido (passe no formato HH:MM de 24 horas)"
            ) from exc
        except Exception as ex:
            raise ex
        # The campus opens at 6:30
        if test_time < time(hour=6, minute=30):
            raise TimeOutOfRange("O campus só abre às 6:30 de segunda-feira à sábado")
        # The campus closes at 23:30 between Monday and Friday
        if test_time > time(hour=23, minute=30) and 0 <= weekday <= 4:
            raise TimeOutOfRange("O campus fecha às 23:30 de segunda à sexta-feira")
        # The campus closes at 13:00 at Saturdays
        if test_time > time(hour=13, minute=0) and weekday == 5:
            raise TimeOutOfRange("O campus fecha às 13:00 de sábado")
        return test_time

    def _is_entry_before(self, entry_time: time, exit_time: time) -> None:
        """
        Tests if the exit time passed by the user is before the entry time

        :param entry_time: The entry time passed by the user
        :type entry_time: time
        :param exit_time: The exit time passed by the user
        :type exit_time: time
        :return: True if the entry is before and false if it is not
        :rtype: bool
        """
        if entry_time > exit_time:
            raise EntryTimeAfterExitTime(
                "O horário de saída não pode ser anterior à entrada"
            )

    def _get_date_already_saved(self, new_attendance: Attendance) -> int | None:
        """
        Verifies if an attendance is already saved in the database
        If the function finds an already saved attendance with the same student_id and date,
        returns the index of the saved attendance

        :param new_attendance: The attendance to be verified
        :type new_attendance: Attendance
        :return: The index of the already saved attendance
        :rtype: int
        """
        for index, attendance in enumerate(self.database):
            if attendance.student_id == new_attendance.student_id:
                if attendance.day.day == new_attendance.day.day:
                    return index

        return None

    # pylint: disable-next=too-many-arguments
    def create_attendance(
        self, day: str, entry_time: str, exit_time: str, user_id: str, proj_id: str
    ) -> None:
        """
        Validates the day, entry time and exit time sent by the user and creates a new attendance.
        If the user didn't sent a date, selects the current date

        :param day: The day passed by the user
        :type day: str
        :param entry_time: The entry time passed by the user
        :type entry_time: str
        :param exit_time: The exit time passed by the user
        :type exit_time: str
        """

        test_day = day
        test_entry_time = entry_time
        test_exit_time = exit_time

        if test_day is None:
            test_day = datetime.now()
        else:
            test_day = self._validate_day(test_day)

        test_entry_time = self._validate_time(
            weekday=test_day.weekday(), param_time=entry_time
        )
        test_exit_time = self._validate_time(
            weekday=test_day.weekday(), param_time=exit_time
        )
        self._is_entry_before(entry_time=test_entry_time, exit_time=test_exit_time)

        new_attend = Attendance(
            attendance_id=str(uuid.uuid4()),
            student_id=user_id,
            project_id=proj_id,
            day=test_day,
            entry_time=test_entry_time,
            exit_time=test_exit_time,
        )

        index = self._get_date_already_saved(new_attend)
        if index is None:
            self.database.append(new_attend)
        else:
            self.database[index] = new_attend
        self.attend_data.save_attend(new_attend)

    def get_all_students_id(self) -> set[str]:
        """
        Iterates over the database and gets all students_id without repetition

        :return: A set with all student_ids
        :rtype: set[str]
        """
        all_students = set()
        for attendance in self.database:
            all_students.add(attendance.student_id)

        return all_students

    def create_sheet(
        self,
        student_name: str,
        student_registration: str,
        project_name: str,
        attendances: list[Attendance],
    ) -> bytes:
        """
        Create the current month's Attendance sheet for a student

        :param student_id: The student id
        :type student_id: str
        :param student_name: The name of the student
        :type student_name: str
        :param project_name: The attendance sheet's project name
        :type project_name: str
        :return: The bytes of the created sheet
        :rtype: bytes
        """

        current_month_attends = []
        for attendance in attendances:
            if attendance.day.month == datetime.now().month:
                current_month_attends.append(attendance)

        return AttendanceSheet(
            AttendanceSheetData(
                student_name=student_name,
                student_registration=student_registration,
                current_date=datetime.now(),
                project_name=project_name,
                attendances=current_month_attends,
            )
        ).generate()
