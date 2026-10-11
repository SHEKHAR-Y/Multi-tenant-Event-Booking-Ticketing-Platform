from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User


async def get_optional_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")

    if not token:
        return None

    # else decode the token extract the  
    try : 
        return await get_current_user(token=token, db=db)
    except Exception:
        return None 
