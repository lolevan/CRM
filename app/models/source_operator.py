from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class SourceOperatorConfig(Base):
    __tablename__ = "source_operator_configs"
    __table_args__ = (UniqueConstraint("source_id", "operator_id", name="uq_source_operator"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id", ondelete="CASCADE"))
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id", ondelete="CASCADE"))
    weight: Mapped[int] = mapped_column(Integer, default=1)

    source = relationship("Source", back_populates="operator_configs")
    operator = relationship("Operator", back_populates="source_configs")
