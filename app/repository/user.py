from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.db_error_handler import handle_db_error 

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        return self.db.scalar(statement)

    def get_user_by_id(self, id: str) -> User | None :
        statement = select(User).where(User.id == id)

        return self.db.scalar(statement)

    def create_user(self, new_user: User) -> User:
        self.db.add(new_user)
        self.db.flush()

        return new_user

    