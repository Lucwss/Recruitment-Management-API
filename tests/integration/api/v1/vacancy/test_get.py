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
    payload_input["sector"] = "IT"

    response = await http_client.post("/vacancy/", json=payload_input)
    assert response.status_code == 201

    response_data = response.json()
    request.cls.vacancy_id = response_data["payload"]["id"]

    yield

    await http_client.aclose()
    await clear_database()


@pytest.mark.asyncio(loop_scope="class")
class TestGetVacancy:
    """
    Test class for retrieving a vacancy and listing vacancies in the API.
    """

    http_client: AsyncClient = AsyncClient(base_url="http://0.0.0.0:8000/api/v1")

    async def test_get_vacancy(self):

        response = await self.http_client.get(f"/vacancy/{self.vacancy_id}/")
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

    async def test_list_vacancies(self):
        pagination_params = {"page": 1, "page_size": 10, "search": None}

        response = await self.http_client.get("/vacancy/", params=pagination_params)

        assert response.status_code == 200

        json_response: dict = response.json()

        assert "status_code" in json_response
        assert "payload" in json_response

    async def test_get_vacancy_wrong_id(self):

        response = await self.http_client.get("/vacancy/serigubsodfgiubs/")
        assert response.status_code == 400

    async def test_get_vacancy_not_found(self):

        random_id = str(uuid4())

        response = await self.http_client.get(f"/vacancy/{random_id}/")
        assert response.status_code == 404


@pytest.mark.asyncio(loop_scope="class")
class TestSystemStatusEndpoint:
    """
    Test suite for GET /api/v1/status endpoint.
    """

    http_client: AsyncClient = AsyncClient(base_url="http://0.0.0.0:8000/api/v1")

    async def test_anonymous_user_can_retrieve_system_status(self):
        response = await self.http_client.get("/health/status/")
        assert response.status_code == 200

        body = response.json()
        assert body is not None

        payload = body.get("payload")

        updated_at = payload.get("updated_at")
        assert updated_at is not None

        dependencies = payload.get("dependencies", {})
        database = dependencies.get("database", {})
        assert database is not None

        assert database.get("version") == 16.9
        assert database.get("max_connections") == 100
        assert database.get("opened_connections") == 1


@pytest.mark.asyncio(loop_scope="class")
class TestDownloadSummaryEndpoint:
    """
    Test suite for GET /api/v1/vacancy/summary endpoint.
    """

    http_client: AsyncClient = AsyncClient(base_url="http://0.0.0.0:8000/api/v1")

    async def test_download_summary(self):
        response = await self.http_client.get(
            "/vacancy/summary/download/", params={"sector": "IT"}
        )

        assert response.status_code == 200

    async def test_not_found_download_summary(self):
        response = await self.http_client.get(
            "/vacancy/summary/download/", params={"sector": "asrgrçksudbfgd"}
        )

        assert response.status_code == 404
