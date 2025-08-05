import traceback

from application.dto.media import MediaPdfOutput
from application.errors.media import NotFoundPdfMediaToGenerate
from application.interfaces.usecase import UseCase
from domain.interfaces.pdf_generator import IPDFGenerator
from domain.interfaces.vacancy_repository import IVacancyRepository
from web.http_response_schema import HttpResponse, HttpResponseSchema, DefaultFileResponse


class DownloadVacancySummaryUseCase(UseCase):
    """
    Use case to download summary from the system (Implementing the UseCase interface).
    """

    def __init__(self, repository: IVacancyRepository, pdf_adapter: IPDFGenerator):
        """
        Initialize the DownloadVacancySummaryUseCase with a repository.

        :param repository: An instance of IVacancyRepository to interact with vacancy data.
        """

        self.repository = repository
        self.pdf_adapter = pdf_adapter

    async def execute(self, sector: str) -> DefaultFileResponse | HttpResponse:

        try:
             summary = await self.repository.get_summary_of_vacancies_by_sector(sector)

             generated_pdf = self.pdf_adapter.generate_pdf(summary)

             media_pdf_output = MediaPdfOutput(
                 path=generated_pdf,
                 media_type="application/pdf",
                 file_name=f"vacancy_summary_{sector}.pdf"
             )

             return HttpResponseSchema.ok_file_response(media_pdf_output)

        except NotFoundPdfMediaToGenerate as e:
            return HttpResponseSchema.not_found(e)

        except Exception as e:
            traceback.print_exc()
            return HttpResponseSchema.internal_server_error(Exception(e))
