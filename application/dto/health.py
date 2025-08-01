from pydantic import BaseModel
from datetime import datetime

class DatabaseStatus(BaseModel):
    """
    Represents the status of the database connection.
    """

    name: str
    database_name: str
    version: float
    max_connections: int
    opened_connections: int

class Dependency(BaseModel):
    """
    Represents a dependency in the health status of the application.
    """

    database: DatabaseStatus

class HealthStatusOutput(BaseModel):
    """
    Health status of the application.
    """

    dependencies: Dependency
    updated_at: str
