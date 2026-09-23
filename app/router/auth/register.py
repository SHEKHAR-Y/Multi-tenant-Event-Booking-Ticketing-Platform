from fastapi import APIRouter, Request, status, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.dependencies.rate_limit import rate_limit

from app.schemas.user import UserRegisterRequest, UserRegisterResponse 

from app.services.auth.user import UserService

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/v1/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(rate_limit(requests=15000000, window_seconds=300))])
def register(request: Request, register_data: UserRegisterRequest, db: Session = Depends(get_db)):
    res = UserService(db=db).register_user_service(register_data)
    return res