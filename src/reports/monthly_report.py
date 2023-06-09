"""
monthly_report
==============

This module provides classes for generating a monthly report.

Classes:
    - MonthlyReportData: Dataclass representing the data for a monthly report.
    - MonthlyReport: Class for generating a monthly report.

"""

import locale
from dataclasses import dataclass
from datetime import datetime, timedelta
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from . import styles

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")


@dataclass
class MonthlyReportData:
    """
    Dataclass representing the data for a monthly report.

    Attributes:
        project_title (str): The title of the project.
        project_manager (str): The name of the project manager.
        student_name (str): The name of the student.
        planned_activities (str): The planned activities for the month.
        performed_activities (str): The performed activities for the month.
        results (str): The results obtained.

    """

    project_title: str
    project_manager: str
    student_name: str
    planned_activities: str
    performed_activities: str
    results: str

    def day_05_of_next_month(self) -> datetime:
        """
        Returns the date representing the 5th day of the next month.

        Returns:
            datetime: The date of the 5th day in the next month.
        """
        next_month = datetime.now() + timedelta(days=30)
        return datetime(next_month.year, next_month.month, 5)


class MonthlyReport:
    """
    Class for generating a monthly report.

    Attributes:
        data (MonthlyReportData): The data for the monthly report.
        content (list): List to store the content of the report.

    Methods:
        generate(): Generates the monthly report.
        setup_header(): Sets up the header section of the report.
        setup_report_table(): Sets up the report table section of the report.
        setup_activities_section(): Sets up the activities section of the report.
        setup_signature_section(): Sets up the signature section of the report.

    """

    def __init__(self, data: MonthlyReportData) -> None:
        """
        Initialize the MonthlyReport object.

        Args:
            data (MonthlyReportData): The data for the monthly report.

        """

        self.data = data
        self.content = []

    def generate(self):
        """
        Generates the monthly report.

        Returns:
            bytes: The generated report in bytes format.

        """

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=57,
            rightMargin=57,
            topMargin=57,
            bottomMargin=57,
            pageCompression=True,
        )
        self.setup_header()
        self.setup_report_table()
        self.setup_activities_section()
        self.setup_signature_section()
        doc.build(self.content)
        return buffer.getvalue()

    def setup_header(self):
        """
        Sets up the header section of the report.

        """
        logo = Image("./assets/img/logo_federal.jpg", width=75, height=75)
        logo.hAlign = "CENTER"
        self.content.append(logo)

        header_title = Paragraph("MINISTÉRIO DA EDUCAÇÃO", styles.header_text_style)
        self.content.append(header_title)

        sub_header_title = Paragraph(
            "INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE SÃO PAULO",
            styles.header_text_style,
        )
        self.content.append(sub_header_title)
        self.content.append(Spacer(1, 8))

        notice_title = Paragraph(
            "EDITAL Nº SPO.009, DE 1º DE FEVEREIRO DE 2023", styles.header_text_style
        )
        self.content.append(notice_title)
        self.content.append(Spacer(1, 8))

        report_title = Paragraph(
            "ANEXO IV- RELATÓRIO MENSAL DE FREQUÊNCIA E AVALIAÇÃO – 2023",
            styles.header_text_style,
        )
        self.content.append(report_title)
        self.content.append(Spacer(1, 18))

    def setup_report_table(self):
        """
        Sets up the report table section of the report.

        """
        project_title_par = Paragraph(
            self.data.project_title, styles.table_content_style
        )
        project_manager_name_par = Paragraph(
            self.data.project_manager, styles.table_content_style
        )
        student_name_par = Paragraph(self.data.student_name, styles.table_content_style)
        submission_date_par = Paragraph(
            self.data.day_05_of_next_month().strftime("%d/%m/%Y"),
            styles.table_content_style,
        )

        report_table_data = [
            [
                Paragraph("Título do Projeto", styles.table_label_style),
                project_title_par,
            ],
            [
                Paragraph("Professor(a) Responsável", styles.table_label_style),
                project_manager_name_par,
            ],
            [Paragraph("Voluntário(a)", styles.table_label_style), student_name_par],
            [
                Paragraph("Data de entrega", styles.table_label_style),
                submission_date_par,
            ],
        ]

        report_table_style = TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
            ]
        )

        report_table = Table(report_table_data, colWidths=["30%", "70%"])
        report_table.setStyle(report_table_style)
        self.content.append(report_table)

    def setup_activities_section(self):
        """
        Sets up the activities section of the report.

        """
        month_name = datetime.now().strftime("%B")
        activities_title = Paragraph(
            f"Resumo das atividades desenvolvidas no mês de {month_name}/2023",
            styles.activities_title_style,
        )
        self.content.append(activities_title)

        planned_activities = Paragraph(
            self.data.planned_activities, styles.activities_table_content_style
        )
        performed_activities = Paragraph(
            self.data.performed_activities,
            styles.activities_table_content_style,
        )
        results = Paragraph(
            self.data.results,
            styles.activities_table_content_style,
        )

        activities_data = [
            [Paragraph("Atividades planejadas:", styles.table_label_style)],
            [planned_activities],
            [Paragraph("Atividades realizadas:", styles.table_label_style)],
            [performed_activities],
            [Paragraph("Resultados obtidos:", styles.table_label_style)],
            [results],
        ]

        activities_table_style = TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
            ]
        )

        activities_table = Table(activities_data, colWidths=["100%"])
        activities_table.setStyle(activities_table_style)
        self.content.append(activities_table)

        observations_par = Paragraph(
            """Observação: Entregar este relatório via plataforma Moodle até o dia 5º de 
            cada mês, conforme previsto no edital.""",
            styles.observations_text_style,
        )
        self.content.append(observations_par)

    def setup_signature_section(self):
        """
        Sets up the signature section of the report.

        """
        signature_data = [
            [
                Paragraph("__________________________", styles.signature_content_style),
                Paragraph("__________________________", styles.signature_content_style),
            ],
            [
                Paragraph("Voluntário(a)", styles.signature_content_style),
                Paragraph("Professor(a) Responsável", styles.signature_content_style),
            ],
        ]

        signature_table = Table(signature_data, colWidths=["50%", "50%"])
        self.content.append(signature_table)
