from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError 
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.router.http_exception_handler import http_exception_handler
from app.router.validation_error_handling import validation_exception_handler

from app.router.auth.register import router as register
from app.router.auth.login import router as login
from app.router.auth.refresh_token import router as refresh_token_router
from app.router.auth.change_role import router as change_role_router

from app.router.event.create_event import router as create_event_router
from app.router.event.get_event import router as get_event_router
from app.router.event.create_event_seat import router as create_event_seat_router
from app.router.event.get_event_seats import router as get_event_seats

# exception handling 
from app.core.exceptions import (UserAlreadyExists, UserNotFound,InvalidTokenError,TokenExpiredError,NotFoundError, UserNotAuthorized, DatabaseUnavailableError, CustomIntegrityError, InvalidCredentialError, EventNotFound)
from app.core.exception_handlers import (user_already_exist, user_not_found, invalid_token_handler, token_expired_handler, user_not_authorized, database_unavailable, integrity_error, invalid_credential_error, event_not_found_handler)

# setting
from app.core.config import get_settings
settings = get_settings()

# logger 
from app.core.logging_config import configure_logging

configure_logging(debug=settings.debug)

# rate limiting 
from app.dependencies.rate_limit import rate_limit

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
app.add_exception_handler(EventNotFound, event_not_found_handler)


app.include_router(register, prefix="/api", tags=["Authentication"])
app.include_router(login, prefix="/api", tags=["Authentication"])
app.include_router(refresh_token_router, prefix="/api", tags=["Authentication"])
app.include_router(change_role_router, prefix="/api", tags=["Authentication"])

app.include_router(create_event_router, prefix="/api", tags=["Event"])
app.include_router(get_event_router, prefix="/api", tags=["Event"])
app.include_router(create_event_seat_router, prefix="/api", tags=["Event"])
app.include_router(get_event_seats, prefix="/api", tags=["Event"])

@app.get("/", dependencies=[Depends(rate_limit(requests=5, window_seconds=60))])
def health_check():
    return {"message": "API is healthy and running!"}
