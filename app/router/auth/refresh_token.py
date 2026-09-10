from fastapi import APIRouter, Depends, Request, status 

from sqlalchemy.orm import Session

from app.schemas.user import UserRefreshTokenRequest, UserRefreshTokenResponse

from app.services.auth.user import UserService

from app.core.database import get_db

from app.dependencies.rate_limit import rate_limit


router = APIRouter()

@router.post("/v1/refresh_access_token", response_model=UserRefreshTokenResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(rate_limit(requests=10, window_seconds=86400))])
def refresh_access_token(request: Request, token_pair: UserRefreshTokenRequest, db: Session=Depends(get_db)):
    return UserService(db=db).refresh_access_token_service(refresh_token=token_pair.refresh_token)
