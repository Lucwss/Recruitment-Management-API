from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class Period(StrEnum):
    MONTHLY = "MONTHLY"
    ANNUAL = "ANNUAL"

class CostSimulationInput(BaseModel):
    sector: Optional[str] = Field(None, description="Sector for the cost simulation")
    period: Period = Field(default="ANNUAL", description="Period for the cost simulation, either MONTHLY or ANNUAL")

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )


class CostSimulationOutput(CostSimulationInput):
    estimated_cost: float = Field(..., description="Estimated cost for the simulation")
    message: str = Field(..., description="Message regarding the simulation result")