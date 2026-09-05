from sqlalchemy import select, update
from sqlalchemy.orm import Session

import uuid

from app.models.user import User
from app.models.refresh_token import RefreshToken

from app.core.db_error_handler import handle_db_error 

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        return self.db.scalar(statement)

    def get_user_by_id(self, id: uuid.UUID) -> User | None :
        statement = select(User).where(User.id == id)

        return self.db.scalar(statement)

    def create_user(self, new_user: User) -> User:
        self.db.add(new_user)
        self.db.flush()
        self.db.refresh(new_user)

        return new_user

    def create_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        self.db.add(refresh_token)
        self.db.flush()
        self.db.refresh(refresh_token)

        return refresh_token

    def fetch_refresh_token(self, jti: uuid.UUID) -> RefreshToken:
        statement = select(RefreshToken).where(RefreshToken.jti == jti)

        return self.db.scalar(statement)

    def mark_refresh_token_used(self, jti: uuid.UUID) -> RefreshToken:
        refresh_token = self.fetch_refresh_token(jti=jti)

        refresh_token.is_used = True
        self.db.flush()
        self.db.refresh(refresh_token)

        return refresh_token

    def revoke_refresh_tokens_with_same_family(self, family_id: uuid.UUID):
        statement = (update(RefreshToken).where(RefreshToken.family_id == family_id).values(is_revoked=True))
        self.db.execute(statement)
        self.db.flush()