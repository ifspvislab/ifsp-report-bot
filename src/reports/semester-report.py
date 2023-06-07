from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    Image,
    Spacer,
)
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# Cria o relatório com tamanho A4
doc = SimpleDocTemplate(
    "relatorio_teste.pdf",
    pagesize=A4,
    leftMargin=1.18 * inch,
    rightMargin=0.79 * inch,
    topMargin=0.79 * inch,
    bottomMargin=0.79 * inch,
)

# registra a fonte 'calibri'
pdfmetrics.registerFont(TTFont("Calibri", "./assets/fonts/calibri/calibri-regular.ttf"))
pdfmetrics.registerFont(
    TTFont("Calibri-Bold", "./assets/fonts/calibri/calibri-bold.ttf")
)
pdfmetrics.registerFont(
    TTFont("Calibri-Italic", "./assets/fonts/calibri/calibri-italic.ttf")
)
pdfmetrics.registerFont(
    TTFont("Calibri-Bold-Italic", "./assets/fonts/calibri/calibri-bold-italic.ttf")
)

# Define o logo do topo

logo = Image("./assets/img/logo_federal.jpg", width=75, height=75)
logo.hAlign = "CENTER"

# Define Spacers que serão usados ao longo do arquivo
spacer1 = Spacer(0.5, 0.15 * inch)
spacer2 = Spacer(0.5, 0.30 * inch)
spacer3 = Spacer(width=0.5 * inch, height=0)

# Obtém os estilos de amostra
styles = getSampleStyleSheet()


# Define estilos do header
header_text_style = ParagraphStyle(
    name="HeaderText",
    fontSize=10,
    fontName="Calibri-Bold",
    textColor=colors.black,
    alignment=TA_CENTER,
    leading=2,
)

name_of_institution_text_style = ParagraphStyle(
    name="HeaderText",
    fontSize=10,
    fontName="Calibri-Bold",
    textColor=colors.black,
    alignment=TA_CENTER,
    leading=2,
)

public_notice_text_style = ParagraphStyle(
    name="HeaderText",
    fontSize=10,
    fontName="Calibri-Bold",
    textColor=colors.black,
    alignment=TA_CENTER,
    leading=2,
)

annex_text_style = ParagraphStyle(
    name="HeaderText",
    fontSize=10,
    fontName="Calibri-Bold",
    textColor=colors.black,
    alignment=TA_CENTER,
    leading=2,
)


activities_text_style = ParagraphStyle(
    name="HeaderText",
    fontSize=12,
    fontName="Calibri-Bold",
    textColor=colors.black,
    alignment=TA_CENTER,
    leading=12,
)

observation_text_style = ParagraphStyle(
    name="HeaderText",
    fontSize=12,
    fontName="Calibri",
    textColor=colors.black,
    leading=12,
    alignment=TA_CENTER,
)

signatures_text_style = ParagraphStyle(
    name="HeaderText",
    fontSize=12,
    fontName="Calibri",
    textColor=colors.black,
    leading=12,
    alignment=TA_CENTER,
)

participants_text_style = ParagraphStyle(
    name="HeaderText",
    fontSize=12,
    fontName="Calibri",
    textColor=colors.black,
    leading=12,
    alignment=TA_CENTER,
)

# Define o que será escrito no arquivo
header_title = Paragraph("MINISTÉRIO DA EDUCAÇÃO", header_text_style)

information_paragraph = Paragraph(
    "INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE SÃO PAULO",
    name_of_institution_text_style,
)

public_notice_paragraph = Paragraph(
    "EDITAL Nº SPO.009, DE 1º DE FEVEREIRO DE 2023", public_notice_text_style
)

annex_paragraph = Paragraph(
    "ANEXO V - RELATÓRIO SEMESTRAL DE FREQUÊNCIA E AVALIAÇÃO - 2023", annex_text_style
)

activities_paragraph1 = Paragraph(
    "Resumo das atividades desenvolvidas no ____ semestre / 2023", activities_text_style
)
activities_paragraph2 = Paragraph(
    "Este relatório inclui as atividades desenvolvidas no mês de ___________ / 2023 e o relatório de desempenho do(a) voluntário(a)",
    activities_text_style,
)

observation_paragraph = Paragraph(
    "Observação: Entregar este relatório via plataforma Moodle até o último dia 05 do semestre letivo vigente, conforme previsto no Edital.",
    observation_text_style,
)

signatures_paragraph = Paragraph(
    "________________________________&nbsp;&nbsp;&nbsp;&nbsp;________________________________",
    signatures_text_style,
)

participants_paragraph1 = Paragraph(
    "Voluntário(a)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Professor(a) Responsável",
    participants_text_style,
)


# Define os dados da tabela
table_data = [
    ["Título do Projeto", ""],
    ["Professor(a) Responsável", ""],
    ["Voluntário(a)", ""],
    ["Data de entrega", ""],
]

# Define o estilo da tabela
table_style = [
    ("GRID", (0, 0), (-1, -1), 1, "black"),  # Grid lines
    ("BACKGROUND", (0, 0), (-1, -1), colors.white),  # Background color for all cells
    ("TEXTCOLOR", (0, 0), (-1, -1), "black"),  # Text color for all cells
    ("FONTNAME", (0, 0), (-1, -1), "Calibri-Bold"),  # Font name for all cells (bold)
    ("FONTSIZE", (0, 0), (-1, -1), 12),  # Font size for all cells
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Vertical alignment for all cells
    ("LEFTPADDING", (0, 0), (-1, -1), 4.72 * inch),  # Left padding for all cells
    ("RIGHTPADDING", (0, 0), (-1, -1), 3.16 * inch),  # Right padding for all cells
]

# Cria a tabela
# A configuração dessa tabela ainda precisa ser ajeitada
table = Table(table_data)
table.setStyle(table_style)

# Adiciona os elementos ao documento
elements = [
    logo,
    spacer1,
    header_title,
    spacer1,
    information_paragraph,
    spacer2,
    public_notice_paragraph,
    spacer2,
    annex_paragraph,
    spacer3,
    table,
    activities_paragraph1,
    activities_paragraph2,
    spacer1,
    observation_paragraph,
    spacer2,
    signatures_paragraph,
    spacer1,
    participants_paragraph1,
]

# Cria o documento
doc.build(elements)
