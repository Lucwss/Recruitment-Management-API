import json
import traceback

from application.dto.vacancy import VacancyInput, VacancyOutput
from application.interfaces.usecase import UseCase
from domain.interfaces.vacancy_repository import IVacancyRepository
from web.http_response_schema import HttpResponse, HttpResponseSchema


class CreateVacancyUseCase(UseCase):
    """
    Use case for creating a vacancy in the system (Implementing the UseCase interface).
    """

    def __init__(self, repository: IVacancyRepository):
        """
        Initialize the CreateVacancyUseCase with a repository.

        :param repository: An instance of IVacancyRepository to interact with vacancy data.
        """

        self.repository = repository

    async def execute(self, vacancy_data_input: VacancyInput) -> HttpResponse:

        try:
            created_vacancy: VacancyOutput = await self.repository.create_vacancy(
                vacancy_data_input
            )
            created_vacancy_dict = json.loads(created_vacancy.model_dump_json())
            return HttpResponseSchema.created(created_vacancy_dict)
        except Exception as e:
            traceback.print_exc()
            return HttpResponseSchema.internal_server_error(Exception(e))
