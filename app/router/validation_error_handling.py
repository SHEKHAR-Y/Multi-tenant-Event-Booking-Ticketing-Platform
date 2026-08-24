from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

def validation_exception_handler(request: Request, exception: RequestValidationError):
    # give the validation error response instead of crash
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"error": exception.errors()}         
    )