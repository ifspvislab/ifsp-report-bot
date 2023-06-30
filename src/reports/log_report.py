"""
    Log Report
"""
import csv

from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate

from reports.styles import events_header_style, events_text_style
from services.log_service import LogService

content = []


class LogReport:
    """
    LogReport class for generating log PDF reports.
    """

    @staticmethod
    def generate_default_report(data_ids: list, data_logs: list, project_id: str):
        """
        Generates a default PDF report based on the specified parameters.

        Parameters:
            - data_ids: List of data IDs.
            - data_logs: List of data logs.
            - project_id: Project ID for filtering.

        Returns:
            None
        """
        title = Paragraph("Value 1 - Padrao", events_header_style)
        content.append(title)
        for ids in data_ids:
            if ids[-1] == str(project_id):
                user_title = Paragraph(ids[2], events_header_style)
                content.append(user_title)

                for rows in data_logs:
                    for events in rows:
                        if events == ids[0]:
                            log_event = Paragraph(rows[-1], events_text_style)
                            content.append(log_event)

    @staticmethod
    def generate_data_report(
        data_ids: list, data_logs: list, project_id: str, start_date: str, end_date: str
    ):
        """
        Generates a PDF report based on the specified parameters.

        Parameters:
            - data_ids: List of data IDs.
            - data_logs: List of data logs.
            - project_id: Project ID for filtering.
            - start_date: Start date for log filtering.
            - end_date: End date for log filtering.

        Returns:
            None
        """
        title = Paragraph("Value 2 - Data escolhida", events_header_style)
        content.append(title)
        for ids in data_ids:
            if ids[-1] == str(project_id):
                user_title = Paragraph(ids[2], events_header_style)
                content.append(user_title)

                for rows in data_logs:
                    for events in rows:
                        validation = LogService.date_validation(
                            self=LogService,
                            date=str(rows[2]),
                            start_date=start_date,
                            end_date=end_date,
                        )
                        if events == ids[0] and validation:
                            log_event = Paragraph(rows[-1], events_text_style)
                            content.append(log_event)

    @staticmethod
    def generate_id_report(
        data_ids: list, data_logs: list, project_id: str, student_id: str
    ):
        """
        Generates an ID-based PDF report based on the specified parameters.

        Parameters:
            - data_ids: List of data IDs.
            - data_logs: List of data logs.
            - project_id: Project ID for filtering.
            - student_id: Student ID for filtering.

        Returns:
            None
        """
        title = Paragraph("Value 3 - ID", events_header_style)
        content.append(title)
        for ids in data_ids:
            if ids[-1] == str(project_id):
                if ids[0] == student_id:
                    user_title = Paragraph(ids[2], events_header_style)
                    content.append(user_title)

        for rows in data_logs:
            for events in rows:
                if events == student_id:
                    log_event = Paragraph(rows[-1], events_text_style)
                    content.append(log_event)

    @staticmethod
    # pylint: disable-next=too-many-arguments
    def generate_id_and_data_report(
        data_ids: list,
        data_logs: list,
        project_id: str,
        start_date: str,
        end_date: str,
        student_id: str,
    ):
        """
        Generates an ID and data-based PDF report based on the specified parameters.

        Parameters:
            - data_ids: List of data IDs.
            - data_logs: List of data logs.
            - project_id: Project ID for filtering.
            - start_date: Start date for log filtering.
            - end_date: End date for log filtering.
            - student_id: Student ID for filtering.

        Returns:
            None
        """
        title = Paragraph("Value 4 - id E DATA", events_header_style)
        content.append(title)
        for ids in data_ids:
            if ids[-1] == str(project_id):
                if ids[0] == student_id:
                    title = Paragraph(ids[2], events_header_style)
                    content.append(title)

        for rows in data_logs:
            for events in rows:
                validation = LogService.date_validation(
                    self=LogService,
                    date=str(rows[2]),
                    start_date=start_date,
                    end_date=end_date,
                )
                if events == student_id and validation:
                    title = Paragraph(rows[-1], events_text_style)
                    content.append(title)

    @staticmethod
    def create_pdf(
        project_id: str = None,
        value: int = 1,
        start_date: str = None,
        end_date: str = None,
        student_id: str = None,
    ) -> None:
        """
        Generates a PDF report based on the specified parameters.

        Parameters:
            - project_id: Project ID for filtering.
            - value: Integer value representing the report type.
            - start_date: Optional start date for log filtering.
            - end_date: Optional end date for log filtering.
            - student_id: Optional student ID for log filtering.

        Returns:
            None
        """
        doc = SimpleDocTemplate(
            "D:/Faculdade/VisLab/ifsp-report-bot/src/bot/cogs/log.pdf", pagesize=letter
        )
        with open(
            "assets/data/logs.csv", "r", newline="", encoding="utf-8"
        ) as csv_logs:
            data_logs = list(csv.reader(csv_logs))

            with open(
                "assets/data/students.csv", "r", newline="", encoding="utf-8"
            ) as csv_ids:
                data_ids = list(csv.reader(csv_ids))

                switch_cases = {
                    1: (
                        LogReport.generate_default_report,
                        [data_ids, data_logs, project_id],
                    ),
                    2: (
                        LogReport.generate_data_report,
                        [data_ids, data_logs, project_id, start_date, end_date],
                    ),
                    3: (
                        LogReport.generate_id_report,
                        [data_ids, data_logs, project_id, student_id],
                    ),
                    4: (
                        LogReport.generate_id_and_data_report,
                        [
                            data_ids,
                            data_logs,
                            project_id,
                            start_date,
                            end_date,
                            student_id,
                        ],
                    ),
                }

                selected_case = switch_cases.get(value)
                if selected_case:
                    selected_function, selected_args = selected_case
                    selected_function(*selected_args)

        doc.build(content)
