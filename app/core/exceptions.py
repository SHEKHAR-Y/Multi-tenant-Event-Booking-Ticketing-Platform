
class AppError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class NotFoundError(AppError):
    pass

class UserAlreadyExists(AppError):
    def __init__(self, message):
        super().__init__(message)

class UserNotFound(AppError):
    def __init__(self, message):
        super().__init__(message)

class UserNotAuthorized(AppError):
    def __init__(self, message):
        super().__init__(message)

class InvalidTokenError(AppError):
    def __init__(self):
        super().__init__("Invalid authentication token")


class TokenExpiredError(AppError):
    def __init__(self):
        super().__init__("Authentication token has expired")

class DatabaseUnavailableError(AppError):
    def __init__(self, message):
        super().__init__(message)

class CustomIntegrityError(AppError):
    def __init__(self, message):
        super().__init__(message)


