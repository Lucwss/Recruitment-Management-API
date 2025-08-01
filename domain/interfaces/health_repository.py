from abc import ABC, abstractmethod

from application.dto.health import HealthStatusOutput


class IHealthRepository(ABC):
    """
    Interface responsible for HealthRepository methods.
    """

    @abstractmethod
    async def check_database_health(self) -> HealthStatusOutput:
        """Get the health status of the system."""
        raise NotImplementedError()
