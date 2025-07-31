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

    async def test_create_vacancy_missing_field(self):
        payload = generate_fake_vacancy_data()

        del payload["description"]

        response = await self.http_client.post("/vacancy/", json=payload)
        assert response.status_code == 422

    async def test_create_vacancy_special_characters(self):
        payload = generate_fake_vacancy_data()
        payload["description"] = "'; DROP TABLE users; --"
        payload["notes"] = "<script>alert('xss')</script>"
        payload["manager"] = "José 🌟"

        response = await self.http_client.post("/vacancy/", json=payload)
        assert response.status_code in [422]

    async def test_create_vacancy_invalid_data_types(self):
        payload = generate_fake_vacancy_data()
        payload["salary_expectation"] = "a lot"
        payload["urgency"] = "high"
        payload["start_date"] = 123456

        response = await self.http_client.post("/vacancy/", json=payload)
        assert response.status_code == 422

    async def test_create_vacancy_boundary_values(self):
        payload = generate_fake_vacancy_data()
        payload["description"] = "x" * 1000
        payload["salary_expectation"] = 999999999999
        payload["urgency"] = -1

        response = await self.http_client.post("/vacancy/", json=payload)
        assert response.status_code in [400, 422]

    async def test_create_vacancy_invalid_dates(self):
        payload = generate_fake_vacancy_data()
        payload["start_date"] = "2025-13-40T99:99:99Z"
        payload["end_date"] = "2020-01-01T00:00:00Z"

        response = await self.http_client.post("/vacancy/", json=payload)
        assert response.status_code in [400, 422]

    async def test_simulate_costs_invalid(self):
        payload = {"sector": 123, "period": None}

        response = await self.http_client.post("/vacancy/simulate-costs/", json=payload)
        assert response.status_code == 422

    async def test_invalid_endpoint(self):
        response = await self.http_client.post("/vacancy/nonexistent", json={})
        assert response.status_code == 404

    async def test_create_vacancy_sql_injection_simple(self):
        payload = generate_fake_vacancy_data()
        payload["description"] = "Robert'); DROP TABLE vacancies; --"

        response = await self.http_client.post("/vacancy/", json=payload)
        assert response.status_code == 422

    async def test_create_vacancy_sql_injection_case_insensitive(self):
        payload = generate_fake_vacancy_data()
        payload["description"] = "dRoP TABLE employees"

        response = await self.http_client.post("/vacancy/", json=payload)
        assert response.status_code == 422
