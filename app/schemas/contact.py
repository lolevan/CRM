from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.contact import ContactStatus
from app.schemas.lead import LeadCreateOrGet


class ContactCreate(BaseModel):
    lead: LeadCreateOrGet = Field(..., description="Данные лида для поиска/создания")
    source_code: str = Field(..., description="Код источника/бота", examples=["bot_a"])
    payload: str | None = Field(None, description="Произвольные данные обращения (JSON/текст)")


class ContactOut(BaseModel):
    id: int = Field(..., description="ID обращения")
    lead_id: int = Field(..., description="ID лида")
    source_id: int = Field(..., description="ID источника")
    operator_id: int | None = Field(None, description="Назначенный оператор (если есть)")
    status: ContactStatus = Field(..., description="Статус обращения")
    payload: str | None = Field(None, description="Тело обращения")
    created_at: datetime = Field(..., description="Дата создания")

    class Config:
        from_attributes = True
