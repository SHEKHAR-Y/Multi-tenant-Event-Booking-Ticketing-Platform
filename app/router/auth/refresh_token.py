from fastapi import APIRouter, Depends, Request, status 

from sqlalchemy.orm import Session

from app.schemas.user import UserRefreshTokenRequest, UserRefreshTokenResponse
from app.services.auth.user import refresh_access_token_service
from app.core.database import get_db


router = APIRouter()

@router.post("/v1/refresh_access_token", response_model=UserRefreshTokenResponse, status_code=status.HTTP_201_CREATED)
def refresh_access_token(request: Request, token_pair: UserRefreshTokenRequest, db: Session=Depends(get_db)):
    return refresh_access_token_service(refresh_token=token_pair.refresh_token, db=db)
