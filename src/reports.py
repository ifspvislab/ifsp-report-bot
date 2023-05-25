"""
Reports module

This module provides functions for generating monthly reports in PDF format.

Dependencies:
- io from io
- logging from logging
- A4 from reportlab.lib.pagesizes
- getSampleStyleSheet, ParagraphStyle from reportlab.lib.styles
- SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image from reportlab.platypus
- colors, enums from reportlab.lib
- pdfmetrics from reportlab.pdfbase
- TTFont from reportlab.pdfbase.ttfonts

Functions:
- _setup_reports_module(): Set up the reports module.
- _register_fonts(): Register the required fonts.
- generate_monthly_report(): Generate a monthly report PDF and return bytes.

"""

from io import BytesIO
import logging
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Spacer,
    Image,
)
from reportlab.lib import colors, enums
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def _setup_reports_module():
    """
    Set up the reports module.

    Configure the logging library with the INFO log level and a specific format.
    Register the required fonts for PDF reports.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s --- [%(filename)s | %(funcName)s] : %(message)s",
    )
    logging.info("starting the setup of the reports module")
    _register_fonts()
    logging.info("report module setup done")


def _register_fonts():
    """
    Register the required fonts.

    Register the necessary fonts for PDF reports using the pdfmetrics module.
    """
    pdfmetrics.registerFont(
        TTFont("Calibri", "assets/fonts/calibri/calibri-regular.ttf")
    )
    pdfmetrics.registerFont(
        TTFont("Calibri-Bold", "assets/fonts/calibri/calibri-bold.ttf")
    )
    pdfmetrics.registerFont(
        TTFont("Calibri-Italic", "assets/fonts/calibri/calibri-italic.ttf")
    )
    pdfmetrics.registerFont(
        TTFont("Calibri-Bold-Italic", "assets/fonts/calibri/calibri-bold-italic.ttf")
    )
    logging.info("register fonts executed")


def generate_monthly_report():
    """
    Generate monthly report PDF and return bytes.

    Returns:
        bytes: PDF document in bytes format.
    """

    styles = getSampleStyleSheet()

    header_text_style = ParagraphStyle(
        name="HeaderText",
        fontSize=10,
        leading=12,
        fontName="Calibri-Bold",
        alignment=enums.TA_CENTER,
        spaceAfter=3,
        textColor=colors.black,
    )

    table_label_style = ParagraphStyle(
        name="TableLabel",
        fontSize=12,
        fontName="Calibri-Bold",
        leading=12,
        alignment=enums.TA_LEFT,
        textColor=colors.black,
    )

    table_content_style = ParagraphStyle(
        name="TableContent",
        parent=styles["Normal"],
        alignment=enums.TA_JUSTIFY,
        fontSize=12,
        leading=12,
        fontName="Calibri",
    )

    activities_title_style = ParagraphStyle(
        name="ActivitiesTitle",
        parent=styles["Normal"],
        alignment=enums.TA_CENTER,
        spaceBefore=15,
        spaceAfter=15,
        textColor=colors.black,
        fontSize=12,
        fontName="Calibri-Bold",
    )

    activities_table_content_style = ParagraphStyle(
        name="ActivitiesTableContent",
        parent=table_content_style,
        leading=18,
    )

    observations_text_style = ParagraphStyle(
        name="HeaderText",
        fontSize=12,
        leading=16,
        fontName="Calibri",
        alignment=enums.TA_JUSTIFY,
        spaceBefore=5,
        spaceAfter=30,
        textColor=colors.black,
    )

    signature_content_style = ParagraphStyle(
        name="SignatureContent",
        parent=styles["Normal"],
        alignment=enums.TA_CENTER,
        fontSize=12,
        leading=12,
        fontName="Calibri",
    )

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=57,
        rightMargin=57,
        topMargin=57,
        bottomMargin=57,
    )

    content = []

    logo = Image("assets/img/logo_federal.jpg", width=75, height=75)
    logo.hAlign = "CENTER"
    content.append(logo)

    header_title = Paragraph("MINISTÉRIO DA EDUCAÇÃO", header_text_style)
    content.append(header_title)

    sub_header_title = Paragraph(
        "INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE SÃO PAULO",
        header_text_style,
    )
    content.append(sub_header_title)
    content.append(Spacer(1, 8))

    notice_title = Paragraph(
        "EDITAL Nº SPO.009, DE 1º DE FEVEREIRO DE 2023", header_text_style
    )
    content.append(notice_title)
    content.append(Spacer(1, 8))

    report_title = Paragraph(
        "ANEXO IV- RELATÓRIO MENSAL DE FREQUÊNCIA E AVALIAÇÃO – 2023",
        header_text_style,
    )
    content.append(report_title)
    content.append(Spacer(1, 18))

    project_title_par = Paragraph(
        "Titulo do Projeto bem grande para ver como fica o layout", table_content_style
    )
    project_manager_name_par = Paragraph("Nome do Responsável", table_content_style)
    student_name = Paragraph(
        "Nome Completo do Aluno com Sobrenome", table_content_style
    )
    submission_date_par = Paragraph("05/05/2023", table_content_style)

    report_table_data = [
        [Paragraph("Título do Projeto", table_label_style), project_title_par],
        [
            Paragraph("Professor(a) Responsável", table_label_style),
            project_manager_name_par,
        ],
        [Paragraph("Voluntário(a)", table_label_style), student_name],
        [Paragraph("Data de entrega", table_label_style), submission_date_par],
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
    content.append(report_table)

    activities_title = Paragraph(
        "Resumo das atividades desenvolvidas no Mês de abril/2023",
        activities_title_style,
    )
    content.append(activities_title)

    planned_activities = Paragraph(
        """ 
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam porttitor 
        et tellus eu congue. Nunc accumsan lobortis metus, id tincidunt dui bibendum vitae. 
        Integer feugiat tincidunt nunc. Sed luctus, purus eget consectetur tristique, 
        nulla mauris feugiat orci, quis tempor arcu odio non sem. Maecenas accumsan maximus 
        fermentum. Aenean mattis aliquet tincidunt.
        """,
        activities_table_content_style,
    )
    performed_activities = Paragraph(
        """ 
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam porttitor 
        et tellus eu congue. Nunc accumsan lobortis metus, id tincidunt dui bibendum vitae. 
        Integer feugiat tincidunt nunc. Sed luctus, purus eget consectetur tristique, 
        nulla mauris feugiat orci, quis tempor arcu odio non sem. Maecenas accumsan maximus 
        fermentum. Aenean mattis aliquet tincidunt.
        """,
        activities_table_content_style,
    )
    results = Paragraph(
        """ 
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam porttitor 
        et tellus eu congue. Nunc accumsan lobortis metus, id tincidunt dui bibendum vitae. 
        Integer feugiat tincidunt nunc. Sed luctus, purus eget consectetur tristique, 
        nulla mauris feugiat orci, quis tempor arcu odio non sem. Maecenas accumsan maximus 
        fermentum. Aenean mattis aliquet tincidunt.
        """,
        activities_table_content_style,
    )

    activities_data = [
        [Paragraph("Atividades planejadas:", table_label_style)],
        [planned_activities],
        [Paragraph("Atividades realizadas:", table_label_style)],
        [performed_activities],
        [Paragraph("Resultados obtidos:", table_label_style)],
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
    content.append(activities_table)

    observations_par = Paragraph(
        """Observação: Entregar este relatório via plataforma Moodle até o dia 5º de 
        cada mês, conforme previsto no edital.""",
        observations_text_style,
    )
    content.append(observations_par)

    signature_data = [
        [
            Paragraph("__________________________", signature_content_style),
            Paragraph("__________________________", signature_content_style),
        ],
        [
            Paragraph("Voluntário(a)", signature_content_style),
            Paragraph("Professor(a) Responsável", signature_content_style),
        ],
    ]

    signature_table = Table(signature_data, colWidths=["50%", "50%"])
    content.append(signature_table)

    doc.build(content)

    return buffer.getvalue()


_setup_reports_module()
