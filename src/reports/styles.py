"""
styles
=======================

This module provides predefined styles for report elements.

Styles:
    - header_text_style: Style for header text.
    - table_label_style: Style for table labels.
    - table_content_style: Style for table content.
    - activities_title_style: Style for activities title.
    - activities_table_content_style: Style for activities table content.
    - observations_text_style: Style for observations text.
    - signature_content_style: Style for signature content.

"""

from reportlab.lib import colors, enums
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

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

termination_text_style = ParagraphStyle(
    name="TerminationText",
    fontSize=12,
    leading=16,
    spaceBefore=5,
    spaceAfter=5,
    fontName="Calibri",
    alignment=enums.TA_JUSTIFY,
    textColor=colors.black,
)

generation_date_style = ParagraphStyle(
    name="GenerationDate",
    fontSize=12,
    leading=16,
    spaceBefore=10,
    spaceAfter=15,
    fontName="Calibri",
    alignment=enums.TA_RIGHT,
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

events_text_style = ParagraphStyle(
    name="EventsText",
    fontSize=12,
    leading=10,
    spaceAfter=3,
    fontName="Segoe",
    textColor=colors.black,
)

events_header_style = ParagraphStyle(
    name="EventsHeader",
    fontSize=16,
    leading=12,
    fontName="Calibri-Bold",
    spaceAfter=3,
    textColor=colors.black,
)

attend_table_style = ParagraphStyle(
    name="AttendSheetHeaderText", alignment=1, wordWrap=True
)
