import pytest

@pytest.mark.asyncio
async def test_register_contact_creates_lead_and_contact(client):
    op = (await client.post("/api/v1/operators", json={"name": "op1", "max_active_contacts": 10})).json()
    s = (await client.post("/api/v1/sources", json={"code": "bot1", "name": "Bot 1"})).json()
    await client.put(f"/api/v1/sources/{s['id']}/operators", json={
        "operators": [{"operator_id": op["id"], "weight": 1}]
    })

    c = (await client.post("/api/v1/contacts", json={
        "lead": {"external_id": "user-1", "phone": "123"},
        "source_code": "bot1"
    })).json()

    assert c["operator_id"] == op["id"]
    assert c["status"] == "active"

    leads = (await client.get("/api/v1/leads")).json()
    assert len(leads) == 1
    assert leads[0]["lead"]["external_id"] == "user-1"
    assert len(leads[0]["contacts"]) == 1

@pytest.mark.asyncio
async def test_no_operators_creates_contact_without_operator(client):
    await client.post("/api/v1/sources", json={"code": "empty", "name": "Empty Bot"})
    c = (await client.post("/api/v1/contacts", json={
        "lead": {"external_id": "u2"},
        "source_code": "empty"
    })).json()
    assert c["operator_id"] is None
    assert c["status"] == "active"
