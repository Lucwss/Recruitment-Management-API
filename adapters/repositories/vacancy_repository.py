from tortoise.contrib.pydantic import pydantic_model_creator

from application.dto.vacancy import VacancyInput, VacancyOutput
from domain.interfaces.vacancy_repository import IVacancyRepository
from infra.database.pgdatabase import Vacancy
from tortoise.transactions import in_transaction


VacancyPydantic = pydantic_model_creator(Vacancy)

class VacancyRepository(IVacancyRepository):

    async def get_vacancy_by_id(self, vacancy_id: str) -> dict:
        pass

    async def create_vacancy(self, vacancy_data: VacancyInput) -> VacancyOutput:
        vacancy_data_as_dict = vacancy_data.model_dump()

        async with in_transaction():
            created_vacation = await Vacancy.create(**vacancy_data_as_dict)
            created_vacation = await VacancyPydantic.from_tortoise_orm(created_vacation)
            return VacancyOutput(**created_vacation.model_dump())



    async def update_vacancy(self, vacancy_id: str, vacancy_data: dict) -> dict:
        pass

    async def delete_vacancy(self, vacancy_id: str) -> None:
        pass

    async def list_vacancies(self, filters: dict = None) -> list:
        pass