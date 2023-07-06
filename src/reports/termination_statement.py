""" . """

import locale
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from . import styles
from .commons import setup_header, setup_signature_section

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

MONTHS = [
    "janeiro",
    "fevereiro",
    "marco",
    "abril",
    "maio",
    "junho",
    "julho",
    "agosto",
    "setembro",
    "outubro",
    "novembro",
    "dezembro",
]


@dataclass
class TerminationStatementData:
    """
    Dataclass that represents the data for the termination statement

    """

    student_name: str
    student_code: str
    project_name: str
    project_manager: str
    termination_date: str
    termination_reason: str


class TerminationStatement:
    """
    Class for generating a termination statement

    Attributes:
        data (TerminationStatementData): The data for the termination statement.
        content (list): List to store the content of the termination statement

    Methods:
        generate(): Generates the termination statement.
        create_header(): Creates the header of the termination statement
        create_date_text(): Creates the text where the student name,
        student code, project name, project manager and termination date
        will be inserted.
        create_terminate_reason_text(): Creates the text associated with
        termination reason.
        create_agreement_text(): Creates the agreement text.
        create_generation_date_text(): Creates the generation date text.


    """

    def __init__(self, data: TerminationStatementData) -> None:
        """
        Initializes the TerminationStatement object.

        Args:
            data (TerminationStatementData): The data for the termination
            statement.
        """
        self.content = []
        self.data = data

    def generate(self):
        """
        Generates the termination statement.

        Returns the bytes of the generated termination statement
        """
        student_name = self.data.student_name
        student_code = self.data.student_code
        project_name = self.data.project_name
        title = f"termo-encerramento-{student_name}-{student_code}-{project_name}"
        subject = f""" Este documento é o termo de encerramento das atividades do aluno
        {student_name} no projeto {project_name}"""

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            title=title,
            subject=subject,
            pagesize=A4,
            leftMargin=56,
            rightMargin=57,
            topMargin=57,
            bottomMargin=57,
            pageCompression=True,
        )

        self.content += self.create_header()
        self.create_date_text()
        self.create_terminate_reason_text()
        self.create_agreement_text()
        self.create_generation_date_text()
        signature = setup_signature_section()
        self.content += signature
        doc.build(self.content)
        return buffer.getvalue()

    def create_header(self) -> list:
        """
        Creates the header section of the termination statement
        :return: list of all header contents
        :rtype: list
        """
        header_content = []
        header_spacer = Spacer(1, 10)
        header_content += setup_header()
        header_content.append(header_spacer)

        report_title = Paragraph(
            "ANEXO VII - TERMO DE ENCERRAMENTO DE PARTICIPAÇÃO EM PROJETO DE ENSINO",
            style=styles.header_text_style,
        )

        header_content.append(report_title)
        header_content.append(header_spacer)

        return header_content

    def create_date_text(self):
        """
        Creates the text associated with student name,
        student code, project name, project manager and
        termination date.

        """
        date_paragraph = Paragraph(
            f"""Eu, <u>{self.data.student_name}</u>, prontuário <u>
            {self.data.student_code}</u>, Voluntário(a) de Ensino vinculado(a)
            ao Projeto <u>{self.data.project_name}</u>, coordenado pelo(a) 
            Professor(a) <u>{self.data.project_manager}</u>, solicito
            o encerramento da minha participação, a partir de
            <u>{self.data.termination_date}</u>.""",
            styles.termination_text_style,
        )

        self.content.append(date_paragraph)

    def create_terminate_reason_text(self):
        """
        Creates the termination reason text.
        """
        termination_reason_paragraph = Paragraph(
            f"O motivo deste pedido é {self.data.termination_reason}.",
            styles.termination_text_style,
        )
        self.content.append(termination_reason_paragraph)

    def create_agreement_text(self):
        """
        Creates the agreement text.
        """
        agreement_paragraph = Paragraph(
            """ 
            Estou ciente de que um retorno ao Programa de Projetos de Ensino com Participação
            Voluntária é condicionado à existência de vaga, à inexistência de pendências com o
            Projeto e ao atendimento às demais condições do Edital. """,
            styles.termination_text_style,
        )
        self.content.append(agreement_paragraph)

    def create_generation_date_text(self):
        """
        Creates the generation date text of the termination statement
        """
        current_date = datetime.now()
        date_text = current_date.strftime("%d/%m/%Y")
        date_text = date_text.split(sep="/")
        day = date_text[0]
        month = date_text[1]
        month = MONTHS[int(month) - 1]
        year = date_text[2]

        generation_date = Paragraph(
            f"São Paulo, {day} de {month} de {year}.", styles.generation_date_style
        )
        self.content.append(generation_date)
