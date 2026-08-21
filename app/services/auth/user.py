from app.schemas.user import UserRegisterRequest, UserRegisterResponse
from app.core.exceptions import UserAlreadyExists
from app.core.security import hash_password
from app.models.user import User
from app.repository.user import UserRepository

from sqlalchemy.orm import Session


def register_user(user: UserRegisterRequest, db: Session) -> UserRegisterResponse: 
    """ check if the user already exist using the email sent in the request """
    if check_user_exist(user.email, db) is not None:
        # raise exception that user already exist
        raise UserAlreadyExists("User already Exist")
    
    # hash the password then access db to insert new user 
    hashed_password = hash_password(user.password)

    # repository call to register the user
    repo = UserRepository(db)
    data = User(
        email = user.email,
        hashed_password = hashed_password,
        full_name = user.username
    )

    new_user = repo.create_user(data)

    # after successfull registration do commit
    db.commit()

    # return response
    return UserRegisterResponse(
        email=new_user.email,
        username=new_user.full_name
    )



def check_user_exist(email: str, db: Session) -> User | None:
    """ user the repository exposed functions to access db and verify the user exist or not"""
    repo = UserRepository(db)

    repo.get_user_by_email(email)
    return None