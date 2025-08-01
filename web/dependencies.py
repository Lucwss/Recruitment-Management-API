from typing import Annotated

from fastapi import Depends

from adapters.repositories.health_repository import HealthRepository
from adapters.repositories.vacancy_repository import VacancyRepository
from domain.usecases.create_vacancy import CreateVacancyUseCase
from domain.usecases.delete_vacancy import DeleteVacancyUseCase
from domain.usecases.edit_vacancy_status import EditVacancyStatusUseCase
from domain.usecases.get_health_status import GetHealthStatusUseCase
from domain.usecases.get_vacancy import GetVacancyUseCase
from domain.usecases.list_vacancy import ListVacancyUseCase
from domain.usecases.simulate_vacancy_costs import SimulateVacancyCostsUseCase
from domain.usecases.update_vacancy import UpdateVacancyUseCase


def vacancy_repository():
    """
    function that injects the dependencies for VacancyRepository
    """

    return VacancyRepository()

def health_repository():
    """
    function that injects the dependencies for HealthRepository
    """

    return HealthRepository()

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


def simulate_vacancy_costs_use_case(
    repository: Annotated[VacancyRepository, Depends(vacancy_repository)],
) -> SimulateVacancyCostsUseCase:
    """
    function that injects the dependencies for SimulateVacancyCostsUseCase
    """

    return SimulateVacancyCostsUseCase(repository)

def get_health_status_use_case(
    repository: Annotated[HealthRepository, Depends(health_repository)],
) -> GetHealthStatusUseCase:
    """
    function that injects the dependencies for GetHealthStatusUseCase
    """

    return GetHealthStatusUseCase(repository)
