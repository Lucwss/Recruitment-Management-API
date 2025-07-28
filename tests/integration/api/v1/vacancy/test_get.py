import pytest
import pytest_asyncio
from httpx import AsyncClient
from faker import Faker
import random

from tests.integration.api.v1.vacancy.fake_data import generate_fake_vacancy_data

@pytest_asyncio.fixture(loop_scope="class", autouse=True)
async def setup_vacancy(request):
    """
        Runs once before all tests in the class.
        Creates a test vacancy and stores it in the class.
    """

    http_client = AsyncClient(base_url="http://0.0.0.0:8000/api/v1")
    request.cls.http_client = http_client

    payload_input = generate_fake_vacancy_data()
    response = await http_client.post("/vacancy/", json=payload_input)
    assert response.status_code == 201

    response_data = response.json()
    request.cls.vacancy_id = response_data["payload"]["id"]

    yield

    await http_client.aclose()

@pytest.mark.asyncio(loop_scope="class")
class TestGetVacancy:
    http_client: AsyncClient = AsyncClient(base_url="http://0.0.0.0:8000/api/v1")

    async def test_get_vacancy(self):

        response = await self.http_client.get(f"/vacancy/{self.vacancy_id}/")
        assert response.status_code == 200

        json_response: dict = response.json()

        assert "status_code" in json_response
        assert "payload" in json_response

        payload = json_response["payload"]

        required_fields = [
            "id", "description", "sector", "manager", "salary_expectation",
            "urgency", "status", "start_date", "end_date", "notes"
        ]
        for field in required_fields:
            assert field in payload

    async def test_list_vacancies(self):
        pagination_params = {
            "page": 1,
            "page_size": 10,
            "search": None
        }

        response = await self.http_client.get(f"/vacancy/", params=pagination_params)

        assert response.status_code == 200

        json_response: dict = response.json()

        assert "status_code" in json_response
        assert "payload" in json_response

