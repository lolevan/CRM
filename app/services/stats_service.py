from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.contact_repo import ContactRepo
from app.repositories.source_repo import SourceRepo
from app.repositories.operator_repo import OperatorRepo
from app.schemas.stats import DistributionRow


class StatsService:
    def __init__(
        self,
        contact_repo: ContactRepo,
        source_repo: SourceRepo,
        operator_repo: OperatorRepo,
    ):
        self._contact_repo = contact_repo
        self._source_repo = source_repo
        self._operator_repo = operator_repo

    async def distribution(self, session: AsyncSession) -> list[DistributionRow]:
        raw = await self._contact_repo.distribution_stats(session)

        sources = {s.id: s for s in await self._source_repo.list(session)}
        operators = {o.id: o for o in await self._operator_repo.list(session)}

        out: list[DistributionRow] = []
        for source_id, operator_id, cnt in raw:
            source = sources.get(source_id)
            operator = operators.get(operator_id) if operator_id is not None else None

            out.append(
                DistributionRow(
                    source_code=source.code if source else f"#{source_id}",
                    operator_id=operator_id,
                    operator_name=operator.name if operator else None,
                    contacts_count=int(cnt),
                )
            )
        return out
