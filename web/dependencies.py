from typing import Annotated

from fastapi import Depends

from adapters.repositories.vacancy_repository import VacancyRepository
from domain.usecases.create_vacancy import CreateVacancyUseCase
from infra.database.pgdatabase import Vacancy


def vacancy_repository():
    """
    function that injects the dependencies for VacancyRepository
    """

    return VacancyRepository()

def create_vacancy_use_case(
        repository: Annotated[VacancyRepository, Depends(vacancy_repository)],
) -> CreateVacancyUseCase:
    """
    function that injects the dependencies for CreateVacancyUseCase
    """

    return CreateVacancyUseCase(repository)
