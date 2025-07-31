import json
import traceback

from application.dto.vacancy import VacancyOutput
from application.interfaces.usecase import UseCase
from domain.interfaces.vacancy_repository import IVacancyRepository
from utils.database_utils import is_valid_uuid
from web.http_response_schema import HttpResponse, HttpResponseSchema


class GetVacancyUseCase(UseCase):
    """
    Use case for finding a vacancy by its id in the system (Implementing the UseCase interface).
    """

    def __init__(self, repository: IVacancyRepository):
        """
        Initialize the GetVacancyUseCase with a repository.

        :param repository: An instance of IVacancyRepository to interact with vacancy data.
        """

        self.repository = repository

    async def execute(self, vacancy_id: str) -> HttpResponse:

        try:
            is_valid_uuid_structure: bool = is_valid_uuid(vacancy_id)

            if not is_valid_uuid_structure:
                return HttpResponseSchema.bad_request(
                    Exception(f"Invalid UUID structure for id: {vacancy_id}.")
                )

            found_vacancy: VacancyOutput | None = (
                await self.repository.get_vacancy_by_id(vacancy_id)
            )

            if not found_vacancy:
                return HttpResponseSchema.not_found(
                    Exception(f"Vacancy not found for id: {vacancy_id}.")
                )

            found_vacancy_dict = json.loads(found_vacancy.model_dump_json())
            return HttpResponseSchema.ok(found_vacancy_dict)
        except Exception as e:
            traceback.print_exc()
            return HttpResponseSchema.internal_server_error(Exception(e))
