from fastapi import APIRouter, Depends, status, Request

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.dependencies.auth import get_current_user

from app.services.auth.user import UserService

from app.schemas.user import UserRoleChangeResponse

router = APIRouter()


@router.patch("/v1/change_role", status_code=status.HTTP_201_CREATED, response_model=UserRoleChangeResponse)
def change_user_role(request: Request, db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    userservice = UserService(db=db)
    user = userservice.change_user_role_customer_to_organizer(current_user)

    return UserRoleChangeResponse(
        email=user.email,
        role=user.role
    )