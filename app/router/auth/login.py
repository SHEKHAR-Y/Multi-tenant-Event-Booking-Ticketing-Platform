from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from schemas.user import UserLoginRequest, UserLoginResponse

router = APIRouter()


@router.post("/login", response_model=UserLoginResponse, status_code=status.HTTP_200_OK)
def login(request: Request, request_data: UserLoginRequest):

    res = UserLoginResponse(email=request_data.email)

    return res