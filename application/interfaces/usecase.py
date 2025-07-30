from abc import ABC, abstractmethod


class UseCase(ABC):
    """
    Interface for UseCase main methods.
    """

    @abstractmethod
    async def execute(self, *args, **kwargs):
        """Main method for the execution of use case."""
        raise NotImplemented()
