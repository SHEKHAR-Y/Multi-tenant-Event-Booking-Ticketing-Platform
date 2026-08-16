from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError 
from starlette.exceptions import HTTPException as StarletteHTTPException

from router.http_exception_handler import http_exception_handler
from router.validation_error_handling import validation_exception_handler

from router.auth.login import router as login
from router.auth.register import router as register

from router.event.create_event import router as create_event_router

app = FastAPI()

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(login, prefix="/api", tags=["Authentication"])
app.include_router(register, prefix="/api", tags=["Authentication"])
app.include_router(create_event_router, prefix="/api/event", tags=["Event"])

@app.get("/")
def health_check():
    return {"message": "API is healthy and running!"}
