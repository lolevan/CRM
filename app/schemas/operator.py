from __future__ import annotations
from pydantic import BaseModel, Field


class OperatorCreate(BaseModel):
    name: str = Field(..., description="Имя оператора", examples=["Ivan Operator"])
    max_active_contacts: int = Field(
        10,
        ge=0,
        description="Максимально допустимое число активных обращений",
        examples=[10],
    )
    is_active: bool = Field(
        True,
        description="Флаг активности. Неактивный оператор не получает новые обращения",
        examples=[True],
    )


class OperatorUpdate(BaseModel):
    max_active_contacts: int | None = Field(
        None, ge=0, description="Новый лимит активных обращений"
    )
    is_active: bool | None = Field(
        None, description="Изменение статуса активности"
    )


class OperatorOut(BaseModel):
    id: int = Field(..., description="ID оператора", examples=[1])
    name: str = Field(..., description="Имя оператора")
    is_active: bool = Field(..., description="Активен ли оператор")
    max_active_contacts: int = Field(..., description="Лимит активных обращений")

    class Config:
        from_attributes = True
