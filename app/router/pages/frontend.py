from fastapi import APIRouter, Depends, Request

from app.core.templates import templates
from app.dependencies.auth import get_current_user
from app.dependencies.auth_cookie import get_optional_current_user

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

@router.get("/refresh", include_in_schema=False)
async def refresh_access_token(request: Request):

    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    return templates.TemplateResponse(request=request, name="refresh.html", context={"access_token": access_token, "refresh_token": refresh_token})

@router.get("/events", include_in_schema=False)
async def events_page(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="events.html", context={"user": user})

@router.get("/events/{event_id}", include_in_schema=False)
async def event_detail_page(request: Request, event_id: str, user = Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request,
        name="event_detail.html",
        context={"user": user, "event_id": event_id},
    )