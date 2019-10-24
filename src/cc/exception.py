class CCError(Exception):
    pass

class ValueError(CCError):
    pass

class AuthenticationError(CCError):
    pass