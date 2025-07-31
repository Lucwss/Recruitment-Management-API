class SQLInjectionDetected(ValueError):
    """
    Custom error for detecting SQL injection attempts.
    """

    def __init__(self, message: str = "SQL injection attempt detected."):
        super().__init__(message)
