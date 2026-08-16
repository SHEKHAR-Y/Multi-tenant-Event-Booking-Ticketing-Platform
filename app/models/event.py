from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from uuid import UUID, uuid4

from app.core.database import Base

from datetime import datetime

import enum

class EventStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELLED = "cancelled"

class Event(Base):
    __tablename__ = "events"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    organizer_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False) # foregin key to user.id 
    organizer: Mapped["User"] = relationship(back_populates="events")
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000))
    venue_name: Mapped[str] = mapped_column(String(100))
    venue_address: Mapped[str] = mapped_column(String(200))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[EventStatus] = mapped_column(Enum(EventStatus), nullable=False, default=EventStatus.PUBLISHED)
    created_at: Mapped[datetime] = mapped_column( DateTime(timezone=True),nullable=False,server_default=func.now(),)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now(),onupdate=func.now())
