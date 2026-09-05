from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.schemas.user import UserLoginResponse
from app.core.security import create_access_token
from app.services.auth.user import UserService
from app.core.database import get_db

router = APIRouter()


@router.post("/v1/login", response_model= UserLoginResponse, status_code=status.HTTP_200_OK)
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # call the service to check the passowrd is correct and check if the user exist 
    tokens = UserService(db=db).login_user_service(form_data.username, form_data.password)

    return tokens

