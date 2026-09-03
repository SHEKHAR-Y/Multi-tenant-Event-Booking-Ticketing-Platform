from sqlalchemy.orm import Session

import uuid

from app.core.exceptions import UserAlreadyExists, UserNotFound, InvalidCredentialError
from app.core.security import hash_password
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_refresh_token
from app.core.db_error_handler import handle_db_error

from app.schemas.user import UserRegisterRequest, UserRegisterResponse, UserLoginResponse

from app.models.user import User

from app.repository.user import UserRepository

def register_user_service(user: UserRegisterRequest, db: Session) -> UserRegisterResponse: 
    """ check if the user already exist using the email sent in the request """
    if check_user_exist_service(user.email, db) is not None:
        # raise exception that user already exist
        raise UserAlreadyExists("User already Exist")
    
    # hash the password then access db to insert new user 
    hashed_password = hash_password(user.password)

    # repository call to register the user
    repo = UserRepository(db)
    new_user = User(
        email = user.email,
        hashed_password = hashed_password,
        full_name = user.username
    )

    with handle_db_error(db):
        new_user = repo.create_user(new_user)
        # commit after successfull registration 
        db.commit()

    # return response
    return UserRegisterResponse(
        email=new_user.email,
        username=new_user.full_name
    )

def login_user_service(email: str, password: str, db: Session) -> UserLoginResponse:
    """Authenticate a user and return an access token."""
    user = check_user_exist_service(email, db)

    if user is None:
        raise UserNotFound("User not found, check email and try again")

    # verify the password hash
    verify = verify_password(password, user.hashed_password)

    if not verify: 
        # raise exception for wrong password
        raise InvalidCredentialError("Invalid credentials were entered")


    # token creation and return token
    subject = str(user.id)
    token = create_access_token(subject)
    refresh_token = create_refresh_token(subject)

    return UserLoginResponse(
        access_token=token,
        refresh_token=refresh_token
    )

def check_user_exist_service(email: str, db: Session) -> User | None:
    """ user the repository exposed functions to access db and verify the user exist or not"""
    repo = UserRepository(db)

    return repo.get_user_by_email(email)

def check_user_exist_by_id_service(id: uuid.UUID, db: Session) -> User | None:
    """ use the repository exposed functions to access db and verify the user exist or not via user_id"""
    repo = UserRepository(db)

    return repo.get_user_by_id(id)


def refresh_access_token_service(refresh_token: str, db: Session) -> UserLoginResponse:

    # decode the refresh token and get the user_id 
    payload = decode_refresh_token(refresh_token)

    # extract user_id from the payload (* important user_id in db is a uuid not string)
    user_id = uuid.UUID(payload["sub"])

    # check the user exist in the db using the user_id
    check_user = check_user_exist_by_id_service(user_id, db)

    if check_user is None:
        raise UserNotFound("User not found")

    # create new access token and return it
    subject = str(check_user.id)
    new_access_token = create_access_token(subject=subject)

    return UserLoginResponse(
        access_token=new_access_token,
        refresh_token=refresh_token
    )