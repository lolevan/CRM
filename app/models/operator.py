from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    max_active_contacts: Mapped[int] = mapped_column(Integer, default=10)

    source_configs = relationship("SourceOperatorConfig", back_populates="operator", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="operator")
