from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class AppError(Exception):
    code: str
    message: str
    status_code: int = 400
    meta: Optional[dict[str, Any]] = None


class NotFound(AppError):
    def __init__(self, message="Entity not found", meta=None):
        super().__init__("not_found", message, 404, meta)


class Conflict(AppError):
    def __init__(self, message="Conflict", meta=None):
        super().__init__("conflict", message, 409, meta)


class NoOperatorsAvailable(AppError):
    def __init__(self, message="No suitable operators for this source", meta=None):
        super().__init__("no_operators_available", message, 422, meta)
