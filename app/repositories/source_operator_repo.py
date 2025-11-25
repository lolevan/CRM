from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.source_operator import SourceOperatorConfig

class SourceOperatorRepo:
    async def list_for_source(self, session: AsyncSession, source_id: int) -> list[SourceOperatorConfig]:
        res = await session.execute(
            select(SourceOperatorConfig).where(SourceOperatorConfig.source_id == source_id)
        )
        return list(res.scalars().all())

    async def replace_for_source(self, session: AsyncSession, source_id: int, configs: list[SourceOperatorConfig]):
        await session.execute(delete(SourceOperatorConfig).where(SourceOperatorConfig.source_id == source_id))
        session.add_all(configs)
        await session.flush()
