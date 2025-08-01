import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from starlette.responses import JSONResponse

from infra.database.pgdatabase import close_db, init_db
from web.app.health import health_router
from web.app.vacancies import vacancy_router

api_version = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="Recruitment Management API", redirect_slashes=False, lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    validation_message = {
        "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "action": f"{request.method} request to endpoint: {request.url}",
        "error": {
            "type": "Validation Error",
            "exception": exc.__class__.__name__,
            "message": "Invalid request data. Please check the input data. It may be missing required fields or have incorrect types.",
            "details": exc.errors(),
        },
    }

    return JSONResponse(
        validation_message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


app.include_router(vacancy_router, prefix=api_version)
app.include_router(health_router, prefix=api_version)


if __name__ == "__main__":
    app_mode: str = os.getenv("APP_MODE", "development")

    uvicorn.run(
        "entrypoint:app",
        host="0.0.0.0",
        port=8000,
        lifespan="on",
        loop="uvloop",
        reload=True if app_mode == "development" else False,
    )
