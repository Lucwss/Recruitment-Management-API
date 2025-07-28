import json
import traceback

from application.dto.vacancy import VacancyInput, VacancyOutput
from web.http_response_schema import HttpResponse

from application.interfaces.usecase import UseCase
from domain.interfaces.vacancy_repository import IVacancyRepository
from web.http_response_schema import HttpResponseSchema


class DeleteVacancyUseCase(UseCase):

    """
    Use case for deleting a vacancy by its id in the system (Implementing the UseCase interface).
    """

    def __init__(self, repository: IVacancyRepository):
        """
        Initialize the DeleteVacancyUseCase with a repository.

        :param repository: An instance of IVacancyRepository to interact with vacancy data.
        """

        self.repository = repository


    async def execute(self, vacancy_id: str) -> HttpResponse:

        try:
            vacancy_in_system = await self.repository.get_vacancy_by_id(vacancy_id)

            if not vacancy_in_system:
                return HttpResponseSchema.not_found(Exception(f"Vacancy not found for id: {vacancy_id}."))

            deleted_vacancy: bool = await self.repository.delete_vacancy(vacancy_id)

            if not deleted_vacancy:
                return HttpResponseSchema.bad_request(Exception(f"It wasn`t possible to delete the vacancy for id {vacancy_id}."))

            response_for_vacancy_deletion = {
                "message": "Vacancy deleted successfully."
            }

            return HttpResponseSchema.ok(response_for_vacancy_deletion)
        except Exception as e:
            traceback.print_exc()
            return HttpResponseSchema.internal_server_error(Exception(e))