from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.rate_limit import rate_limit
from app.schemas.user import UserRefreshTokenRequest, UserRefreshTokenResponse
from app.services.auth.user import UserService

router = APIRouter()

@router.post("/v1/refresh_access_token", response_model=UserRefreshTokenResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(rate_limit(requests=10000000, window_seconds=86400))])
async def refresh_access_token(request: Request, response: Response, token_pair: UserRefreshTokenRequest, db: AsyncSession=Depends(get_db)):
    tokens = await UserService(db=db).refresh_access_token_service(refresh_token=token_pair.refresh_token)
    
    response.set_cookie(
                key="refresh_token",
                value=tokens.refresh_token,
                httponly=True, 
                secure=True, 
                samesite="lax",
                max_age=259200,      
                path="/refresh",   
            )
        
    response.set_cookie(
            key="access_token",
            value=tokens.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=900
        )
        
    return tokens