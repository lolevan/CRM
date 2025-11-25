from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.repositories.operator_repo import OperatorRepo
from app.repositories.lead_repo import LeadRepo
from app.repositories.source_repo import SourceRepo
from app.repositories.contact_repo import ContactRepo
from app.repositories.source_operator_repo import SourceOperatorRepo
from app.services.distribution import DistributionService
from app.services.contact_service import ContactService
from app.services.lead_service import LeadService
from app.services.stats_service import StatsService


def get_operator_repo() -> OperatorRepo:
    return OperatorRepo()


def get_lead_repo() -> LeadRepo:
    return LeadRepo()


def get_source_repo() -> SourceRepo:
    return SourceRepo()


def get_contact_repo() -> ContactRepo:
    return ContactRepo()


def get_source_operator_repo() -> SourceOperatorRepo:
    return SourceOperatorRepo()


def get_distribution_service(
    contact_repo: ContactRepo = Depends(get_contact_repo),
) -> DistributionService:
    return DistributionService(contact_repo)

def get_lead_service(
    lead_repo: LeadRepo = Depends(get_lead_repo),
) -> LeadService:
    return LeadService(lead_repo)


def get_stats_service(
    contact_repo: ContactRepo = Depends(get_contact_repo),
    source_repo: SourceRepo = Depends(get_source_repo),
    operator_repo: OperatorRepo = Depends(get_operator_repo),
) -> StatsService:
    return StatsService(
        contact_repo=contact_repo,
        source_repo=source_repo,
        operator_repo=operator_repo,
    )

def get_contact_service(
    lead_repo: LeadRepo = Depends(get_lead_repo),
    source_repo: SourceRepo = Depends(get_source_repo),
    contact_repo: ContactRepo = Depends(get_contact_repo),
    distribution: DistributionService = Depends(get_distribution_service),
) -> ContactService:
    return ContactService(
        lead_repo=lead_repo,
        source_repo=source_repo,
        contact_repo=contact_repo,
        distribution=distribution,
    )


def get_db_session(session: AsyncSession = Depends(get_session)) -> AsyncSession:
    return session
