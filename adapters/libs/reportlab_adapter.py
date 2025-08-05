from typing import List

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from application.dto.vacancy import VacancyOutput
from application.errors.media import NotFoundPdfMediaToGenerate
from domain.interfaces.pdf_generator import IPDFGenerator

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4


class ReportLabAdapter(IPDFGenerator):
    """
    Adapter for generating PDF reports using ReportLab.
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.output_filename = "report.pdf"

    def generate_pdf(self, vacancies: List[VacancyOutput]) -> str:
        total_salary = 0

        if len(vacancies) == 0:
            raise NotFoundPdfMediaToGenerate("No vacancies to generate report.")

        document_template = SimpleDocTemplate(self.output_filename, pagesize=A4)
        elements = []

        elements.append(Paragraph("Relatório de gastos", self.styles["Title"]))
        elements.append(Spacer(1, 12))

        table_data = [[
            "Descrição", "Setor", "Gerente", "Expectativa de salário"
        ]]

        for vacancy in vacancies:
            table_data.append([
                vacancy.description,
                vacancy.sector,
                vacancy.manager,
                f"${vacancy.salary_expectation:.2f}",
            ])
            total_salary += vacancy.salary_expectation

        table_data.append(["Total", "", "", f"${total_salary:.2f}"])
        table = Table(table_data, colWidths=[180, 80, 160, 135])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (5, 1), (-1, -1), "RIGHT"),
            ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
        ]))

        elements.append(table)
        document_template.build(elements)

        return self.output_filename