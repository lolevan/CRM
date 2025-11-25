from __future__ import annotations

from fastapi import APIRouter, Depends, Body, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, get_operator_repo
from app.repositories.operator_repo import OperatorRepo
from app.models.operator import Operator
from app.schemas.operator import OperatorCreate, OperatorOut, OperatorUpdate
from app.core.errors import (
    ValidationErrorSchema, NotFoundErrorSchema, ConflictErrorSchema, ServerErrorSchema
)
from app.core.exceptions import NotFound

router = APIRouter(prefix="/operators")


@router.post(
    "",
    response_model=OperatorOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создание оператора",
    description="Создаёт нового оператора, который может получать обращения.",
    responses={
        status.HTTP_201_CREATED: {"model": OperatorOut},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ServerErrorSchema},
    },
)
async def create_operator(
    payload: OperatorCreate = Body(..., description="Данные нового оператора"),
    session: AsyncSession = Depends(get_db_session),
    repo: OperatorRepo = Depends(get_operator_repo),
):
    op = Operator(**payload.model_dump())
    await repo.create(session, op)
    await session.commit()
    await session.refresh(op)
    return op


@router.get(
    "",
    response_model=list[OperatorOut],
    summary="Список операторов",
    description="Возвращает всех операторов с их лимитами и статусом активности.",
    responses={
        status.HTTP_200_OK: {"model": list[OperatorOut]},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ServerErrorSchema},
    },
)
async def list_operators(
    session: AsyncSession = Depends(get_db_session),
    repo: OperatorRepo = Depends(get_operator_repo),
):
    return await repo.list(session)


@router.patch(
    "/{operator_id}",
    response_model=OperatorOut,
    summary="Обновление параметров оператора",
    description="Меняет лимит нагрузки и/или активность оператора.",
    responses={
        status.HTTP_200_OK: {"model": OperatorOut},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundErrorSchema},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ServerErrorSchema},
    },
)
async def update_operator(
    operator_id: int = Path(..., description="ID оператора"),
    payload: OperatorUpdate = Body(..., description="Поля для обновления оператора"),
    session: AsyncSession = Depends(get_db_session),
    repo: OperatorRepo = Depends(get_operator_repo),
):
    op = await repo.get(session, operator_id)
    if not op:
        raise NotFound(message=f"Operator {operator_id} not found")

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(op, k, v)

    await session.commit()
    await session.refresh(op)
    return op
