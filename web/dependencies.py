from typing import Annotated

from fastapi import Depends

from adapters.repositories.vacancy_repository import VacancyRepository
from domain.usecases.create_vacancy import CreateVacancyUseCase
from domain.usecases.delete_vacancy import DeleteVacancyUseCase
from domain.usecases.get_vacancy import GetVacancyUseCase
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

def get_vacancy_use_case(
        repository: Annotated[VacancyRepository, Depends(vacancy_repository)],
) -> GetVacancyUseCase:
    """
    function that injects the dependencies for GetVacancyUseCase
    """

    return GetVacancyUseCase(repository)

def delete_vacancy_use_case(
        repository: Annotated[VacancyRepository, Depends(vacancy_repository)],
) -> DeleteVacancyUseCase:
    """
    function that injects the dependencies for DeleteVacancyUseCase
    """

    return DeleteVacancyUseCase(repository)