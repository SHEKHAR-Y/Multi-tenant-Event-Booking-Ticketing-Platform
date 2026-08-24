from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import InvalidTokenError, TokenExpiredError, UserAlreadyExists, UserNotFound, UserNotAuthorized, DatabaseUnavailableError, CustomIntegrityError, InvalidCredentialError


async def user_already_exist(request: Request, exc: UserAlreadyExists):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error":exc.message}
    )

async def user_not_found(request: Request, exc: UserNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": exc.message}
    )

async def invalid_credential_error(request: Request, exc: InvalidCredentialError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": exc.message}
    )

async def user_not_authorized(requset: Request, exc: UserNotAuthorized):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"error": exc.message}
    )

async def invalid_token_handler(request: Request, exc: InvalidTokenError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": "InvalidToken", "message": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )

async def token_expired_handler(request: Request, exc: TokenExpiredError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": "TokenExpired", "message": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )

async def database_unavailable(request: Request, exc: DatabaseUnavailableError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"error": exc.message}
    )

async def integrity_error(request: Request, exc: CustomIntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": exc.message}
    )