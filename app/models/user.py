from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String, Boolean, Enum, func 
from uuid import UUID, uuid4
from app.core.database import Base

from datetime import datetime

import enum


class UserRole(str, enum.Enum):
    ORGANIZER = "organizer"
    CUSTOMER = "customer"
    ADMIN = "admin"


# inherit from Base class (that inherit from declarative base) in core/database.py 
# (this declarative base tells sqlalchemy that this class is a model and should be mapped to a table in the database) 
class User(Base):

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(20), nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    events: Mapped[list["Event"]] = relationship(back_populates="organizer")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column( DateTime(timezone=True),nullable=False,server_default=func.now(),)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now(),onupdate=func.now())