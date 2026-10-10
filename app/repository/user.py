import uuid

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken
from app.models.user import User, UserRole


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        return await self.db.scalar(statement)

    async def get_user_by_id(self, id: uuid.UUID) -> User | None :
        statement = select(User).where(User.id == id)

        return await self.db.scalar(statement)

    async def create_user(self, new_user: User) -> User:
        self.db.add(new_user)
        await self.db.flush()
        await self.db.refresh(new_user)

        return new_user

    async def create_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        self.db.add(refresh_token)
        await self.db.flush()
        await self.db.refresh(refresh_token)

        return refresh_token

    async def fetch_refresh_token(self, jti: uuid.UUID) -> RefreshToken:
        statement = select(RefreshToken).where(RefreshToken.jti == jti)

        return await self.db.scalar(statement)

    async def mark_refresh_token_used(self, jti: uuid.UUID) -> RefreshToken:
        refresh_token = await self.fetch_refresh_token(jti=jti)

        refresh_token.is_used = True
        await self.db.flush()
        await self.db.refresh(refresh_token)

        return refresh_token

    async def revoke_refresh_tokens_with_same_family(self, family_id: uuid.UUID):
        statement = (update(RefreshToken).where(RefreshToken.family_id == family_id).values(is_revoked=True))
        await self.db.execute(statement)
        await self.db.flush()

    async def change_role_from_customer_to_organizer(self, user_id: uuid.UUID):
        statement = (update(User).where(User.id == user_id).values(role=UserRole.ORGANIZER))
        await self.db.execute(statement=statement)
        await self.db.flush()