from __future__ import annotations
from pydantic import BaseModel, Field


class SourceCreate(BaseModel):
    code: str = Field(..., min_length=1, description="Уникальный код источника/бота", examples=["bot_a"])
    name: str = Field(..., description="Название источника", examples=["Telegram Bot A"])


class SourceOut(BaseModel):
    id: int = Field(..., description="ID источника", examples=[1])
    code: str = Field(..., description="Уникальный код источника")
    name: str = Field(..., description="Название источника")

    class Config:
        from_attributes = True


class SourceOperatorWeight(BaseModel):
    operator_id: int = Field(..., description="ID оператора", examples=[10])
    weight: int = Field(
        ...,
        ge=0,
        description="Вес/компетенция оператора для этого источника",
        examples=[30],
    )


class SourceWeightsUpdate(BaseModel):
    operators: list[SourceOperatorWeight] = Field(
        ...,
        description="Полный список операторов, обслуживающих источник. Перезаписывает конфигурацию",
        examples=[{"operator_id": 1, "weight": 10}],
    )
