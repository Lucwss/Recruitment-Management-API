from datetime import datetime
from typing import Any, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Pagination(BaseModel):
    """
    Pagination model representing the pagination in the application.
    """

    page: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, le=100, default=10)
    search: Any = Field(None)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={int: lambda v: int(v)},
    )


class PaginationResponse(BaseModel):
    """
    Pagination response model representing the pagination response in the application.
    """

    data: List[Any]
    total: int

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat().replace("+00:00", "Z"),
            UUID: lambda v: str(v),
        },
    )
