class NotFoundPdfMediaToGenerate(ValueError):
    """
    Custom error for when no PDF media is found to generate.
    """

    def __init__(self, message: str = "No PDF media found to generate."):
        super().__init__(message)
