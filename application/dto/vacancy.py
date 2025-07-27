from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from infra.database.pgdatabase import Urgency, Status
from uuid import UUID

class VacancyInput(BaseModel):
    """
    Input schema for creating or updating a vacancy.
    """

    description: str = Field(..., description="Description of the vacancy")
    sector: str = Field(..., description="Sector of the vacancy")
    manager: str = Field(..., description="Manager responsible for the vacancy")
    salary_expectation: str = Field(..., description="Expected salary for the vacancy")
    urgency: Urgency = Field(..., description="Urgency level of the vacancy")
    status: Status = Field(..., description="Current status of the vacancy")
    start_date: datetime = Field(..., description="Start date of the vacancy")
    end_date: datetime | None = Field(None, description="End date of the vacancy")
    notes: str | None = Field(None, description="Additional notes for the vacancy")

class VacancyOutput(VacancyInput):
    id: UUID = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat().replace("+00:00", "Z"),
            UUID: lambda v: str(v)
        },
    )