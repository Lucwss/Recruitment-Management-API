import os
from datetime import datetime
from enum import IntEnum, StrEnum
from typing import Optional
from uuid import UUID

from tortoise import Tortoise, fields
from tortoise.models import Model


class Urgency(IntEnum):
    """
    Enumeration for the urgency level of a vacancy.
    """

    low = 0
    medium = 1
    high = 2


class Status(StrEnum):
    """
    Enumeration for the status of a vacancy.
    """

    in_progress = "IN_PROGRESS"
    finished = "FINISHED"
    canceled = "CANCELED"


class Vacancy(Model):
    """
    Model representing a vacancy in the recruitment system.
    """

    id: UUID = fields.UUIDField(primary_key=True)
    description: str = fields.CharField(max_length=255)
    sector: str = fields.CharField(max_length=255)
    manager: str = fields.CharField(max_length=255)
    salary_expectation: float = fields.FloatField()
    urgency: Urgency = fields.IntEnumField(Urgency, "Urgency options")
    status: Status = fields.CharEnumField(Status, "Status options")
    start_date: datetime = fields.DatetimeField()
    end_date: Optional[datetime] = fields.DatetimeField(null=True)
    notes: Optional[str] = fields.CharField(max_length=255, null=True)
    created_at: datetime = fields.DatetimeField(auto_now=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True)


TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": os.getenv("POSTGRES_HOST", "0.0.0.0"),
                "port": os.getenv("POSTGRES_PORT", 5432),
                "user": os.getenv("POSTGRES_USER", "localuser"),
                "password": os.getenv("POSTGRES_PASSWORD", "localpassword"),
                "database": os.getenv("POSTGRES_DB", "recruitment-database"),
            },
        }
    },
    "apps": {
        "models": {
            "default_connection": "default",
            "models": ["infra.database.pgdatabase", "aerich.models"],
        }
    },
}


async def init_db() -> None:
    await Tortoise.init(config=TORTOISE_ORM)


async def close_db() -> None:
    await Tortoise.close_connections()
