from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, get_lead_service
from app.services.lead_service import LeadService
from app.schemas.leads import LeadWithContactsOut
from app.schemas.lead import LeadOut
from app.schemas.contact import ContactOut
from app.core.errors import ServerErrorSchema

router = APIRouter(prefix="/leads")


@router.get(
    "",
    response_model=list[LeadWithContactsOut],
    summary="Список лидов с обращениями",
    description=(
        "Возвращает всех лидов и их обращения. "
        "Оптимизировано: лиды и обращения подгружаются одной выборкой (без N+1)."
    ),
    responses={
        status.HTTP_200_OK: {"model": list[LeadWithContactsOut]},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ServerErrorSchema},
    },
)
async def list_leads_with_contacts(
    session: AsyncSession = Depends(get_db_session),
    service: LeadService = Depends(get_lead_service),
):
    leads = await service.list_with_contacts(session)

    return [
        LeadWithContactsOut(
            lead=LeadOut.model_validate(l),
            contacts=[ContactOut.model_validate(c) for c in l.contacts],
        )
        for l in leads
    ]
