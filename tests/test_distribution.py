import asyncio

import pytest
from sqlalchemy import func, select

from app.models.contact import Contact, ContactStatus
from app.models.lead import Lead
from app.models.operator import Operator
from app.models.source import Source
from app.models.source_operator import SourceOperatorConfig
from app.repositories.contact_repo import ContactRepo
from app.services.distribution import DistributionService

@pytest.mark.asyncio
async def test_weighted_distribution_basic(client):
    # create operators
    op1 = (await client.post("/api/v1/operators", json={"name": "op1", "max_active_contacts": 1000})).json()
    op2 = (await client.post("/api/v1/operators", json={"name": "op2", "max_active_contacts": 1000})).json()

    # create source
    s = (await client.post("/api/v1/sources", json={"code": "A", "name": "Bot A"})).json()

    # set weights 10 vs 30 (25% / 75%)
    await client.put(f"/api/v1/sources/{s['id']}/operators", json={
        "operators": [
            {"operator_id": op1["id"], "weight": 10},
            {"operator_id": op2["id"], "weight": 30},
        ]
    })

    # simulate 200 contacts
    counts = {op1["id"]: 0, op2["id"]: 0, None: 0}
    for i in range(200):
        c = (await client.post("/api/v1/contacts", json={
            "lead": {"external_id": f"L{i}"},
            "source_code": "A",
            "payload": "hi"
        })).json()
        counts[c["operator_id"]] += 1

    # expect roughly 1:3 ratio
    ratio = counts[op2["id"]] / max(counts[op1["id"]], 1)
    assert 2.0 < ratio < 4.5


@pytest.mark.asyncio
async def test_parallel_assignments_respect_limit(session_maker):
    distribution = DistributionService(ContactRepo())

    async with session_maker() as session:
        async with session.begin():
            operator = Operator(name="op", max_active_contacts=1)
            source = Source(code="SRC-P", name="Src P")
            cfg = SourceOperatorConfig(source=source, operator=operator, weight=1)
            session.add_all([operator, source, cfg])

        operator_id = operator.id
        source_id = source.id

    ready = asyncio.Event()
    proceed = asyncio.Event()

    async def assign_contact(name: str, *, wait_before_create: bool = False):
        async with session_maker() as session:
            async with session.begin():
                op = await distribution.choose_operator(session, source_id)

                if wait_before_create:
                    ready.set()
                    await proceed.wait()

                if not op:
                    return None

                lead = Lead(external_id=f"lead-{name}")
                session.add(lead)
                await session.flush()

                session.add(
                    Contact(
                        lead_id=lead.id,
                        source_id=source_id,
                        operator_id=op.id,
                        status=ContactStatus.active,
                    )
                )
                return op.id

    task1 = asyncio.create_task(assign_contact("first", wait_before_create=True))
    await ready.wait()
    task2 = asyncio.create_task(assign_contact("second"))

    proceed.set()
    first_op, second_op = await asyncio.gather(task1, task2)

    assert first_op == operator_id
    assert second_op is None

    async with session_maker() as session:
        res = await session.execute(
            select(func.count(Contact.id)).where(
                Contact.operator_id == operator_id,
                Contact.status == ContactStatus.active,
            )
        )
        assert res.scalar() == 1
