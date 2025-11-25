from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.source import Source

class SourceRepo:
    async def create(self, session: AsyncSession, source: Source) -> Source:
        session.add(source)
        await session.flush()
        return source

    async def get_by_code(self, session: AsyncSession, code: str) -> Source | None:
        res = await session.execute(select(Source).where(Source.code == code))
        return res.scalar_one_or_none()

    async def get(self, session: AsyncSession, source_id: int) -> Source | None:
        res = await session.execute(select(Source).where(Source.id == source_id))
        return res.scalar_one_or_none()

    async def list(self, session: AsyncSession) -> list[Source]:
        res = await session.execute(select(Source).order_by(Source.id))
        return list(res.scalars().all())
