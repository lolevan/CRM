from __future__ import annotations
from pydantic import BaseModel, Field


class DistributionRow(BaseModel):
    source_code: str = Field(
        ...,
        description="Код источника/бота",
        examples=["bot_a"],
    )
    operator_id: int | None = Field(
        None,
        description="ID оператора, которому назначены обращения. null — если обращения без оператора",
        examples=[1, None],
    )
    operator_name: str | None = Field(
        None,
        description="Имя оператора (если назначен)",
        examples=["Ivan Operator", None],
    )
    contacts_count: int = Field(
        ...,
        ge=0,
        description="Количество обращений для пары (источник, оператор)",
        examples=[42],
    )
