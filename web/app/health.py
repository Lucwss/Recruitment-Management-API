from fastapi import APIRouter
from starlette.responses import JSONResponse

health_router = APIRouter(prefix="/health", tags=["Health Check"])

@health_router.get("/status/", summary="Route for checking system status.")
async def get_status(
):
    ...

