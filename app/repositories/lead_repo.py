from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import Lead


class LeadRepo:
    async def get_by_external_id(self, session: AsyncSession, external_id: str) -> Lead | None:
        res = await session.execute(select(Lead).where(Lead.external_id == external_id))
        return res.scalar_one_or_none()

    async def create(self, session: AsyncSession, lead: Lead) -> Lead:
        session.add(lead)
        await session.flush()
        return lead

    async def list(self, session: AsyncSession) -> list[Lead]:
        res = await session.execute(select(Lead).order_by(Lead.id))
        return list(res.scalars().all())

    async def list_with_contacts(self, session: AsyncSession) -> list[Lead]:
        stmt = (
            select(Lead)
            .options(selectinload(Lead.contacts))
            .order_by(Lead.id)
        )
        res = await session.execute(stmt)
        return list(res.scalars().unique().all())
