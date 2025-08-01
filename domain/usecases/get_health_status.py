import traceback
from pprint import pprint

from application.dto.health import HealthStatusOutput
from application.interfaces.usecase import UseCase
from domain.interfaces.health_repository import IHealthRepository
from web.http_response_schema import HttpResponse, HttpResponseSchema


class GetHealthStatusUseCase(UseCase):
    """
    Use case for getting health status from system (Implementing the UseCase interface).
    """

    def __init__(self, repository: IHealthRepository):
        """
        Initialize the GetHealthStatusUseCase with a repository.

        :param repository: An instance of IVacancyRepository to interact with vacancy data.
        """

        self.repository = repository

    async def execute(self) -> HttpResponse:
        try:
            result: HealthStatusOutput = await self.repository.check_database_health()
            result_as_dict = result.model_dump()

            pprint(result_as_dict)

            return HttpResponseSchema.ok(result_as_dict)
        except Exception as e:
            traceback.print_exc()
            return HttpResponseSchema.internal_server_error(Exception(e))
