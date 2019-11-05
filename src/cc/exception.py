from requests.exceptions import (
    HTTPError,
    ConnectionError
)
from json.decoder import JSONDecodeError

class CCError(Exception):
    pass

class ValueError(CCError, ValueError):
    pass

class TypeError(CCError, TypeError):
    pass

class ResponseError(CCError):
    pass

class AuthenticationError(CCError):
    pass

class TemplateNotFoundError(CCError):
    pass