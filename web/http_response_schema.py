from typing import Any

from pydantic import BaseModel


class HttpResponse(BaseModel):
    """Standard HTTP response for all requests."""

    status_code: int
    payload: Any


class DefaultFileResponse(BaseModel):
    """
    Default file response schema.
    """

    media: Any
    status_code: int = 200


class HttpResponseSchema:
    """
    Helper class for HTTP responses.
    """

    @staticmethod
    def unauthorized(error: Exception) -> HttpResponse:
        """
        This method treats a bad request response from server
        :param error: --> Exception caught or raised in the system.
        :return: HttpResponse object with status_code and payload with the reason of error.
        """

        return HttpResponse(status_code=401, payload=str(error))

    @staticmethod
    def forbidden(error: Exception) -> HttpResponse:
        """
        This method treats a bad request response from server
        :param error: --> Exception caught or raised in the system.
        :return: HttpResponse object with status_code and payload with the reason of error.
        """

        return HttpResponse(status_code=403, payload=str(error))

    @staticmethod
    def bad_request(error: Exception) -> HttpResponse:
        """
        This method treats a bad request response from server
        :param error: --> Exception caught or raised in the system.
        :return: HttpResponse object with status_code and payload with the reason of error.
        """

        return HttpResponse(status_code=400, payload=str(error))

    @staticmethod
    def unprocessable_entity(error: Exception) -> HttpResponse:
        """
        This method treats a unprocessable entity response from server
        :param error: --> Exception caught or raised in the system.
        :return: HttpResponse object with status_code and payload with the reason of error.
        """

        return HttpResponse(status_code=422, payload=str(error))

    @staticmethod
    def internal_server_error(error: Exception) -> HttpResponse:
        """
        This method treats a internal server error response from server
        :param error: --> Exception caught or raised in the system.
        :return: HttpResponse object with status_code and payload with the reason of error.
        """

        return HttpResponse(status_code=500, payload=str(error))

    @staticmethod
    def service_unavailable(error: Exception) -> HttpResponse:
        """
        This method treats a service unavailable error response from server
        :param error: --> Exception caught or raised in the system.
        :return: HttpResponse object with status_code and payload with the reason of error.
        """

        return HttpResponse(status_code=503, payload=str(error))

    @staticmethod
    def not_found(error: Exception) -> HttpResponse:
        """
        This method treats a not found error response from server
        :param error: --> Exception caught or raised in the system.
        :return: HttpResponse object with status_code and payload with the reason of error.
        """

        return HttpResponse(status_code=404, payload=str(error))

    @staticmethod
    def ok(data: Any):
        """
        This method treats a successful response from server
        :param data: --> Content to be shown as a success response.
        :return: HttpResponse object with status_code and payload with the reason of error.
        """

        return HttpResponse(status_code=200, payload=data)

    @staticmethod
    def ok_file_response(media: Any) -> DefaultFileResponse:
        """
        This method treats a successful file response from server
        """

        return DefaultFileResponse(status_code=200, media=media)

    @staticmethod
    def created(data: Any):
        """
        This method treats a successful created response from server
        :param data: --> Content to be shown as a success response.
        :return: HttpResponse object with status_code and payload with the reason of error.
        """

        return HttpResponse(status_code=201, payload=data)
