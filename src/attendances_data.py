"""
data_attendances
====

Module for accessing and manipulating attendance data from csv files

Classes:
    - Attendances

Functions:
    - _strtime_to_time(strtime: str) -> time: Converts from string type to time type.
    - _row_to_attend(row: str) -> Attendance: Create a Attendance from a row string.
    - _load_attend() -> list[Attendance]: Read the saved Attendances.
    - load_attend() -> list[Attendance]: Returns all saved Attendences.
    - save_attend(new_attend: Attendance) -> None: Saves new attendances to the csv file,
    overwriting the saved attendance with the new one if it is from the same
    user and date

"""


from dataclasses import dataclass
from datetime import datetime, time

MONTHS = [
    "janeiro",
    "fevereiro",
    "marco",
    "abril",
    "maio",
    "junho",
    "julho",
    "agosto",
    "setembro",
    "outubro",
    "novembro",
    "dezembro",
]


@dataclass
class Attendance:
    """
    Data Class for attendances
    """

    attendance_id: str
    student_id: int
    day: datetime
    entry_time: time
    exit_time: time


def _strtime_to_time(strtime: str) -> time:
    """
    Converts from string type to time type

    :param strtime: The string data to be converted
    :type strtime: str
    :return: A time in HH:MM format
    :rtype: time
    """
    split_time = [int(part) for part in strtime.split(":")]
    return time(hour=split_time[0], minute=split_time[1])


def _strdate_to_date(strdate: str) -> datetime:
    """
    Converts from string type to datetime type
    Dates are saved in dd/mm/yyyy format

    :param strdate: The string data to be converted
    :type strdate: str
    :return: A date
    :rtype: datetime
    """
    split_date = [int(part) for part in strdate.split("/")]
    return datetime(day=split_date[0], month=split_date[1], year=split_date[2])


def _row_to_attend(row: str) -> Attendance:
    """
    Create a new Attendance from a row of data in string type

    :param row: The row of data to be made into an Attendance
    :type row: str
    :return: A Attendance instance
    :rtype: Attendance
    """
    fields = [field.strip() for field in row.split(sep=",")]
    return Attendance(
        fields[0],
        int(fields[1]),
        _strdate_to_date(fields[2]),
        _strtime_to_time(fields[3]),
        _strtime_to_time(fields[4]),
    )


def _attend_to_row(attend: Attendance) -> str:
    row = ""
    row += f"{attend.attendance_id}"
    row += f",{attend.student_id}"
    row += f",{attend.day.strftime('%d/%m/%Y')}"
    row += f",{attend.entry_time.strftime('%H:%M')}"
    row += f",{attend.exit_time.strftime('%H:%M')}\n"
    return row


def load_attend() -> list[Attendance]:
    """
    Read the assets/data/attendances.csv file and create a list of all saved Attendances

    :return: The list of all saved Attendences
    :rtype: list[Attendance]
    """
    with open("assets/data/attendances.csv", "r", encoding="utf-8") as file:
        attendances = []
        for row in file:
            attendances.append(_row_to_attend(row))
        return attendances


def save_attend(new_attend: Attendance) -> None:
    """
    Saves the data sent by the student in attendances.csv
    If the new data have the same date and student as another registered date, it will
    erase the older one

    :rtype: None
    """

    buffer = []
    is_new = True

    with open("assets/data/attendances.csv", "r", encoding="utf8") as file:
        for row in file:
            data = row.split(",")
            student_id = int(data[1])
            day = data[2]

            if student_id == new_attend.student_id:
                if day == new_attend.day.strftime("%d/%m/%Y"):
                    is_new = False
                    buffer.append(_attend_to_row(new_attend))
                    continue

            buffer.append(row)

    if is_new:
        buffer.append(_attend_to_row(new_attend))

    with open("assets/data/attendances.csv", "w", encoding="utf8") as file:
        file.writelines(buffer)
