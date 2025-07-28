from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from typing import Annotated

from application.dto.vacancy import VacancyInput
from domain.usecases.create_vacancy import CreateVacancyUseCase
from web.dependencies import create_vacancy_use_case

vacancy_router = APIRouter(
    prefix="/vacancy",
    tags=["Vacancies"]
)

@vacancy_router.post("/", summary='Route for creation of a vacancy.')
async def create_vacancy(
        vacancy_input: Annotated[VacancyInput, Body(...)],
        use_case: Annotated[CreateVacancyUseCase, Depends(create_vacancy_use_case)]
):
    response = await use_case.execute(vacancy_data_input=vacancy_input)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)