from uuid import UUID

from tortoise.contrib.pydantic import pydantic_model_creator

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



    async def update_vacancy(self, vacancy_id: str, vacancy_data: dict) -> dict:
        pass

    async def delete_vacancy(self, vacancy_id: str) -> None:
        pass

    async def list_vacancies(self, filters: dict = None) -> list:
        pass