import random
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.operator import Operator
from app.models.source_operator import SourceOperatorConfig
from app.repositories.contact_repo import ContactRepo


class DistributionService:
    """
    Выбор оператора по весам для конкретного источника.
    Нагрузка = количество ACTIVE обращений (Contact.status=active).
    NEW обращения в нагрузку не входят.
    """

    def __init__(self, contact_repo: ContactRepo):
        self.contact_repo = contact_repo

    async def choose_operator(
        self,
        session: AsyncSession,
        source_id: int,
    ) -> Operator | None:
        res = await session.execute(
            select(SourceOperatorConfig, Operator)
            .join(Operator, Operator.id == SourceOperatorConfig.operator_id)
            .where(SourceOperatorConfig.source_id == source_id)
            .order_by(SourceOperatorConfig.id)  # стабильный порядок
        )
        rows = res.all()

        candidates: list[tuple[Operator, int]] = []
        for cfg, op in rows:
            if not op.is_active:
                continue

            active_cnt = await self.contact_repo.count_active_by_operator(session, op.id)
            if active_cnt >= op.max_active_contacts:
                continue

            w = int(cfg.weight or 0)
            if w > 0:
                candidates.append((op, w))

        if not candidates:
            return None

        ops, weights = zip(*candidates)
        return random.choices(ops, weights=weights, k=1)[0]
