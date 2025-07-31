import json
import traceback

from application.dto.vacancy import VacancyInput, VacancyOutput
from application.errors.database import SQLInjectionDetected
from application.errors.date import DateTimeWrongFormat, DateTimeWrongType
from application.interfaces.usecase import UseCase
from domain.interfaces.vacancy_repository import IVacancyRepository
from utils.database_utils import is_valid_uuid, validate_no_sql_commands
from utils.date_utils import validate_dates
from web.http_response_schema import HttpResponse, HttpResponseSchema


class UpdateVacancyUseCase(UseCase):
    """
    Use case for updating a vacancy by its id in the system (Implementing the UseCase interface).
    """

    def __init__(self, repository: IVacancyRepository):
        """
        Initialize the UpdateVacancyUseCase with a repository.

        :param repository: An instance of IVacancyRepository to interact with vacancy data.
        """

        self.repository = repository

    async def execute(
        self, vacancy_id: str, vacancy_data_input: VacancyInput
    ) -> HttpResponse:

        try:
            is_valid_uuid_structure: bool = is_valid_uuid(vacancy_id)

            validate_dates(vacancy_data_input.start_date, vacancy_data_input.end_date)
            validate_no_sql_commands(vacancy_data_input)

            if not is_valid_uuid_structure:
                return HttpResponseSchema.bad_request(
                    Exception(f"Invalid UUID structure for id: {vacancy_id}.")
                )

            found_vacancy: VacancyOutput | None = (
                await self.repository.get_vacancy_by_id(vacancy_id)
            )

            if not found_vacancy:
                return HttpResponseSchema.not_found(
                    Exception(f"Vacancy not found for id: {vacancy_id}.")
                )

            updated_vacancy: VacancyOutput | None = (
                await self.repository.update_vacancy(vacancy_id, vacancy_data_input)
            )

            if not updated_vacancy:
                return HttpResponseSchema.bad_request(
                    Exception(f"Vacancy not found for id: {vacancy_id}.")
                )

            updated_vacancy_dict = json.loads(updated_vacancy.model_dump_json())
            return HttpResponseSchema.ok(updated_vacancy_dict)

        except (DateTimeWrongFormat, DateTimeWrongType, SQLInjectionDetected) as e:
            return HttpResponseSchema.unprocessable_entity(e)

        except Exception as e:
            traceback.print_exc()
            return HttpResponseSchema.internal_server_error(Exception(e))
