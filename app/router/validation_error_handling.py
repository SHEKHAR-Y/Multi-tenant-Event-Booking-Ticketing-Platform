from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def validation_exception_handler(request: Request, exception: RequestValidationError):
    # give the validation error response instead of crash
    errors = exception.errors()
    for error in errors:
        for error in errors:
            if "ctx" in error and "error" in error["ctx"]:
                error["ctx"]["error"] = str(error["ctx"]["error"])
            if "input" in error and isinstance(error["input"], bytes):
                error["input"] = error["input"].decode("utf-8", errors="replace")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"error": exception.errors()}         
    )