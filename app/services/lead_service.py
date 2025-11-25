from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.lead_repo import LeadRepo
from app.models.lead import Lead


class LeadService:
    def __init__(self, lead_repo: LeadRepo):
        self._lead_repo = lead_repo

    async def list_with_contacts(self, session: AsyncSession) -> list[Lead]:
        return await self._lead_repo.list_with_contacts(session)
