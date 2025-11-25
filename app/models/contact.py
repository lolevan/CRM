from enum import Enum
from datetime import datetime, timezone
from sqlalchemy import Integer, DateTime, String, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class ContactStatus(str, Enum):
    new = "new"
    active = "active"
    closed = "closed"


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"))
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id", ondelete="CASCADE"))
    operator_id: Mapped[int | None] = mapped_column(ForeignKey("operators.id", ondelete="SET NULL"), nullable=True)

    status: Mapped[ContactStatus] = mapped_column(
        SAEnum(ContactStatus),
        default=ContactStatus.new,
        nullable=False,
    )

    payload: Mapped[str | None] = mapped_column(String, nullable=True)

    lead = relationship("Lead", back_populates="contacts")
    source = relationship("Source", back_populates="contacts")
    operator = relationship("Operator", back_populates="contacts")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
