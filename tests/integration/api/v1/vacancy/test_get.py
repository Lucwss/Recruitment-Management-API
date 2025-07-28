import pytest
from httpx import AsyncClient
from faker import Faker
import random

from tests.integration.api.v1.vacancy.fake_data import generate_fake_vacancy_data


@pytest.mark.asyncio(loop_scope="class")
class TestGetVacancy:
    http_client: AsyncClient = AsyncClient(base_url="http://0.0.0.0:8000/api/v1")

    async def test_get_vacancy(self):
        payload_input = generate_fake_vacancy_data()

        response = await self.http_client.post("/vacancy/", json=payload_input)
        assert response.status_code == 201

        json_response: dict = response.json()

        assert "status_code" in json_response
        assert "payload" in json_response

        payload = json_response["payload"]

        assert "id" in payload

        vacancy_identification = payload["id"]

        response = await self.http_client.get(f"/vacancy/{vacancy_identification}")
        assert response.status_code == 200

        json_response: dict = response.json()

        assert "status_code" in json_response
        assert "payload" in json_response

        payload = json_response["payload"]

        assert "id" in payload
        assert "description" in payload
        assert "sector" in payload
        assert "manager" in payload
        assert "salary_expectation" in payload
        assert "urgency" in payload
        assert "status" in payload
        assert "start_date" in payload
        assert "end_date" in payload
        assert "notes" in payload

