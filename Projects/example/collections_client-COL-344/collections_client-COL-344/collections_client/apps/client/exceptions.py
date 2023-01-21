from requests.models import Response
from requests.exceptions import RequestException


class ClientHTTPError(RequestException):
    """400-e ошибки"""


class ServerHTTPError(RequestException):
    """500-e ошибки"""


def raise_for_status(response: Response):
    if 400 <= response.status_code < 500:
        raise ClientHTTPError("Ошибка на стороне клиента")
    elif response.status_code >= 500:
        raise ServerHTTPError("Ошибка на стороне сервера")
    return response
