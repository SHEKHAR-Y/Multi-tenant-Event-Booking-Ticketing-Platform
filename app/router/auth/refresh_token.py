from fastapi import APIRouter, Depends, Request, status 

from sqlalchemy.orm import Session

from app.schemas.user import UserLoginResponse, UserRefreshTokenRequest
from app.services.auth.user import refresh_access_token_service
from app.core.database import get_db


router = APIRouter()

@router.post("/v1/refresh_access_token", response_model=UserLoginResponse, status_code=status.HTTP_201_CREATED)
def refresh_access_token(request: Request, refresh_token: UserRefreshTokenRequest, db: Session=Depends(get_db)):
    return refresh_access_token_service(refresh_token=refresh_token.refresh_token, db=db)
