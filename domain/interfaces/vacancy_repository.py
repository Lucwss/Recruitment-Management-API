from abc import ABC, abstractmethod

from application.dto.vacancy import VacancyInput, VacancyOutput


class IVacancyRepository(ABC):
    """
    Interface responsible for VacancyRepository methods.
    """

    @abstractmethod
    async def get_vacancy_by_id(self, vacancy_id: str) -> VacancyOutput | None:
        """ Get a vacancy by its ID. """
        raise NotImplementedError()

    @abstractmethod
    async def create_vacancy(self, vacancy_data: VacancyInput) -> VacancyOutput:
        """ Create a new vacancy. """
        raise NotImplementedError()

    @abstractmethod
    async def update_vacancy(self, vacancy_id: str, vacancy_data: dict) -> dict:
        """ Update an existing vacancy. """
        raise NotImplementedError()

    @abstractmethod
    async def delete_vacancy(self, vacancy_id: str) -> None:
        """ Delete a vacancy by its ID. """
        raise NotImplementedError()

    @abstractmethod
    async def list_vacancies(self, filters: dict = None) -> list:
        """ List all vacancies with optional filters. """
        raise NotImplementedError()

