from datetime import datetime, timezone
from typing import List
from uuid import UUID

from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.expressions import Q
from tortoise.transactions import in_transaction

from application.dto.pagination import Pagination, PaginationResponse
from application.dto.simulation import CostSimulationInput, CostSimulationOutput
from application.dto.vacancy import (
    NotesInput,
    StatusToUpdate,
    VacancyInput,
    VacancyOutput,
)
from domain.interfaces.vacancy_repository import IVacancyRepository
from infra.database.pgdatabase import Status, Vacancy

VacancyPydantic = pydantic_model_creator(Vacancy)


class VacancyRepository(IVacancyRepository):
    """
    Repository for managing vacancies in the database.
    """

    async def get_vacancy_by_id(self, vacancy_id: str) -> VacancyOutput | None:
        found_vacancy = await Vacancy.get_or_none(id=UUID(vacancy_id))

        if found_vacancy:
            found_vacancy_in_database = await VacancyPydantic.from_tortoise_orm(
                found_vacancy
            )
            return VacancyOutput(**found_vacancy_in_database.model_dump())

        return None

    async def get_summary_of_vacancies_by_sector(self, sector: str) -> List[VacancyOutput]:

        if not sector:
            return []

        query = Vacancy.filter(sector__iexact=sector)

        vacancies = await query.all()

        list_response = [
            VacancyOutput(**(await VacancyPydantic.from_tortoise_orm(v)).model_dump())
            for v in vacancies
        ]

        return list_response



    async def create_vacancy(self, vacancy_data: VacancyInput) -> VacancyOutput:
        vacancy_data_as_dict = vacancy_data.model_dump()

        start_date = vacancy_data_as_dict["start_date"]
        end_date = vacancy_data_as_dict["end_date"]

        if not start_date:
            vacancy_data_as_dict["start_date"] = datetime.now(timezone.utc)

        if not end_date:
            vacancy_data_as_dict["end_date"] = datetime.now(timezone.utc)

        async with in_transaction():
            created_vacancy = await Vacancy.create(**vacancy_data_as_dict)
            created_vacancy = await VacancyPydantic.from_tortoise_orm(created_vacancy)
            return VacancyOutput(**created_vacancy.model_dump())

    async def update_vacancy(
        self, vacancy_id: str, vacancy_data: VacancyInput
    ) -> VacancyOutput | None:
        found_vacancy = await Vacancy.get_or_none(id=UUID(vacancy_id))

        if found_vacancy:
            try:
                async with in_transaction():
                    found_vacancy.description = vacancy_data.description
                    found_vacancy.sector = vacancy_data.sector
                    found_vacancy.manager = vacancy_data.manager
                    found_vacancy.salary_expectation = vacancy_data.salary_expectation
                    found_vacancy.urgency = vacancy_data.urgency
                    found_vacancy.status = vacancy_data.status
                    found_vacancy.start_date = vacancy_data.start_date
                    found_vacancy.end_date = vacancy_data.end_date
                    found_vacancy.notes = vacancy_data.notes
                    found_vacancy.updated_at = datetime.now(timezone.utc)

                    await found_vacancy.save()

                    updated_vacancy = await VacancyPydantic.from_tortoise_orm(
                        found_vacancy
                    )
                    return VacancyOutput(**updated_vacancy.model_dump())

            except Exception as e:
                print(e)
                return None

        return None

    async def delete_vacancy(self, vacancy_id: str) -> bool:
        found_vacancy = await Vacancy.get_or_none(id=UUID(vacancy_id))

        if not found_vacancy:
            return False

        try:
            async with in_transaction():
                await found_vacancy.delete()
                return True
        except Exception as e:
            print(e)
            return False

    async def list_vacancies(self, pagination: Pagination) -> PaginationResponse:
        query = Q()

        if pagination.search:
            query |= Q(description__icontains=pagination.search)
            query |= Q(sector__icontains=pagination.search)
            query |= Q(manager__icontains=pagination.search)
            query |= Q(notes__icontains=pagination.search)

        offset = pagination.page * pagination.page_size

        vacancies = (
            await Vacancy.filter(query).offset(offset).limit(pagination.page_size)
        )

        total = await Vacancy.filter(query).count()

        list_response = [
            VacancyOutput(**(await VacancyPydantic.from_tortoise_orm(v)).model_dump())
            for v in vacancies
        ]

        return PaginationResponse(data=list_response, total=total)

    async def edit_vacancy_status(
        self,
        vacancy_id: str,
        vacancy_status: StatusToUpdate,
        optional_notes: NotesInput = None,
    ) -> VacancyOutput | None:
        found_vacancy = await Vacancy.get_or_none(id=UUID(vacancy_id))

        if not found_vacancy:
            return None

        try:
            async with in_transaction():
                found_vacancy.status = vacancy_status.value
                found_vacancy.end_date = datetime.now(timezone.utc)
                found_vacancy.updated_at = datetime.now(timezone.utc)

                if optional_notes:
                    found_vacancy.notes = optional_notes.notes

                await found_vacancy.save()

                updated_vacancy = await VacancyPydantic.from_tortoise_orm(found_vacancy)
                return VacancyOutput(**updated_vacancy.model_dump())

        except Exception as e:
            print(e)
            return None

    async def simulate_vacancy_costs(
        self, costs_simulation_input: CostSimulationInput
    ) -> CostSimulationOutput:
        query = Vacancy.filter(status=Status.in_progress)

        if costs_simulation_input.sector:
            query = query.filter(sector__iexact=costs_simulation_input.sector)

        vacancies = await query.all()

        if not vacancies:
            return CostSimulationOutput(
                period=costs_simulation_input.period,
                sector=costs_simulation_input.sector,
                estimated_cost=0.0,
                message="Não existem vagas em andamento para o filtro selecionado.",
            )

        total = sum(v.salary_expectation for v in vacancies)

        if costs_simulation_input.period == "ANNUAL":
            total *= 12

        return CostSimulationOutput(
            period=costs_simulation_input.period,
            sector=costs_simulation_input.sector,
            estimated_cost=total,
            message=f"Custo total estimado ({costs_simulation_input.period.title()})"
            + (
                f" para o setor '{costs_simulation_input.sector}'"
                if costs_simulation_input.sector
                else ""
            )
            + f": R$ {total:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", "."),
        )
