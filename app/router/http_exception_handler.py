from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

def http_exception_handler(request: Request, exception: StarletteHTTPException):
    # give the HTTP exception response instead of crash
    return JSONResponse(
        status_code=exception.status_code,
        content={"error": exception.detail}
    )