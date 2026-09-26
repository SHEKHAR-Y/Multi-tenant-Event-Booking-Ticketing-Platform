from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/v1/logout", status_code=status.HTTP_200_OK)
def logout(request: Request, response: Response):
    # task 1: clear the cookies in the browser
    response = JSONResponse(
        content={"message": "Logout successful"},
        status_code=status.HTTP_200_OK
    )   
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response