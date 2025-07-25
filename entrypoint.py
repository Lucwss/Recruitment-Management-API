from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

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

