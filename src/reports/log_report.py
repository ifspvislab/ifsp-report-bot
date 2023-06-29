"""
LogReport class for generating log PDF reports.
"""
import csv

from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate

from reports.styles import events_header_style, events_text_style
from services.log_service import LogService


class LogReport:
    """
    LogReport class for generating log PDF reports.
    """

    def create_pdf(
        self,
        value: int = 1,
        start_date: str = None,
        end_date: str = None,
        student_id: str = None,
    ) -> None:
        """
        Generates a PDF report based on the specified parameters.

        Parameters:
            - value: Integer value representing the report type.
            - start_date: Optional start date for log filtering.
            - end_date: Optional end date for log filtering.
            - member_id: Optional member ID for log filtering.

        Returns:
            None
        """
        doc = SimpleDocTemplate(
            "D:/Faculdade/VisLab/ifsp-report-bot/src/bot/cogs/log.pdf", pagesize=letter
        )

        content = []
        title = Paragraph("Log file", events_header_style)
        content.append(title)

        with open(
            "assets/data/logs.csv", "r", newline="", encoding="utf-8"
        ) as csv_logs:
            reader_logs = csv.reader(csv_logs)
            data_logs = list(reader_logs)

            with open(
                "assets/data/students.csv", "r", newline="", encoding="utf-8"
            ) as csv_ids:
                reader_ids = csv.reader(csv_ids)
                data_ids = list(reader_ids)

                if value == 1:
                    title = Paragraph("Value 1", events_header_style)
                    content.append(title)

                    for ids in data_ids:
                        user_title = Paragraph(ids[2], events_header_style)
                        content.append(user_title)

                        for rows in data_logs:
                            for events in rows:
                                if events == ids[0]:
                                    log_event = Paragraph(
                                        rows[-1], events_text_style)
                                    content.append(log_event)

                if value == 2:
                    title = Paragraph("Value 2", events_header_style)
                    content.append(title)
                    for ids in data_ids:
                        user_title = Paragraph(ids[2], events_header_style)
                        content.append(user_title)

                        for rows in data_logs:
                            for events in rows:
                                validation = LogService.date_validation(self=LogService,
                                    date=str(rows[2]), start_date=start_date, end_date=end_date
                                )
                                if events == ids[0] and validation:
                                    log_event = Paragraph(
                                        rows[-1], events_text_style)
                                    content.append(log_event)

                if value == 3:
                    title = Paragraph("Value 3", events_header_style)
                    content.append(title)
                    for ids in data_ids:
                        if ids[0] == student_id:
                            user_title = Paragraph(ids[2], events_header_style)
                            content.append(user_title)

                    for rows in data_logs:
                        for events in rows:
                            if events == student_id:
                                log_event = Paragraph(
                                    rows[-1], events_text_style)
                                content.append(log_event)

                if value == 4:
                    title = Paragraph("Value 4", events_header_style)
                    content.append(title)
                    for ids in data_ids:
                        if ids[0] == student_id:
                            user_title = Paragraph(ids[2], events_header_style)
                            content.append(user_title)

                    for rows in data_logs:
                        for events in rows:
                            validation = LogService.date_validation(self=LogService,
                                    date=str(rows[2]), start_date=start_date, end_date=end_date
                                )
                            if events == student_id and validation:
                                log_event = Paragraph(
                                    rows[-1], events_text_style)
                                content.append(log_event)

        doc.build(content)
