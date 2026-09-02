from fastapi import Depends 

import uuid

from sqlalchemy.orm import Session

from app.core.security import oauth2_scheme
from app.core.database import get_db
from app.core.security import decode_access_token
from app.core.exceptions import UserNotFound
from app.repository.user import UserRepository

from app.models.user import User


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    # decode the token and get the payload
    payload = decode_access_token(token)

    # now from the payload extract the subject (in our case it is the user id convert back to uuid.uuid4())
    user_id = uuid.UUID(payload["sub"])  

    # now check if the user exist in the database with the id (user user repository)
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_id(user_id)

    # exception handling if the user is not found
    if not user:
        raise UserNotFound("User not found")

    return user

