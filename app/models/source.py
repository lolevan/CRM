from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))

    operator_configs = relationship("SourceOperatorConfig", back_populates="source", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="source")
