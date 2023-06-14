"""
attendance_sheet
==============

This module provides classes for generating the attendance sheet.

Classes:
    - AttendanceSheetData: Defines the necessary data that needs to be sent to the
    attendance sheet
    - AttendanceSheet: Generates the attendance sheet from the data sent

"""


import calendar
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from data.attendances_data import MONTHS, Attendance

from . import styles
from .commons import setup_header


@dataclass
class AttendanceSheetData:
    """
    Defines the necessary data that needs to be sent to the attendance sheet

    Attributes:
        student_name (str): The name of the student.
        current_date (datetime): The creation date of the document.
        project_name (str): The name of the project.
        attendances (list[Attendance]): All Attendances of the current month
    """

    student_name: str
    student_registration: str
    current_date: datetime
    project_name: str
    attendances: list[Attendance]


class AttendanceSheet:
    """
    Generates the attendance sheet from the data sent

    Attributes:
        data (AttendanceSheetData): The data for the attendance sheet.
        content (list): List to store the content of the sheet.
        total_hours (timedelta): The total hours of the attendances

    Methods:
        generate(): Generates the attendance sheet.
        generate_header(): Sets up the header section of the sheet.
        generate_upper_table(): Create the table with the student name, project name, etc.
        generate_mid_table(): Create the attendances section.
        generate_lower_table(): Create the total hours and signature section.


    """

    def __init__(self, data: AttendanceSheetData) -> None:
        """
        Initialize the AttendanceSheet object.

        Args:
            data (AttendanceSheetData): The data for the attendance sheet.

        """
        self.content = []
        self.data = data
        self.total_hours = timedelta()

    def _seconds_to_hours_minutes(self, seconds: float) -> tuple[int, int]:
        total_seconds = seconds
        hours = int(total_seconds / 3600)
        minutes = int((total_seconds % 3600) / 60)
        return (hours, minutes)

    def _calc_time_difference(self, entry_time: time, exit_time: time):
        # Converting the time into datetime to calculate the difference
        converted_entry_time = datetime.strptime(entry_time.isoformat(), "%H:%M:%S")
        converted_exit_time = datetime.strptime(exit_time.isoformat(), "%H:%M:%S")
        return converted_exit_time - converted_entry_time

    def generate(self) -> bytes:
        """
        Generates the attendance sheet.

        :return: The pdf bytes created by the function
        :rtype: bytes
        """

        month = MONTHS[self.data.current_date.month - 1]
        student_name = self.data.student_name
        proj_name = self.data.project_name

        # Breaking line to not exceed 100 characters
        subject = "Este documento é a folha de frequência do mês"
        subject += f"{month} do aluno {student_name} do projeto {proj_name}"

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=cm * 2,
            rightMargin=cm * 2,
            topMargin=cm * 1.5,
            bottomMargin=cm * 2,
            pageCompression=True,
            subject=subject,
            title=f"folha-de-frequencia-{month}-{student_name}-{self.data.student_registration}",
        )

        self.content += self.generate_header()
        self.content.append(self.generate_upper_table())
        self.content.append(self.generate_mid_table())
        self.content.append(self.generate_lower_table())

        doc.build(self.content)
        return buffer.getvalue()

    def generate_header(self) -> list:
        """
        Sets up the header section of the sheet.

        :return: List of all header contents
        :rtype: list
        """
        header_content = []
        header_content += setup_header()

        header_content.append(Spacer(1, 12))

        report_title = Paragraph(
            "ANEXO VI  - FOLHA DE FREQUÊNCIA", style=styles.header_text_style
        )

        header_content.append(report_title)
        header_content.append(Spacer(1, 12))

        return header_content

    def generate_upper_table(self) -> Table:
        """
        Create the table with the student name, project name, etc.

        :return: The table with it's contents
        :rtype: Table
        """
        upper_table_data = [
            ["Folha de Frequência - Projetos de Ensino"],
            [
                f"Nome: {self.data.student_name}",
                f"Mês: {self.data.current_date.month}",
                f"Ano: {self.data.current_date.year}",
            ],
            [f"Projeto: {self.data.project_name}"],
            [
                Paragraph(
                    "Lotação: Instituto Federal de Educação - <i>Campus</i> São Paulo"
                )
            ],
        ]

        upper_table_style = TableStyle(
            [
                ("SPAN", (0, 0), (-1, 0)),
                ("SPAN", (0, 2), (-1, 2)),
                ("SPAN", (0, 3), (-1, 3)),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("GRID", (0, 0), (-1, 0), 0.5, colors.black),
                ("GRID", (0, 2), (-1, 2), 0.5, colors.black),
                ("GRID", (0, 3), (-1, 3), 0.5, colors.black),
                ("BOX", (0, 1), (2, 1), 0.5, colors.black),
                ("BOX", (-2, 1), (-1, 1), 0.5, colors.black),
                ("LINEBELOW", (0, 1), (-1, 1), 1.5, colors.black),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ]
        )

        upper_table = Table(
            data=upper_table_data,
            style=upper_table_style,
            colWidths=["60%", "20%", "20%"],
        )

        return upper_table

    def generate_mid_table(self) -> Table:
        """
        Create the attendances section.

        :return: The table with all attendances inserted
        :rtype: Table
        """

        # Used later to convert datetime.weekday() to the correct weekday in portuguese
        weekdays = [
            "Segunda-feira",
            "Terça-feira",
            "Quarta-feira",
            "Quinta-feira",
            "Sexta-feira",
            "Sábado",
            "Domingo",
        ]

        content = [
            [
                # "Dia" is not a Paragraph just so pylint don't red my code
                "Dia",
                Paragraph("Dia da semana", style=styles.attend_table_style),
                Paragraph("Hora de entrada", style=styles.attend_table_style),
                Paragraph("Hora de saída", style=styles.attend_table_style),
                Paragraph("Tempo de Atividade", style=styles.attend_table_style),
                Paragraph("Assinatura", style=styles.attend_table_style),
            ]
        ]

        # Gets the day of all the attendances
        attendances_dates = [attendance.day.day for attendance in self.data.attendances]

        # Recieves a tuple with the last weekday[0] and the last day[1] of the month
        last_day = calendar.monthrange(
            year=self.data.current_date.year, month=self.data.current_date.month
        )
        # For each day in the month, verifies if there is an attendance
        # If yes, add the attendance's data into the table
        for i in range(1, last_day[1] + 1):
            line = [
                f"{i}",
                f"{weekdays[self.data.current_date.replace(day=i).weekday()]}",
            ]

            if i in attendances_dates:
                index = attendances_dates.index(i)
                entry_time = self.data.attendances[index].entry_time
                exit_time = self.data.attendances[index].exit_time
                # The program calculates the difference between the entry time and exit time
                # to find the attendance time

                difference = self._calc_time_difference(
                    entry_time=entry_time, exit_time=exit_time
                )
                self.total_hours += difference
                hours, minutes = self._seconds_to_hours_minutes(
                    difference.total_seconds()
                )

                line += [
                    f"{entry_time.strftime('%H:%M')}",
                    f"{exit_time.strftime('%H:%M')}",
                    f"{hours}h {minutes}m",
                ]

            content.append(line)

        mid_table_style = TableStyle(
            [
                ("LEFTPADDING", (0, 0), (0, -1), 1),
                ("RIGHTPADDING", (0, 0), (0, -1), 1),
                ("TOPPADDING", (0, 0), (-1, 0), 0),
                ("TOPPADDING", (0, 1), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 0),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 1),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )

        mid_table = Table(
            data=content,
            style=mid_table_style,
            colWidths=["5%", "25%", "15%", "15%", "15%", "30%"],
        )

        return mid_table

    def generate_lower_table(self) -> Table:
        """
        Create the total hours and signature section.

        :return: The footer of the table, with the signature and the total hours
        :rtype: Table
        """
        hours, minutes = self._seconds_to_hours_minutes(
            self.total_hours.total_seconds()
        )
        content = [
            ["", "", "Total de horas trabalhadas:", "", f"{hours}h {minutes}m", ""],
            [],
            ["Assinatura do professor responsável", "", "", "", "", "Data: __/__/____"],
        ]

        lower_table_style = TableStyle(
            [
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                ("SPAN", (2, 0), (3, 0)),
                ("SPAN", (0, -1), (2, -1)),
                ("SPAN", (3, -1), (4, -1)),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BOX", (4, 0), (4, 0), 0.5, colors.black),
                ("LINEABOVE", (0, 0), (-1, 0), 0.5, colors.black),
                ("LINEBELOW", (3, -1), (4, -1), 0.5, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )

        lower_table = Table(
            data=content,
            style=lower_table_style,
            colWidths=["5%", "25%", "15%", "15%", "15%", "30%"],
        )

        return lower_table
