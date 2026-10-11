from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.user import UserRoleChangeResponse
from app.services.auth.user import UserService

router = APIRouter()


@router.patch("/v1/change_role", status_code=status.HTTP_201_CREATED, response_model=UserRoleChangeResponse)
async def change_user_role(request: Request, db: AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    userservice = UserService(db=db)
    user = await userservice.change_user_role_customer_to_organizer(current_user)

    return UserRoleChangeResponse(
        email=user.email,
        role=user.role
    )