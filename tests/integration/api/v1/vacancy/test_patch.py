import random

import pytest
import pytest_asyncio
from httpx import AsyncClient

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
class TestPatchVacancy:
    """
    Test class for changing the status of a vacancy in the API.
    """

    http_client: AsyncClient = AsyncClient(base_url="http://0.0.0.0:8000/api/v1")

    async def test_change_vacancy_status(self):

        status_to_insert = random.choice(["FINISHED", "CANCELED"])

        parameters = {"vacancy_status": status_to_insert}

        response = await self.http_client.patch(
            f"/vacancy/{self.vacancy_id}/status/", params=parameters
        )
        assert response.status_code == 200

        json_response: dict = response.json()

        assert "status_code" in json_response
        assert "payload" in json_response

        payload = json_response["payload"]

        assert payload["status"] == status_to_insert
