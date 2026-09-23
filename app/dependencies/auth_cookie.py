from fastapi import Request, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.user import User

from app.dependencies.auth import get_current_user

async def get_optional_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")

    if not token:
        return None

    # else decode the token extract the  
    try : 
        return get_current_user(token=token, db=db)
    except Exception:
        return None 
