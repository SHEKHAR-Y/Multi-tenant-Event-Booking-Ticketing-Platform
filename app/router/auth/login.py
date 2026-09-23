from fastapi import APIRouter, Request, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.schemas.user import UserLoginResponse

from app.core.database import get_db

from app.services.auth.user import UserService

from app.dependencies.rate_limit import rate_limit

router = APIRouter()


@router.post("/v1/login", response_model= UserLoginResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(rate_limit(requests=5000000, window_seconds=180))])
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # call the service to check the passowrd is correct and check if the user exist 
    tokens = UserService(db=db).login_user_service(form_data.username, form_data.password)

    return tokens

