from pydantic import BaseModel

class MediaPdfOutput(BaseModel):
    """
    Output schema for a PDF media file.
    """

    path: str
    media_type: str
    file_name: str