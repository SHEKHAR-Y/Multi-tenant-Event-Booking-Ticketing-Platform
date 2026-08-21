from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserLoginRequest, UserLoginResponse
from app.core.security import create_access_token

router = APIRouter()


@router.post("/v1/login",response_model= UserLoginResponse,status_code=status.HTTP_200_OK)
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password

    # call the service to check the passowrd is correct and check if the user exist 

    # if the user exist and correct credentials(password & email) create a jwt token and return it
    token = create_access_token(email)

    return UserLoginResponse(
        jwt=token
    )
