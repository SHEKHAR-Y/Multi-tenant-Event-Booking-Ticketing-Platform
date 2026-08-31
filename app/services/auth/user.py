from sqlalchemy.orm import Session

from app.schemas.user import UserRegisterRequest, UserRegisterResponse
from app.core.exceptions import UserAlreadyExists, UserNotFound, InvalidCredentialError
from app.core.security import hash_password
from app.models.user import User
from app.repository.user import UserRepository
from app.core.security import verify_password, create_access_token
from app.core.db_error_handler import handle_db_error



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

def login_user_service(email: str, password: str, db: Session) -> str:
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

    return token
    


def check_user_exist_service(email: str, db: Session) -> User | None:
    """ user the repository exposed functions to access db and verify the user exist or not"""
    repo = UserRepository(db)

    return repo.get_user_by_email(email)

    