from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import Lead
from app.models.contact import Contact, ContactStatus
from app.repositories.lead_repo import LeadRepo
from app.repositories.source_repo import SourceRepo
from app.repositories.contact_repo import ContactRepo
from app.services.distribution import DistributionService
from app.core.exceptions import NotFound


class ContactService:
    def __init__(
        self,
        lead_repo: LeadRepo,
        source_repo: SourceRepo,
        contact_repo: ContactRepo,
        distribution: DistributionService,
    ):
        self._lead_repo = lead_repo
        self._source_repo = source_repo
        self._contact_repo = contact_repo
        self._distribution = distribution

    async def register_contact(
        self,
        session: AsyncSession,
        *,
        external_id: str,
        source_code: str,
        phone: str | None = None,
        email: str | None = None,
        payload: str | None = None,
    ) -> Contact:
        """
        1) Найти/создать лид
        2) Найти источник
        3) Выбрать оператора по весам и лимитам
        4) Создать обращение (если операторов нет — operator_id=None)
        """
        lead = await self._lead_repo.get_by_external_id(session, external_id)
        if not lead:
            lead = await self._lead_repo.create(
                session, Lead(external_id=external_id, phone=phone, email=email)
            )

        source = await self._source_repo.get_by_code(session, source_code)
        if not source:
            raise NotFound(message=f"Source '{source_code}' not found")

        operator = await self._distribution.choose_operator(session, source.id)

        contact = Contact(
            lead_id=lead.id,
            source_id=source.id,
            operator_id=operator.id if operator else None,
            status=ContactStatus.active,
            payload=payload,
        )
        await self._contact_repo.create(session, contact)
        return contact
