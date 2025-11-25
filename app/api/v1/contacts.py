from __future__ import annotations

from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, get_contact_service
from app.services.contact_service import ContactService
from app.schemas.contact import ContactCreate, ContactOut
from app.core.errors import (
    ValidationErrorSchema, NotFoundErrorSchema, NoOperatorsAvailableSchema, ServerErrorSchema
)

router = APIRouter(prefix="/contacts")


@router.post(
    "",
    response_model=ContactOut,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация обращения",
    description=(
        "Принимает данные лида и код источника. "
        "Создаёт/находит лида, выбирает оператора с учётом лимита и весов, "
        "создаёт обращение. Если операторов нет — operator_id=null."
    ),
    responses={
        status.HTTP_201_CREATED: {"model": ContactOut},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundErrorSchema},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ServerErrorSchema},
    },
)
async def register_contact(
    payload: ContactCreate = Body(..., description="Данные обращения"),
    session: AsyncSession = Depends(get_db_session),
    service: ContactService = Depends(get_contact_service),
):
    async with session.begin():  # транзакционная граница сеньор-стайл
        contact = await service.register_contact(
            session=session,
            external_id=payload.lead.external_id,
            phone=payload.lead.phone,
            email=payload.lead.email,
            source_code=payload.source_code,
            payload=payload.payload,
        )
    await session.refresh(contact)
    return contact
