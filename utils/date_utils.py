from datetime import datetime

from application.errors.date import DateTimeWrongFormat


def validate_dates(start_date: datetime, end_date: datetime | None):
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
