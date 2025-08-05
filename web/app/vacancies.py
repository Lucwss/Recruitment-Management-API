from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse, FileResponse

from application.dto.simulation import CostSimulationInput
from application.dto.vacancy import NotesInput, StatusToUpdate, VacancyInput
from domain.usecases.create_vacancy import CreateVacancyUseCase
from domain.usecases.delete_vacancy import DeleteVacancyUseCase
from domain.usecases.download_vacancy_summary import DownloadVacancySummaryUseCase
from domain.usecases.edit_vacancy_status import EditVacancyStatusUseCase
from domain.usecases.get_vacancy import GetVacancyUseCase
from domain.usecases.list_vacancy import ListVacancyUseCase
from domain.usecases.simulate_vacancy_costs import SimulateVacancyCostsUseCase
from domain.usecases.update_vacancy import UpdateVacancyUseCase
from web.dependencies import (
    create_vacancy_use_case,
    delete_vacancy_use_case,
    edit_vacancy_status_use_case,
    get_vacancy_use_case,
    list_vacancy_use_case,
    simulate_vacancy_costs_use_case,
    update_vacancy_use_case, download_vacancy_summary_costs_use_case,
)
from web.http_response_schema import HttpResponse

vacancy_router = APIRouter(prefix="/vacancy", tags=["Vacancies"])


@vacancy_router.post("/", summary="Route for creation of a vacancy.")
async def create_vacancy(
    vacancy_input: Annotated[VacancyInput, Body(...)],
    use_case: Annotated[CreateVacancyUseCase, Depends(create_vacancy_use_case)],
):
    response = await use_case.execute(vacancy_data_input=vacancy_input)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)


@vacancy_router.get("/{vacancy_id}/", summary="Route for getting a vacancy by ID.")
async def get_vacancy(
    vacancy_id: Annotated[str, Path(...)],
    use_case: Annotated[GetVacancyUseCase, Depends(get_vacancy_use_case)],
):
    response = await use_case.execute(vacancy_id=vacancy_id)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)


@vacancy_router.delete("/{vacancy_id}/", summary="Route for deleting a vacancy by ID.")
async def delete_vacancy(
    vacancy_id: Annotated[str, Path(...)],
    use_case: Annotated[DeleteVacancyUseCase, Depends(delete_vacancy_use_case)],
):
    response = await use_case.execute(vacancy_id=vacancy_id)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)


@vacancy_router.put("/{vacancy_id}/", summary="Route for updating a vacancy by ID.")
async def update_vacancy(
    vacancy_id: Annotated[str, Path(...)],
    vacancy_input: Annotated[VacancyInput, Body(...)],
    use_case: Annotated[UpdateVacancyUseCase, Depends(update_vacancy_use_case)],
):
    response = await use_case.execute(
        vacancy_id=vacancy_id, vacancy_data_input=vacancy_input
    )
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)


@vacancy_router.get("/", summary="Route for getting all vacancies.")
async def list_vacancies(
    use_case: Annotated[ListVacancyUseCase, Depends(list_vacancy_use_case)],
    search: Any = Query(None),
    page: int = Query(default=0, gte=0),
    page_size: int = Query(default=10, le=100, gt=0),
):
    response = await use_case.execute(page=page, page_size=page_size, search=search)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)

@vacancy_router.get("/summary/download/", summary="Route for downloading a vacancy summary.")
async def download_vacancy_summary(
        sector: Annotated[str, Query(...)],
        use_case: Annotated[DownloadVacancySummaryUseCase, Depends(download_vacancy_summary_costs_use_case)]
):
    response = await use_case.execute(sector=sector)

    if isinstance(response, HttpResponse):
        return JSONResponse(content=response.model_dump(), status_code=response.status_code)

    return FileResponse(
        path=response.media.path,
        media_type=response.media.media_type,
        filename=response.media.file_name
    )


@vacancy_router.patch(
    "/{vacancy_id}/status/", summary="Route for editing a vacancy status."
)
async def update_vacancy_status(
    vacancy_id: Annotated[str, Path(...)],
    vacancy_status: Annotated[StatusToUpdate, Query(...)],
    use_case: Annotated[
        EditVacancyStatusUseCase, Depends(edit_vacancy_status_use_case)
    ],
    notes: NotesInput = Body(default=None),
):
    response = await use_case.execute(
        vacancy_id=vacancy_id, vacancy_status=vacancy_status, optional_notes=notes
    )
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)


@vacancy_router.post("/simulate-costs/", summary="Route for creation of a vacancy.")
async def simulate_in_progress_vacancy(
    cost_simulation_input: Annotated[CostSimulationInput, Body(...)],
    use_case: Annotated[
        SimulateVacancyCostsUseCase, Depends(simulate_vacancy_costs_use_case)
    ],
):
    response = await use_case.execute(costs_simulation_input=cost_simulation_input)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)
