from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient

from infra.scripts.wait_for_services import clear_database
from tests.integration.api.v1.vacancy.fake_data import generate_fake_vacancy_data


@pytest_asyncio.fixture(loop_scope="class", autouse=True)
async def setup_vacancy(request):
    """
    Runs once before all tests in the class.
    Creates a test vacancy and stores it in the class.
    """

    await clear_database()

    http_client = AsyncClient(base_url="http://0.0.0.0:8000/api/v1")
    request.cls.http_client = http_client

    payload_input = generate_fake_vacancy_data()
    response = await http_client.post("/vacancy/", json=payload_input)
    assert response.status_code == 201

    response_data = response.json()
    request.cls.vacancy_id = response_data["payload"]["id"]

    yield

    await http_client.aclose()
    await clear_database()


@pytest.mark.asyncio(loop_scope="class")
class TestUpdateVacancy:
    """
    Test class for updating a vacancy in the API.
    """

    http_client: AsyncClient = AsyncClient(base_url="http://0.0.0.0:8000/api/v1")

    async def test_update_vacancy(self):
        payload_input = generate_fake_vacancy_data()

        response = await self.http_client.put(
            f"/vacancy/{self.vacancy_id}/", json=payload_input
        )
        assert response.status_code == 200

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

    async def test_update_vacancy_wrong_id(self):

        response = await self.http_client.get("/vacancy/serigubsodfgiubs/")
        assert response.status_code == 400

    async def test_update_vacancy_not_found(self):
        random_id = str(uuid4())

        response = await self.http_client.get(f"/vacancy/{random_id}/")
        assert response.status_code == 404

    async def test_update_vacancy_missing_field(self):
        payload = generate_fake_vacancy_data()
        del payload["manager"]

        response = await self.http_client.put(
            f"/vacancy/{self.vacancy_id}/", json=payload
        )
        assert response.status_code == 422

    async def test_update_vacancy_invalid_data_types(self):
        payload = generate_fake_vacancy_data()
        payload["urgency"] = "high"
        payload["salary_expectation"] = "many"
        payload["start_date"] = 123456

        response = await self.http_client.put(
            f"/vacancy/{self.vacancy_id}/", json=payload
        )
        assert response.status_code == 422

    async def test_update_vacancy_special_characters(self):
        payload = generate_fake_vacancy_data()
        payload["description"] = "'; DROP TABLE users; --"
        payload["notes"] = "<script>alert('xss')</script>"
        payload["manager"] = "José 🌟"

        response = await self.http_client.put(
            f"/vacancy/{self.vacancy_id}/", json=payload
        )
        assert response.status_code == 422

    async def test_update_vacancy_boundary_values(self):
        payload = generate_fake_vacancy_data()
        payload["description"] = "x" * 1000
        payload["salary_expectation"] = 999999999999
        payload["urgency"] = -1

        response = await self.http_client.put(
            f"/vacancy/{self.vacancy_id}/", json=payload
        )
        assert response.status_code in [400, 422]

    async def test_update_vacancy_invalid_dates(self):
        payload = generate_fake_vacancy_data()
        payload["start_date"] = "2025-13-40T99:99:99Z"
        payload["end_date"] = "2020-01-01T00:00:00Z"

        response = await self.http_client.put(
            f"/vacancy/{self.vacancy_id}/", json=payload
        )
        assert response.status_code in [400, 422]

    async def test_update_vacancy_sql_injection(self):
        payload = generate_fake_vacancy_data()
        payload["description"] = "Robert'); DROP TABLE vacancies; --"

        response = await self.http_client.put(
            f"/vacancy/{self.vacancy_id}/", json=payload
        )
        assert response.status_code == 422
