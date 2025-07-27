from fastapi import FastAPI
from tortoise.models import Model
from tortoise import fields
from uuid import UUID
from datetime import datetime
from enum import IntEnum, StrEnum
import os
from tortoise.contrib.fastapi import register_tortoise

class Urgency(IntEnum):
    low = 0
    medium = 1
    high = 2

class Status(StrEnum):
    in_progress = "IN_PROGRESS"
    finished = "FINISHED"
    canceled = "CANCELED"

class Vacancy(Model):
    id: UUID = fields.UUIDField(primary_key=True)
    description: str = fields.CharField(max_length=255)
    sector: str = fields.CharField(max_length=255)
    manager: str = fields.CharField(max_length=255)
    salary_expectation: str = fields.CharField(max_length=255)
    urgency: Urgency = fields.IntEnumField(Urgency, "Urgency options")
    status: Status = fields.CharEnumField(Status, "Status options")
    start_date: datetime = fields.DatetimeField(auto_now=True)
    end_date: datetime = fields.DatetimeField(auto_now=True, null=True)
    notes: str = fields.CharField(max_length=255, null=True)


TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": os.getenv("POSTGRES_HOST", "0.0.0.0"),
                "port": os.getenv("POSTGRES_PORT", 5432),
                "user": os.getenv("POSTGRES_USER", "localuser"),
                "password": os.getenv("POSTGRES_PASSWORD", "localpassword"),
                "database": os.getenv("POSTGRES_DB", "recruitment-database")
            }
        }
    },
    "apps": {
        "models": {
            "default_connection": "default",
            "models": [
                "infra.database.pgdatabase",
                "aerich.models"
            ],
        }
    }
}

def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=os.environ.get("POSTGRES_URL"),
        modules={"models": ["infra.database.pgdatabase"]},
        generate_schemas=True,
        add_exception_handlers=True,
)