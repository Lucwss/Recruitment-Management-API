from typing import Annotated

from fastapi import Depends

from adapters.repositories.vacancy_repository import VacancyRepository
from domain.usecases.create_vacancy import CreateVacancyUseCase
from domain.usecases.delete_vacancy import DeleteVacancyUseCase
from domain.usecases.edit_vacancy_status import EditVacancyStatusUseCase
from domain.usecases.get_vacancy import GetVacancyUseCase
from domain.usecases.list_vacancy import ListVacancyUseCase
from domain.usecases.update_vacancy import UpdateVacancyUseCase
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

def update_vacancy_use_case(
        repository: Annotated[VacancyRepository, Depends(vacancy_repository)],
) -> UpdateVacancyUseCase:
    """
    function that injects the dependencies for UpdateVacancyUseCase
    """

    return UpdateVacancyUseCase(repository)

def list_vacancy_use_case(
        repository: Annotated[VacancyRepository, Depends(vacancy_repository)],
) -> ListVacancyUseCase:
    """
    function that injects the dependencies for ListVacancyUseCase
    """

    return ListVacancyUseCase(repository)

def edit_vacancy_status_use_case(
        repository: Annotated[VacancyRepository, Depends(vacancy_repository)],
) -> EditVacancyStatusUseCase:
    """
    function that injects the dependencies for EditVacancyStatusUseCase
    """

    return EditVacancyStatusUseCase(repository)