from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Period(StrEnum):
    """
    Enumeration for the period of cost simulation.
    """

    MONTHLY = "MONTHLY"
    ANNUAL = "ANNUAL"


class CostSimulationInput(BaseModel):
    """
    Input model for cost simulation.
    """

    sector: Optional[str] = Field(None, description="Sector for the cost simulation")
    period: Period = Field(
        default="ANNUAL",
        description="Period for the cost simulation, either MONTHLY or ANNUAL",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)


class CostSimulationOutput(CostSimulationInput):
    """
    Output model for cost simulation results.
    """

    estimated_cost: float = Field(..., description="Estimated cost for the simulation")
    message: str = Field(..., description="Message regarding the simulation result")
