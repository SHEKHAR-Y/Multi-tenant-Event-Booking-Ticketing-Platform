from sqlalchemy.orm import Session

import uuid

from app.core.exceptions import UserAlreadyExists, UserNotFound, InvalidCredentialError, UserNotAuthorized
from app.core.security import hash_password
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_refresh_token
from app.core.db_error_handler import handle_db_error

from app.schemas.user import UserRegisterRequest, UserRegisterResponse, UserLoginResponse

from app.models.refresh_token import RefreshToken
from app.models.user import User

from app.repository.user import UserRepository

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(self.db)

    def check_user_exist_by_email_service(self, email: str) -> User | None:
        """ user the repository exposed functions to access db and verify the user exist or not"""
        return self.repo.get_user_by_email(email)

    def check_user_exist_by_id_service(self, id: uuid.UUID) -> User | None:
        """ use the repository exposed functions to access db and verify the user exist or not via user_id"""
        return self.repo.get_user_by_id(id)

    def store_refresh_token_service(self, token_id: uuid.UUID, token_expiry, user_id: uuid.UUID, family_id: uuid.UUID | None = None) -> bool:
        if family_id is None: 
            family_id = uuid.uuid4()

        # user id 
        user_id = user_id

        # create the object 
        refresh_token_object = RefreshToken(
            jti = token_id,
            family_id = family_id,
            user_id = user_id,
            expiry = token_expiry
        )

        # use repo to access db and create 
        with handle_db_error(self.db):
            refreh_token = self.repo.create_refresh_token(refresh_token_object)
            self.db.commit()

        return True

    def register_user_service(self, user: UserRegisterRequest) -> UserRegisterResponse: 
        """ check if the user already exist using the email sent in the request """
        if self.check_user_exist_by_email_service(user.email) is not None:
            # raise exception that user already exist
            raise UserAlreadyExists("User already Exist")

        # hash the password then access db to insert new user 
        hashed_password = hash_password(user.password)

        # repository call to register the user
        new_user = User(
            email = user.email,
            hashed_password = hashed_password,
            full_name = user.username
        )

        with handle_db_error(self.db):
            new_user = self.repo.create_user(new_user)
            # commit after successfull registration 
            self.db.commit()

        # return response
        return UserRegisterResponse(
            email=new_user.email,
            username=new_user.full_name
        )

    def login_user_service(self, email: str, password: str) -> UserLoginResponse:
        """Authenticate a user and return an access token."""
        user = self.check_user_exist_by_email_service(email)

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
        refresh_token, jti, expiry = create_refresh_token(subject)

        # store the refresh_token for token revocation or token rotation
        refresh = self.store_refresh_token_service(token_id=uuid.UUID(jti), token_expiry=expiry, user_id=uuid.UUID(subject))

        if not refresh:
            raise UserNotAuthorized("error while token rotation mechanism")

        return UserLoginResponse(
            access_token=token,
            refresh_token=refresh_token
        )

    def refresh_access_token_service(self, refresh_token: str) -> UserLoginResponse:
        # check if the refresh token is provided
        if not refresh_token :
            raise InvalidCredentialError("Refresh token is required")

        # decode the refresh token and get the user_id 
        payload = decode_refresh_token(refresh_token)

        # extract user_id from the payload (* important user_id in db is a uuid not string)
        # extract jti from the payload so that we can use it to extract the family_id and then use family id to 
        # generate a new refresh token and mark earlier one used
        user_id = uuid.UUID(payload["sub"])
        jti = uuid.UUID(payload["jti"])

        # check the user exist in the db using the user_id
        check_user = self.check_user_exist_by_id_service(user_id)

        if check_user is None:
            raise UserNotFound("User not found")

        # fetch the current refresh token details from the db 
        old_refresh_token_object = self.fetch_refresh_token_from_db_service(jti=jti)

        # extract family id
        family_id = old_refresh_token_object.family_id

        if not old_refresh_token_object: 
            raise InvalidCredentialError("invalid refresh token")

        if old_refresh_token_object.is_used == True:
            # in this case use the family id to revoke all the tokens and raise exception
            # * to be completed
            self.revoke_refresh_token(family_id=family_id)
            raise InvalidCredentialError("threat detected")

        if old_refresh_token_object.is_revoked == True:
            raise InvalidCredentialError("threat detected")

        # mark the current refresh token used
        self.mark_current_refresh_token_used_service(jti=jti)

        # create new access token and refresh token
        subject = str(check_user.id)
        new_access_token = create_access_token(subject=subject)
        new_refresh_token, jti, new_expiry = create_refresh_token(subject=subject)

        # create a new refresh token object to be stored in db with the same family id
        new_refresh_token_object = self.store_refresh_token_service(token_id=uuid.UUID(jti), token_expiry=new_expiry, user_id=user_id, family_id=family_id)

        if new_refresh_token_object == False: 
            raise InvalidCredentialError("token cretion failed")

        return UserLoginResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )

    def fetch_refresh_token_from_db_service(self, jti: uuid.UUID) -> RefreshToken:
        # use repo to access db and get 
        with handle_db_error(self.db):
            token = self.repo.fetch_refresh_token(jti=jti)
            self.db.commit()
            return token

    def mark_current_refresh_token_used_service(self, jti: uuid.UUID) -> RefreshToken:
        # use repo to access db and marks token used
        with handle_db_error(self.db):
            self.repo.mark_refresh_token_used(jti=jti)
            self.db.commit()

    def revoke_refresh_token(self, family_id: uuid.UUID):
        # use repo and revoke all the tokens with the family id 
        with handle_db_error(self.db):
            self.repo.revoke_refresh_tokens_with_same_family(family_id=family_id) 
            self.db.commit()