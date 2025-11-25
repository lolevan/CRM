from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.operator import Operator

class OperatorRepo:
    async def create(self, session: AsyncSession, op: Operator) -> Operator:
        session.add(op)
        await session.flush()
        return op

    async def get(self, session: AsyncSession, op_id: int) -> Operator | None:
        res = await session.execute(select(Operator).where(Operator.id == op_id))
        return res.scalar_one_or_none()

    async def list(self, session: AsyncSession) -> list[Operator]:
        res = await session.execute(select(Operator).order_by(Operator.id))
        return list(res.scalars().all())
