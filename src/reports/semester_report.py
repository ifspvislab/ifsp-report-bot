"""
semester_report
==============

This module provides classes for generating a semester report.

Classes:
    - SemesterReportData: Dataclass representing the data for a semester report.
    - SemesterReport: Class for generating a semester report.

"""
import locale
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

from . import styles
from .commons import setup_header

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")


@dataclass
class SemesterReportData:
    """
    Dataclass representing the data for a semester report.

    Attributes:
        project_title (str): The title of the project.
        project_manager (str): The name of the project manager.
        student_name (str): The name of the student.
        planned_activities (str): The planned activities for the month.
        performed_activities (str): The performed activities for the month and semester.
        results (str): The results obtained.

    """

    project_title: str
    project_manager: str
    student_name: str
    planned_activities: str
    performed_activities: str
    results: str

    def current_date(self) -> datetime:
        """
        Returns the current date of submission

        Returns:
            datetime: The current date of submission
        """
        submission_date = datetime.now()
        return datetime(
            submission_date.year, submission_date.month, submission_date.day
        )


class SemesterReport:
    """
    Class for generating a semester report.

    Attributes:
        data (SemesterReportData): The data for the semester report.
        content (list): List to store the content of the report.

    Methods:
        generate(): Generates the semester report.
        setup_header(): Sets up the header section of the report.
        setup_report_table(): Sets up the report table section of the report.
        setup_activities_section(): Sets up the activities section of the report.
        setup_signature_section(): Sets up the signature section of the report.

    """

    def __init__(self, data: SemesterReportData) -> None:
        """
        Initialize the SemesterReport object.

        Args:
            data (SemesterReportData): The data for the semester report.

        """

        self.data = data
        self.content = []

    @staticmethod
    def current_semester() -> datetime:
        """
        Returns the current semester of submission, 1st or 2nd
        Returns:
            datetime: The current semester of submission, 1st or 2nd
        """
        current_month = datetime.now().month
        if current_month <= 6:
            semester = "1º"
            return semester
        semester = "2º"
        return semester

    def generate(self):
        """
        Generates the semester report.

        Returns:
            bytes: The generated report in bytes format.

        """

        semester = self.current_semester()
        student_name = self.data.student_name
        proj_name = self.data.project_title

        month = datetime.now().strftime("%B")
        subject = f"Este documento é o relatório semestral do {semester} semestre"
        subject += f" do aluno {student_name} do projeto {proj_name}"

        title = f"relatório-semestral-{month}-{student_name}"

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=57,
            rightMargin=57,
            topMargin=57,
            bottomMargin=57,
            pageCompression=True,
            title=title,
            subject=subject,
        )

        self.content += self.generate_header()
        self.content.append(self.setup_report_table())
        self.content.append(self.setup_activities_section())
        self.content.append(self.setup_signature_section())

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
            "ANEXO IV- RELATÓRIO SEMESTRAL DE FREQUÊNCIA E AVALIAÇÃO – 2023",
            styles.header_text_style,
        )

        header_content.append(report_title)
        header_content.append(Spacer(1, 12))

        return header_content

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
            self.data.current_date().strftime("%d/%m/%Y"),
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
        semester = self.current_semester()

        month_name = datetime.now().strftime("%B")
        activities_title = Paragraph(
            f"Resumo das atividades desenvolvidas no {semester} semestre /2023",
            styles.activities_title_style,
        )
        self.content.append(activities_title)

        activities_title2 = Paragraph(
            f"Este relatório inclui as atividades desenvolvidas no mês de {month_name}/ 2023 \
                e o relatório de desempenho do(a) voluntário(a)",
            styles.activities_title_style,
        )
        self.content.append(activities_title2)

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
