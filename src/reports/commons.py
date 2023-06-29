"""
commons.py

Unifies functions used by different reports in a single place

Functions:
 - setup_header: Create the header of the report and return it to the caller
"""


from reportlab.platypus import Image, Paragraph, Spacer

from . import styles


def setup_header() -> list:
    """
    Sets up the header section of the report.

    :returns: The report header
    :rtype: list
    """

    content = []

    logo = Image("./assets/img/logo_federal.jpg", width=75, height=75)
    logo.hAlign = "CENTER"
    content.append(logo)

    header_title = Paragraph("MINISTÉRIO DA EDUCAÇÃO", styles.header_text_style)
    content.append(header_title)

    sub_header_title = Paragraph(
        "INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE SÃO PAULO",
        styles.header_text_style,
    )
    content.append(sub_header_title)
    content.append(Spacer(1, 8))

    notice_title = Paragraph(
        "EDITAL Nº SPO.009, DE 1º DE FEVEREIRO DE 2023", styles.header_text_style
    )
    content.append(notice_title)

    return content
