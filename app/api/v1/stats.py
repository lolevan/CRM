from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, get_stats_service
from app.services.stats_service import StatsService
from app.schemas.stats import DistributionRow
from app.core.errors import ServerErrorSchema

router = APIRouter(prefix="/stats")


@router.get(
    "/distribution",
    response_model=list[DistributionRow],
    summary="Распределение обращений",
    description=(
        "Агрегированная статистика распределения обращений по источникам и операторам."
    ),
    responses={
        status.HTTP_200_OK: {"model": list[DistributionRow]},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ServerErrorSchema},
    },
)
async def distribution(
    session: AsyncSession = Depends(get_db_session),
    service: StatsService = Depends(get_stats_service),
):
    return await service.distribution(session)
