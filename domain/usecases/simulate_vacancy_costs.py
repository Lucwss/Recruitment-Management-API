import json
import traceback

from application.dto.simulation import CostSimulationInput, Period
from application.dto.vacancy import VacancyInput, VacancyOutput
from web.http_response_schema import HttpResponse

from application.interfaces.usecase import UseCase
from domain.interfaces.vacancy_repository import IVacancyRepository
from web.http_response_schema import HttpResponseSchema


class SimulateVacancyCostsUseCase(UseCase):

    """
    Use case for simulating all vacancies costs in the system (Implementing the UseCase interface).
    """

    def __init__(self, repository: IVacancyRepository):
        """
        Initialize the SimulateVacancyCostsUseCase with a repository.

        :param repository: An instance of IVacancyRepository to interact with vacancy data.
        """

        self.repository = repository


    async def execute(self, costs_simulation_input: CostSimulationInput) -> HttpResponse:

        try:
            simulated_total = await self.repository.simulate_vacancy_costs(costs_simulation_input)
            simulated_total = simulated_total.model_dump()

            return HttpResponseSchema.ok(simulated_total)
        except Exception as e:
            traceback.print_exc()
            return HttpResponseSchema.internal_server_error(Exception(e))