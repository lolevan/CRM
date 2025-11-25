from __future__ import annotations

from fastapi import APIRouter, Depends, Body, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db_session, get_source_repo, get_operator_repo, get_source_operator_repo
)
from app.repositories.source_repo import SourceRepo
from app.repositories.operator_repo import OperatorRepo
from app.repositories.source_operator_repo import SourceOperatorRepo
from app.models.source import Source
from app.models.source_operator import SourceOperatorConfig
from app.schemas.source import SourceCreate, SourceOut, SourceWeightsUpdate
from app.core.errors import (
    ValidationErrorSchema, NotFoundErrorSchema, ConflictErrorSchema, ServerErrorSchema
)
from app.core.exceptions import NotFound, Conflict

router = APIRouter(prefix="/sources")


@router.post(
    "",
    response_model=SourceOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создание источника (бота)",
    responses={
        status.HTTP_201_CREATED: {"model": SourceOut},
        status.HTTP_409_CONFLICT: {"model": ConflictErrorSchema},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ServerErrorSchema},
    },
)
async def create_source(
    payload: SourceCreate = Body(..., description="Данные источника/бота"),
    session: AsyncSession = Depends(get_db_session),
    source_repo: SourceRepo = Depends(get_source_repo),
):
    if await source_repo.get_by_code(session, payload.code):
        raise Conflict(message=f"Source code '{payload.code}' already exists")

    source = Source(**payload.model_dump())
    await source_repo.create(session, source)
    await session.commit()
    await session.refresh(source)
    return source


@router.get(
    "",
    response_model=list[SourceOut],
    summary="Список источников",
    responses={
        status.HTTP_200_OK: {"model": list[SourceOut]},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ServerErrorSchema},
    },
)
async def list_sources(
    session: AsyncSession = Depends(get_db_session),
    source_repo: SourceRepo = Depends(get_source_repo),
):
    return await source_repo.list(session)


@router.put(
    "/{source_id}/operators",
    summary="Настройка операторов источника",
    description="Полностью перезаписывает конфигурацию операторов и их весов для источника.",
    responses={
        status.HTTP_200_OK: {"content": {"application/json": {}}},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundErrorSchema},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ServerErrorSchema},
    },
)
async def set_source_operators(
    source_id: int = Path(..., description="ID источника"),
    payload: SourceWeightsUpdate = Body(..., description="Список операторов и весов"),
    session: AsyncSession = Depends(get_db_session),
    source_repo: SourceRepo = Depends(get_source_repo),
    operator_repo: OperatorRepo = Depends(get_operator_repo),
    cfg_repo: SourceOperatorRepo = Depends(get_source_operator_repo),
):
    source = await source_repo.get(session, source_id)
    if not source:
        raise NotFound(message=f"Source {source_id} not found")

    configs: list[SourceOperatorConfig] = []
    for item in payload.operators:
        op = await operator_repo.get(session, item.operator_id)
        if not op:
            raise NotFound(message=f"Operator {item.operator_id} not found")

        configs.append(
            SourceOperatorConfig(
                source_id=source_id,
                operator_id=item.operator_id,
                weight=item.weight,
            )
        )

    await cfg_repo.replace_for_source(session, source_id, configs)
    await session.commit()
    return {"source_id": source_id, "operators": payload.operators}
