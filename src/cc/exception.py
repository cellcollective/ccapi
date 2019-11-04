from requests.exceptions import (
    HTTPError,
    ConnectionError
)

class CCError(Exception):
    pass

class ValueError(CCError, ValueError):
    pass

class TypeError(CCError, TypeError):
    pass

class AuthenticationError(CCError):
    pass