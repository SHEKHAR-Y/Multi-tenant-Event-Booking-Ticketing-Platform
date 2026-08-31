from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError 
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.router.http_exception_handler import http_exception_handler
from app.router.validation_error_handling import validation_exception_handler

from app.router.auth.login import router as login
from app.router.auth.register import router as register

from app.router.event.create_event import router as create_event_router

# exception handling 
from app.core.exceptions import (UserAlreadyExists, UserNotFound,InvalidTokenError,TokenExpiredError,NotFoundError, UserNotAuthorized, DatabaseUnavailableError, CustomIntegrityError, InvalidCredentialError)
from app.core.exception_handlers import (user_already_exist, user_not_found, invalid_token_handler, token_expired_handler, user_not_authorized, database_unavailable, integrity_error, invalid_credential_error)

# setting
from app.core.config import get_settings
settings = get_settings()

# logger 
from app.core.logging_config import configure_logging

configure_logging(debug=settings.debug)

app = FastAPI(
    title=settings.app_name
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.add_exception_handler(UserAlreadyExists, user_already_exist)
app.add_exception_handler(UserNotFound, user_not_found)
app.add_exception_handler(InvalidTokenError, invalid_token_handler)
app.add_exception_handler(TokenExpiredError, token_expired_handler)
app.add_exception_handler(UserNotAuthorized, user_not_authorized)
app.add_exception_handler(DatabaseUnavailableError, database_unavailable)
app.add_exception_handler(CustomIntegrityError, integrity_error)
app.add_exception_handler(InvalidCredentialError, invalid_credential_error)



app.include_router(login, prefix="/api", tags=["Authentication"])
app.include_router(register, prefix="/api", tags=["Authentication"])
app.include_router(create_event_router, prefix="/api", tags=["Event"])

@app.get("/")
def health_check():
    return {"message": "API is healthy and running!"}
