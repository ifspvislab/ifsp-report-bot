"""
    Log Report
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate

from data import Log, Member, Participation

from .styles import events_header_style, events_text_style


@dataclass
# pylint: disable=too-many-instance-attributes
class LogReportData:
    """
    Data class to store log report data.

    Attributes:
    - students: A list of dictionaries representing student data.
    - logs: A list of dictionaries representing log data.
    - project_id: The project ID for filtering students.
    - value: An integer indicating the type of report to generate.
    - start_date: The start date for filtering log entries.
    - end_date: The end date for filtering log entries.
    - student_id: The ID of the student for filtering log entries.
    """

    members: list[Member]
    participations: list[Participation]
    logs: list[Log]
    project_id: str
    value: int
    start_date: datetime
    end_date: datetime
    discord_id: int


class LogReport:
    """
    Class to generate log reports based on provided data.

    Attributes:
    - content: A list to store the content of the generated report.
    - data: An instance of LogReportData containing the report data.
    """

    def __init__(self, data: LogReportData) -> None:
        self.content = []
        self.data = data

    def generate(self) -> bytes:
        """
        Generates the log report based on the provided data.
        Returns the generated report as bytes.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        if self.data.value == 1:
            self.generate_default_report()
        elif self.data.value == 2:
            self.generate_date_report()
        elif self.data.value == 3:
            self.generate_id_report()
        else:
            self.generate_id_and_date_report()

        doc.build(self.content)
        return buffer.getvalue()

    def generate_default_report(self):
        """
        Generates a default report for all students and logs.

        This method adds a title to the report and iterates over
        the student and log data to include relevant information
        in the report content.
        """

        title_report = Paragraph("Log File", events_header_style)
        self.content.append(title_report)

        for participation in self.data.participations:
            if participation.project_id == str(self.data.project_id):
                members = [
                    member
                    for member in self.data.members
                    if (participation.registration == member.registration)
                ]
                self.content.extend(
                    [Paragraph(member.name, events_header_style) for member in members]
                )

                logs = [
                    log
                    for log in self.data.logs
                    if (
                        log.registration == participation.registration
                        and log.project_id == self.data.project_id
                    )
                ]
                self.content.extend(
                    [Paragraph(log.action, events_text_style) for log in logs]
                )

    def generate_date_report(self):
        """
        Generates a report for a specific date range.

        This method adds a titled based on the specified date range,
        filters the student and log data based on the project ID,
        and includes relevant log entries in the report content.
        """

        title_report = Paragraph("Log File", events_header_style)
        self.content.append(title_report)

        for participation in self.data.participations:
            if participation.project_id == str(self.data.project_id):
                members = [
                    member
                    for member in self.data.members
                    if (participation.registration == member.registration)
                ]
                self.content.extend(
                    [Paragraph(member.name, events_header_style) for member in members]
                )

                logs = [
                    log
                    for log in self.data.logs
                    if (
                        log.registration == participation.registration
                        and log.project_id == self.data.project_id
                        and self.data.start_date
                        <= datetime.strptime(log.date, "%d/%m/%Y %H:%M")
                        <= self.data.end_date + timedelta(days=1)
                    )
                ]
                self.content.extend(
                    [Paragraph(log.action, events_text_style) for log in logs]
                )

    def generate_id_report(self):
        """
        Generates a report for a specific student ID.

        This method adds a title to the report, filters the student
        data based on the project ID and student ID, and includes
        relevant log entries in the report content.
        """

        title_report = Paragraph("Log File", events_header_style)
        self.content.append(title_report)

        for participation in self.data.participations:
            if participation.project_id == self.data.project_id:
                members = [
                    member
                    for member in self.data.members
                    if (
                        participation.registration == member.registration
                        and member.discord_id == self.data.discord_id
                    )
                ]
                self.content.extend(
                    [Paragraph(member.name, events_header_style) for member in members]
                )

                logs = [
                    log
                    for log in self.data.logs
                    if (
                        log.registration == participation.registration
                        and log.project_id == self.data.project_id
                        and log.discord_id == self.data.discord_id
                    )
                ]
                self.content.extend(
                    [Paragraph(log.action, events_text_style) for log in logs]
                )

    def generate_id_and_date_report(self):
        """
        Generates a report for a specific student ID and date range.

        This method adds a title based on the specified date range,
        filters the student data based on the project ID and student ID,
        and includes relevant log entries in the report content.
        """

        title_report = Paragraph("Log File", events_header_style)
        self.content.append(title_report)

        for participation in self.data.participations:
            if participation.project_id == self.data.project_id:
                members = [
                    member
                    for member in self.data.members
                    if (
                        participation.registration == member.registration
                        and member.discord_id == self.data.discord_id
                    )
                ]
                self.content.extend(
                    [Paragraph(member.name, events_header_style) for member in members]
                )

                logs = [
                    log
                    for log in self.data.logs
                    if (
                        log.registration == participation.registration
                        and log.project_id == self.data.project_id
                        and log.discord_id == self.data.discord_id
                        and self.data.start_date
                        <= datetime.strptime(log.date, "%d/%m/%Y %H:%M")
                        <= self.data.end_date + timedelta(days=1)
                    )
                ]
                self.content.extend(
                    [Paragraph(log.action, events_text_style) for log in logs]
                )
