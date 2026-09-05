from sqlalchemy import String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

from datetime import datetime

from uuid import UUID, uuid4

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    jti: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, nullable=False)
    family_id: Mapped[UUID] = mapped_column(index=True, nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    expiry: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped["User"] = relationship("User")
