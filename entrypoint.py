import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infra.database.pgdatabase import close_db, init_db
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

app.include_router(vacancy_router, prefix=api_version)


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
