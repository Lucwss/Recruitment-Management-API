import sqlparse
from pydantic import BaseModel

from application.errors.database import SQLInjectionDetected


def is_suspicious_input(text: str) -> bool:
    """
    Check if the input text contains SQL commands or suspicious patterns.
    """

    parsed = sqlparse.parse(text)
    return any(stmt.get_type() != "UNKNOWN" for stmt in parsed)


def validate_no_sql_commands(input_data: BaseModel):
    """
    Check if any string field in the input contains SQL command patterns.
    Raises ValueError if suspicious SQL is detected.
    """

    for field_name, value in input_data.model_dump().items():
        if isinstance(value, str) and is_suspicious_input(value):
            raise SQLInjectionDetected(
                f"Field '{field_name}' contains a forbidden SQL pattern."
            )
