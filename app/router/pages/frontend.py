from fastapi import APIRouter, Response, Request, Depends

from app.core.templates import templates 

from app.dependencies.auth_cookie import get_optional_current_user
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/", include_in_schema=False)
async def home(request: Request, user = Depends(get_optional_current_user)):
    return templates.TemplateResponse(request=request, name="home.html", context={"user": user})

@router.get("/login", include_in_schema=False)
async def login_page(request: Request, user = Depends(get_optional_current_user)):
    return templates.TemplateResponse(request=request, name="login.html", context={"user": user, "error": None})

@router.get("/register", include_in_schema=False)
async def register_page(request: Request, user = Depends(get_optional_current_user)):
    return templates.TemplateResponse(request=request, name="register.html", context={"user": user, "error": None})

# from app.dependencies.auth_cookie import get_optional_current_user  # forces nothing itself,
# # but /events should require login — reuse your existing forcing dependency:
# from app.dependencies.auth import get_current_user

@router.get("/events", include_in_schema=False)
async def events_page(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="events.html", context={"user": user})