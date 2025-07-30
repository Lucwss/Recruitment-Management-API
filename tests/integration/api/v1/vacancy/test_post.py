import pytest
from httpx import AsyncClient

from tests.integration.api.v1.vacancy.fake_data import (
    generate_fake_data_simulation_input,
    generate_fake_vacancy_data,
)


@pytest.mark.asyncio(loop_scope="class")
class TestPostVacancy:
    """
    Test class for creating a vacancy and simulating costs in the API.
    """

    http_client: AsyncClient = AsyncClient(base_url="http://0.0.0.0:8000/api/v1")

    async def test_create_vacancy(self):
        payload_input = generate_fake_vacancy_data()

        response = await self.http_client.post("/vacancy/", json=payload_input)
        assert response.status_code == 201

        json_response: dict = response.json()

        assert "status_code" in json_response
        assert "payload" in json_response

        payload = json_response["payload"]

        required_fields = [
            "id",
            "description",
            "sector",
            "manager",
            "salary_expectation",
            "urgency",
            "status",
            "start_date",
            "end_date",
            "notes",
        ]
        for field in required_fields:
            assert field in payload

    async def test_simulate_costs(self):
        payload_input = generate_fake_data_simulation_input()

        response = await self.http_client.post(
            "/vacancy/simulate-costs/", json=payload_input
        )
        assert response.status_code == 200

        json_response: dict = response.json()

        assert "status_code" in json_response
        assert "payload" in json_response
