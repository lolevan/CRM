from __future__ import annotations

from pydantic import BaseModel, Field
from app.schemas.lead import LeadOut
from app.schemas.contact import ContactOut


class LeadWithContactsOut(BaseModel):
    lead: LeadOut = Field(..., description="Лид")
    contacts: list[ContactOut] = Field(
        default_factory=list,
        description="Обращения лида из разных источников",
    )
