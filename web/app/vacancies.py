from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse
from typing import Annotated

from application.dto.vacancy import VacancyInput
from domain.usecases.create_vacancy import CreateVacancyUseCase
from domain.usecases.delete_vacancy import DeleteVacancyUseCase
from domain.usecases.get_vacancy import GetVacancyUseCase
from web.dependencies import create_vacancy_use_case, get_vacancy_use_case, delete_vacancy_use_case

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

@vacancy_router.get("/{vacancy_id}", summary='Route for getting a vacancy by ID.')
async def get_vacancy(
        vacancy_id: Annotated[str, Path(...)],
        use_case: Annotated[GetVacancyUseCase, Depends(get_vacancy_use_case)]
):
    response = await use_case.execute(vacancy_id=vacancy_id)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)

@vacancy_router.delete("/{vacancy_id}", summary='Route for deleting a vacancy by ID.')
async def delete_vacancy(
        vacancy_id: Annotated[str, Path(...)],
        use_case: Annotated[DeleteVacancyUseCase, Depends(delete_vacancy_use_case)]
):
    response = await use_case.execute(vacancy_id=vacancy_id)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)