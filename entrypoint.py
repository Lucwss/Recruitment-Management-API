from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

from infra.database.pgdatabase import init_db

api_version = '/api/v1'

app = FastAPI(
    title="Recruitment Management API",
    redirect_slashes=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def startup() -> None:
    init_db(app)

app.add_event_handler('startup', startup)


if __name__ == "__main__":
    app_mode: str = os.getenv("APP_MODE", "development")

    uvicorn.run(
        "entrypoint:app",
        host="0.0.0.0",
        port=8000,
        lifespan="on",
        loop="uvloop",
        reload=True if app_mode == "development" else False
    )

