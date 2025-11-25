from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.contact import Contact, ContactStatus

class ContactRepo:
    async def create(self, session: AsyncSession, contact: Contact) -> Contact:
        session.add(contact)
        await session.flush()
        return contact

    async def count_active_by_operator(self, session: AsyncSession, operator_id: int) -> int:
        res = await session.execute(
            select(func.count(Contact.id))
            .where(Contact.operator_id == operator_id, Contact.status == ContactStatus.active)
        )
        return int(res.scalar() or 0)

    async def list_by_lead(self, session: AsyncSession, lead_id: int) -> list[Contact]:
        res = await session.execute(select(Contact).where(Contact.lead_id == lead_id))
        return list(res.scalars().all())

    async def distribution_stats(self, session: AsyncSession):
        res = await session.execute(
            select(Contact.source_id, Contact.operator_id, func.count(Contact.id))
            .group_by(Contact.source_id, Contact.operator_id)
        )
        return res.all()
