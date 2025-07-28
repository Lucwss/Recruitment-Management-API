
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio(loop_scope="class")
class TestPostVacancy:

    http_client: AsyncClient = AsyncClient(base_url="http://0.0.0.0:8000/api/v1")

    async def test_create_vacancy(self):

        payload_input = {
            "description": "Test",
            "sector": "test",
            "manager": "manager",
            "salary_expectation": 5000.00,
            "urgency": 2,
            "status": "IN_PROGRESS",
            "start_date": "2023-10-01T00:00:00Z",
            "end_date": None,
            "notes": None

        }

        response = await self.http_client.post("/vacancy/", json=payload_input)
        assert response.status_code == 201

        json_response: dict = response.json()

        assert "status_code" in json_response
        assert "payload" in json_response

