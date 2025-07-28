from typing import Any
from uuid import UUID

from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.expressions import Q

from application.dto.pagination import Pagination, PaginationResponse
from application.dto.vacancy import VacancyInput, VacancyOutput
from domain.interfaces.vacancy_repository import IVacancyRepository
from infra.database.pgdatabase import Vacancy
from tortoise.transactions import in_transaction


VacancyPydantic = pydantic_model_creator(Vacancy)

class VacancyRepository(IVacancyRepository):

    async def get_vacancy_by_id(self, vacancy_id: str) -> VacancyOutput | None:
        found_vacancy = await Vacancy.get_or_none(id=UUID(vacancy_id))

        if found_vacancy:
            found_vacancy_in_database = await VacancyPydantic.from_tortoise_orm(found_vacancy)
            return VacancyOutput(**found_vacancy_in_database.model_dump())

        return None

    async def create_vacancy(self, vacancy_data: VacancyInput) -> VacancyOutput:
        vacancy_data_as_dict = vacancy_data.model_dump()

        async with in_transaction():
            created_vacancy = await Vacancy.create(**vacancy_data_as_dict)
            created_vacancy = await VacancyPydantic.from_tortoise_orm(created_vacancy)
            return VacancyOutput(**created_vacancy.model_dump())



    async def update_vacancy(self, vacancy_id: str, vacancy_data: VacancyInput) -> VacancyOutput | None:
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

                    await found_vacancy.save()

                    updated_vacancy = await VacancyPydantic.from_tortoise_orm(found_vacancy)
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

        total = await Vacancy.filter(query).count()

        offset = (pagination.page - 1) * pagination.page_size

        vacancies = await Vacancy.filter(query).offset(offset).limit(pagination.page_size)

        list_response = [
            VacancyOutput(**(await VacancyPydantic.from_tortoise_orm(v)).model_dump())
            for v in vacancies
        ]

        return PaginationResponse(
            data=list_response,
            total=total
        )
