class DateTimeWrongType(TypeError):
    """
    Custom error for wrong type of datetime input.
    """

    def __init__(
        self, message: str = "Expected a string or datetime in ISO 8601 format"
    ):
        super().__init__(message)


class DateTimeWrongFormat(ValueError):
    """
    Custom error for wrong format of datetime input.
    """

    def __init__(
        self, message: str = "Invalid datetime format. Expected ISO 8601 format."
    ):
        super().__init__(message)
