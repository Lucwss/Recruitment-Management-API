import json
import traceback
from typing import Any

from application.dto.pagination import Pagination, PaginationResponse
from web.http_response_schema import HttpResponse

from application.interfaces.usecase import UseCase
from domain.interfaces.vacancy_repository import IVacancyRepository
from web.http_response_schema import HttpResponseSchema


class ListVacancyUseCase(UseCase):

    """
    Use case to list all vacancies in the system (Implementing the UseCase interface).
    """

    def __init__(self, repository: IVacancyRepository):
        """
        Initialize the ListVacancyUseCase with a repository.

        :param repository: An instance of IVacancyRepository to interact with vacancy data.
        """

        self.repository = repository


    async def execute(self, page: int, page_size: int, search: Any) -> HttpResponse:

        try:
            pagination: Pagination = Pagination(page=page, page_size=page_size, search=search)
            list_of_vacancies: PaginationResponse = await self.repository.list_vacancies(pagination)
            list_of_vacancies_as_dict = json.loads(list_of_vacancies.model_dump_json())
            return HttpResponseSchema.ok(list_of_vacancies_as_dict)

        except Exception as e:
            traceback.print_exc()
            return HttpResponseSchema.internal_server_error(Exception(e))