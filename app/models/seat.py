import enum
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SeatStatus(str, enum.Enum):
    AVAILABLE = "available"
    LOCKED = "locked"
    BOOKED = "booked"

class Seat(Base):
    __tablename__ = "seats"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, nullable=False)
    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    row: Mapped[str] = mapped_column(String(4), nullable=False)
    seat_number: Mapped[int] = mapped_column(Integer)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    status: Mapped[SeatStatus] = mapped_column(Enum(SeatStatus), default=SeatStatus.AVAILABLE)

    event: Mapped["Event"] = relationship(back_populates="seats")
    