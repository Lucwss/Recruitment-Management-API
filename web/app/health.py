from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from domain.usecases.get_health_status import GetHealthStatusUseCase
from web.dependencies import get_health_status_use_case

health_router = APIRouter(prefix="/health", tags=["Health Check"])


@health_router.get("/status/", summary="Route for checking system status.")
async def get_status(
    use_case: Annotated[GetHealthStatusUseCase, Depends(get_health_status_use_case)],
):
    response = await use_case.execute()
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)
