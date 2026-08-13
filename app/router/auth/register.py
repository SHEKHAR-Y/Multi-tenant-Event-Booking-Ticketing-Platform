from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from schemas.user import UserRegisterRequest, UserRegisterResponse 
 
from services.auth import user 
from core import security  

router = APIRouter()


@router.post("/register", response_model=UserRegisterResponse)
def register(request: Request, register_data: UserRegisterRequest):

    try : 
        # check if the user already exists with the same email in the db (service layer -> repository layer -> db) 
        # if user exists raise exception 
        if user.check_existing_user(register_data.email): 
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, 
                content={"error": "User with this email already exists."}
            )

        # else hash the password and store the user in the db (core -> security -> hashing.py)
        else :
            hashed_password = security.hash_password(register_data.password)

        # if user is successully created return respone expected
        return UserRegisterResponse(
            email=register_data.email, 
            username=register_data.username,
            hashed_password=hashed_password
        )
     

    # else raise exception with rollback transaction and return error response
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content={"error": "An error occurred while registering the user."}
            )