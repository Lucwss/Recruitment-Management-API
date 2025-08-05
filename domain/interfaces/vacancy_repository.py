from abc import ABC, abstractmethod
from typing import List

from application.dto.pagination import Pagination, PaginationResponse
from application.dto.simulation import CostSimulationInput, CostSimulationOutput
from application.dto.vacancy import (
    NotesInput,
    StatusToUpdate,
    VacancyInput,
    VacancyOutput,
)


class IVacancyRepository(ABC):
    """
    Interface responsible for VacancyRepository methods.
    """

    @abstractmethod
    async def get_vacancy_by_id(self, vacancy_id: str) -> VacancyOutput | None:
        """Get a vacancy by its ID."""
        raise NotImplementedError()

    @abstractmethod
    async def create_vacancy(self, vacancy_data: VacancyInput) -> VacancyOutput:
        """Create a new vacancy."""
        raise NotImplementedError()

    @abstractmethod
    async def update_vacancy(
        self, vacancy_id: str, vacancy_data: VacancyInput
    ) -> VacancyOutput | None:
        """Update an existing vacancy."""
        raise NotImplementedError()

    @abstractmethod
    async def delete_vacancy(self, vacancy_id: str) -> bool:
        """Delete a vacancy by its ID."""
        raise NotImplementedError()

    @abstractmethod
    async def list_vacancies(self, pagination: Pagination) -> PaginationResponse:
        """List all vacancies with optional filters."""
        raise NotImplementedError()

    @abstractmethod
    async def edit_vacancy_status(
        self,
        vacancy_id: str,
        vacancy_status: StatusToUpdate,
        optional_notes: NotesInput = None,
    ) -> VacancyOutput | None:
        """Edit an existing vacancy status."""
        raise NotImplementedError()

    @abstractmethod
    async def get_summary_of_vacancies_by_sector(
        self, sector: str
    ) -> List[VacancyOutput]:
        """Get a summary of vacancies."""
        raise NotImplementedError()

    @abstractmethod
    async def simulate_vacancy_costs(
        self, costs_simulation_input: CostSimulationInput
    ) -> CostSimulationOutput:
        """Simulate costs for all vacancies."""
        raise NotImplementedError()
