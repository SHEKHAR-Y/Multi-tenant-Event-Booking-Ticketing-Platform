from fastapi import APIRouter, Request, status, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.schemas.user import UserLoginResponse

from app.core.database import get_db

from app.services.auth.user import UserService

from app.dependencies.rate_limit import rate_limit

router = APIRouter()

@router.post("/v1/login", response_model= UserLoginResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(rate_limit(requests=500, window_seconds=180))])
def login(request: Request, response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # call the service to check the passowrd is correct and check if the user exist 
    tokens = UserService(db=db).login_user_service(form_data.username, form_data.password)

    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=False,
        secure=False,
        samesite="lax",
        max_age=900
    )
    
    response.set_cookie(
            key="access_token",
            value=tokens.access_token,
            httponly=False,
            secure=False,
            samesite="lax",
            max_age=900
        )
    
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=False, 
        secure=False, 
        samesite="lax",
        max_age=259200,      
        path="/api/v1/refresh_access_token",   
    )

    return tokens

