from __future__ import annotations
from pydantic import BaseModel, Field


class LeadCreateOrGet(BaseModel):
    external_id: str = Field(
        ...,
        description="Внешний уникальный идентификатор лида (например, user_id в боте/CRM)",
        examples=["tg:12345678"],
    )
    phone: str | None = Field(None, description="Телефон лида", examples=["+79991234567"])
    email: str | None = Field(None, description="Email лида", examples=["lead@mail.com"])


class LeadOut(BaseModel):
    id: int = Field(..., description="ID лида")
    external_id: str = Field(..., description="Внешний ID лида")
    phone: str | None = Field(None, description="Телефон")
    email: str | None = Field(None, description="Email")

    class Config:
        from_attributes = True
