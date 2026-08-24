from fastapi import APIRouter, Request, status, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.core.database import get_db

from app.schemas.user import UserRegisterRequest, UserRegisterResponse 
 
from app.services.auth.user import register_user_service

import logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/v1/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
def register(request: Request, register_data: UserRegisterRequest, db: Session = Depends(get_db)):

    res = register_user_service(register_data, db)
    return res