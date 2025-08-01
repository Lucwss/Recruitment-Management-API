from tortoise import Tortoise
import os
from application.dto.health import HealthStatusOutput
from domain.interfaces.health_repository import IHealthRepository
from datetime import datetime, timezone

class HealthRepository(IHealthRepository):
    """
    Repository for managing health system connected in the database.
    """

    async def check_database_health(self) -> HealthStatusOutput:
        updated_at = datetime.now(timezone.utc)

        conn = Tortoise.get_connection("default")

        result_server_version = await conn.execute_query_dict("SHOW server_version;")
        result_max_connections = await conn.execute_query_dict("SHOW max_connections;")

        database_name = os.getenv("POSTGRES_DB")

        result_opened_connections = await conn.execute_query_dict(
            f"SELECT count(*)::int as open_conn FROM pg_stat_activity WHERE datname = '{database_name}';"
        )

        server_version = result_server_version[0]["server_version"]
        max_connections = int(result_max_connections[0]["max_connections"])
        opened_connections = result_opened_connections[0]["open_conn"]

        check_result = {
            "updated_at": str(updated_at),
            "dependencies": {
                "database": {
                    "name": "PostgreSQL",
                    "database_name": database_name,
                    "version": server_version,
                    "max_connections": max_connections,
                    "opened_connections": opened_connections,
                }
            },
        }

        return HealthStatusOutput(**check_result)