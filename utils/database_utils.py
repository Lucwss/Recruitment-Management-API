import sqlparse


def is_suspicious_input(text: str) -> bool:
    """
    Check if the input text contains SQL commands or suspicious patterns.
    """

    parsed = sqlparse.parse(text)
    return any(stmt.get_type() != "UNKNOWN" for stmt in parsed)
