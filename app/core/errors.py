from __future__ import annotations

from typing import Any, Optional, Literal
from pydantic import BaseModel, Field


class ErrorDetailSchema(BaseModel):
    code: str = Field(..., description="Машинно-читаемый код ошибки")
    message: str = Field(..., description="Человекочитаемое сообщение")
    meta: Optional[dict[str, Any]] = Field(None, description="Доп.данные для отладки")


class ErrorResponseSchema(BaseModel):
    error: ErrorDetailSchema


class ValidationErrorSchema(ErrorResponseSchema):
    error: ErrorDetailSchema = Field(
        default_factory=lambda: ErrorDetailSchema(code="validation_error", message="Validation error")
    )


class NotFoundErrorSchema(ErrorResponseSchema):
    error: ErrorDetailSchema = Field(
        default_factory=lambda: ErrorDetailSchema(code="not_found", message="Entity not found")
    )


class ConflictErrorSchema(ErrorResponseSchema):
    error: ErrorDetailSchema = Field(
        default_factory=lambda: ErrorDetailSchema(code="conflict", message="Conflict")
    )


class ServerErrorSchema(ErrorResponseSchema):
    error: ErrorDetailSchema = Field(
        default_factory=lambda: ErrorDetailSchema(code="server_error", message="Internal server error")
    )


class NoOperatorsAvailableSchema(ErrorResponseSchema):
    error: ErrorDetailSchema = Field(
        default_factory=lambda: ErrorDetailSchema(
            code="no_operators_available",
            message="No suitable operators for this source",
        )
    )
