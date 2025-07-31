import json
import traceback
from datetime import datetime

from application.dto.vacancy import VacancyInput, VacancyOutput
from application.errors.database import SQLInjectionDetected
from application.errors.date import DateTimeWrongFormat, DateTimeWrongType
from application.interfaces.usecase import UseCase
from domain.interfaces.vacancy_repository import IVacancyRepository
from utils.database_utils import is_suspicious_input
from web.http_response_schema import HttpResponse, HttpResponseSchema


class CreateVacancyUseCase(UseCase):
    """
    Use case for creating a vacancy in the system (Implementing the UseCase interface).
    """

    def __init__(self, repository: IVacancyRepository):
        """
        Initialize the CreateVacancyUseCase with a repository.

        :param repository: An instance of IVacancyRepository to interact with vacancy data.
        """

        self.repository = repository

    def _validate_dates(self, start_date: datetime, end_date: datetime | None):
        """
        Validate that the start_date and end_date are valid ISO 8601 date strings or datetime objects.
        Raise ValueError if the validation fails.
        """

        for field_name, date_value in {
            "start_date": start_date,
            "end_date": end_date,
        }.items():

            if date_value is None:
                continue

            if isinstance(date_value, datetime):
                continue

            if isinstance(date_value, str):

                try:
                    datetime.fromisoformat(date_value.replace("Z", "+00:00"))
                except ValueError as exc:
                    raise DateTimeWrongFormat(
                        f"{field_name} has invalid datetime format: {date_value}. "
                        "Expected format: YYYY-MM-DDTHH:MM:SS[.fff]Z"
                    ) from exc
            else:
                raise DateTimeWrongFormat(
                    f"{field_name} must be a datetime or ISO 8601 string, not {type(date_value).__name__}"
                )

    def _validate_no_sql_commands(self, input_data: VacancyInput):
        """
        Check if any string field in the input contains SQL command patterns.
        Raises ValueError if suspicious SQL is detected.
        """
        for field_name, value in input_data.model_dump().items():
            if isinstance(value, str) and is_suspicious_input(value):
                raise SQLInjectionDetected(
                    f"Field '{field_name}' contains a forbidden SQL pattern."
                )

    async def execute(self, vacancy_data_input: VacancyInput) -> HttpResponse:

        try:

            self._validate_dates(
                vacancy_data_input.start_date, vacancy_data_input.end_date
            )
            self._validate_no_sql_commands(vacancy_data_input)

            created_vacancy: VacancyOutput = await self.repository.create_vacancy(
                vacancy_data_input
            )
            created_vacancy_dict = json.loads(created_vacancy.model_dump_json())
            return HttpResponseSchema.created(created_vacancy_dict)

        except (DateTimeWrongFormat, DateTimeWrongType, SQLInjectionDetected) as e:
            return HttpResponseSchema.unprocessable_entity(e)

        except Exception as e:
            traceback.print_exc()
            return HttpResponseSchema.internal_server_error(Exception(e))
